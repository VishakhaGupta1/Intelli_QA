from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
	sys.path.insert(0, str(BASE_DIR))

load_dotenv()

from logging_config import get_logger
import gap_analyzer
import groq_client
import mock_claude
import spec_parser
import test_writer

logger = get_logger(__name__)


def _write_spec_endpoints_to_disk(endpoints: List[Dict]) -> Path:
	output_dir = BASE_DIR / "output"
	output_dir.mkdir(parents=True, exist_ok=True)
	output_file = output_dir / "spec_endpoints.json"
	output_file.write_text(json.dumps(endpoints, indent=2, ensure_ascii=False), encoding="utf-8")
	return output_file


def _write_spec_endpoints_to_mongo(endpoints: List[Dict]) -> None:
	mongo_uri = os.getenv("MONGO_URI")
	if not mongo_uri:
		return
	try:
		from pymongo import MongoClient
	except Exception:
		logger.warning("pymongo not installed; skipping Mongo spec endpoint persistence")
		return
	client = None
	try:
		client = MongoClient(mongo_uri)
		db_name = os.getenv("MONGO_DB_NAME", "qa_platform")
		collection = client[db_name]["spec_endpoints"]
		documents = []
		for endpoint in endpoints:
			documents.append({
				"path": endpoint.get("path"),
				"method": endpoint.get("method"),
				"tag": (endpoint.get("tags") or ["untagged"])[0] if endpoint.get("tags") else "untagged",
				"summary": endpoint.get("summary", ""),
				"parsedAt": datetime.utcnow().isoformat(),
			})
		if documents:
			collection.delete_many({})
			collection.insert_many(documents)
	except Exception as exc:
		logger.warning("Could not persist spec endpoints to MongoDB: %s", exc)
	finally:
		if client is not None:
			try:
				client.close()
			except Exception:
				pass


def _generate_cases_for_endpoint(endpoint: Dict) -> List[Dict]:
	if os.getenv("USE_MOCK", "false").lower() == "true":
		logger.info("USE_MOCK=true; generating mock test cases for %s %s", endpoint.get("method"), endpoint.get("path"))
		return mock_claude.get_mock_test_cases(endpoint)
	try:
		cases = groq_client.generate_test_cases(endpoint)
		logger.info("Generated %s test case(s) for %s %s", len(cases), endpoint.get("method"), endpoint.get("path"))
		return cases
	except Exception as exc:
		logger.warning("Groq generation failed for %s %s: %s", endpoint.get("method"), endpoint.get("path"), exc)
		return mock_claude.get_mock_test_cases(endpoint)


def main() -> int:
	parser = argparse.ArgumentParser(description="Generate Java API tests from an OpenAPI spec")
	parser.add_argument("--spec", default=str(BASE_DIR / "specs" / "sample-api.yaml"), help="Path to OpenAPI YAML/JSON file")
	parser.add_argument(
		"--output",
		default=str((BASE_DIR.parent / "test-engine" / "src" / "test" / "java" / "com" / "qaplatform" / "api" / "SampleApiTests.java").resolve()),
		help="Output Java file path",
	)
	args = parser.parse_args()
	logger.info("Starting generator for spec: %s", args.spec)
	endpoints = spec_parser.parse_spec(args.spec)
	logger.info("Parsed %s endpoints", len(endpoints))
	for endpoint in endpoints:
		logger.info("Found endpoint: %s %s", endpoint.get("method"), endpoint.get("path"))
	json_path = _write_spec_endpoints_to_disk(endpoints)
	logger.info("Saved parsed endpoints to %s", json_path)
	_write_spec_endpoints_to_mongo(endpoints)
	untested = gap_analyzer.find_untested_endpoints(endpoints)
	logger.info("Untested endpoints: %s", len(untested))
	for endpoint in untested:
		logger.info("Gap: %s %s", endpoint.get("method"), endpoint.get("path"))
	all_test_cases: List[Dict] = []
	for endpoint in endpoints:
		all_test_cases.extend(_generate_cases_for_endpoint(endpoint))
	test_writer.write_test_file(all_test_cases, args.output)
	logger.info("Wrote generated Java tests to %s", args.output)
	logger.info("Generated %s test cases across %s endpoints", len(all_test_cases), len(endpoints))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

"""Import test results and spec endpoints into MongoDB from local build artifacts.

This script backfills the dashboard data source when the Java result writer is
not persisting documents directly.
"""
from __future__ import annotations

import os
import re
import sys
import uuid
import json
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from pymongo import MongoClient

ROOT = Path(__file__).resolve().parent.parent
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "qa_platform")
SUREFIRE_DIR = ROOT / "test-engine" / "target" / "surefire-reports"
SPEC_ENDPOINTS_JSON = ROOT / "ai-generator" / "output" / "spec_endpoints.json"
API_SOURCE = ROOT / "test-engine" / "src" / "test" / "java" / "com" / "qaplatform" / "api" / "SampleApiTests.java"


def load_endpoint_map(source_path: Path) -> dict[str, str]:
    """Map Java test method names to the endpoint they set before execution."""
    if not source_path.exists():
        return {}

    content = source_path.read_text(encoding="utf-8")
    pattern = re.compile(r"public void\s+(\w+)\s*\(\) throws Exception \{\s*setCurrentEndpoint\(\"([^\"]+)\"\);", re.DOTALL)
    return {match.group(1): match.group(2) for match in pattern.finditer(content)}


def parse_testcases(xml_path: Path, endpoint_map: dict[str, str]) -> list[dict]:
    """Parse one Surefire XML report into MongoDB-ready test result documents."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    classname = root.attrib.get("name", "")
    layer = "ui" if ".ui." in classname or classname.endswith("UITests") else "api"
    now = datetime.utcnow().isoformat()
    results: list[dict] = []

    for testcase in root.findall("testcase"):
        name = testcase.attrib.get("name", "unknown")
        duration = int(float(testcase.attrib.get("time", "0")) * 1000)
        failure_node = testcase.find("failure") or testcase.find("error")
        status = "failed" if failure_node is not None else "passed"
        failure_message = None
        if failure_node is not None:
            failure_message = (failure_node.text or "").strip() or failure_node.attrib.get("message")

        result = {
            "testName": name,
            "layer": layer,
            "status": status,
            "duration": duration,
            "failureMessage": failure_message,
            "failureType": None,
            "runId": str(uuid.uuid4()),
            "runAt": now,
            "tags": [layer],
            "endpoint": endpoint_map.get(name),
        }
        results.append(result)

    return results


def load_spec_endpoints() -> list[dict]:
    """Load parsed spec endpoints from the generator output JSON file."""
    if not SPEC_ENDPOINTS_JSON.exists():
        return []

    try:
        data = json.loads(SPEC_ENDPOINTS_JSON.read_text(encoding="utf-8"))
    except Exception:
        return []

    parsed_at = datetime.utcnow().isoformat()
    documents = []
    for endpoint in data:
        tags = endpoint.get("tags") or []
        tag = tags[0] if isinstance(tags, list) and tags else "untagged"
        documents.append({
            "path": endpoint.get("path"),
            "method": endpoint.get("method"),
            "tag": tag,
            "summary": endpoint.get("summary", ""),
            "parsedAt": parsed_at,
        })
    return documents


def main() -> int:
    """Backfill MongoDB collections from local artifacts and exit with a status code."""
    if not SUREFIRE_DIR.exists():
        print(f"Missing Surefire directory: {SUREFIRE_DIR}")
        return 1

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    endpoint_map = load_endpoint_map(API_SOURCE)
    test_results: list[dict] = []
    for xml_file in sorted(SUREFIRE_DIR.glob("TEST-*.xml")):
        test_results.extend(parse_testcases(xml_file, endpoint_map))

    spec_endpoints = load_spec_endpoints()

    if spec_endpoints:
        db.spec_endpoints.delete_many({})
        db.spec_endpoints.insert_many(spec_endpoints)

    if test_results:
        db.test_results.delete_many({})
        db.test_results.insert_many(test_results)

    print(f"Imported {len(spec_endpoints)} spec endpoints and {len(test_results)} test results into MongoDB.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

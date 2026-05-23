# Troubleshooting Guide

## Common Errors and Fixes

### Docker Compose says port 27017 is already allocated
- Cause: a local MongoDB service or another container is using the port.
- Fix: stop the host `mongod` process or keep the temporary Mongo host mapping on 27018.

### Generator fails with LLM errors
- Cause: missing or invalid `GROK_API_KEY`, provider outage, or bad endpoint payload.
- Fix: confirm the key, check network access, and use mock fallback only for non-production work.

### Generated Java does not compile
- Cause: malformed AI output or invalid test names.
- Fix: inspect the generated prompt/response and verify the writer escaping logic; the current `test_writer.py` sanitizes names and strings.

### Dashboard UI loads but shows no data
- Cause: API base URL mismatch or MongoDB has no data yet.
- Fix: verify `VITE_API_BASE_URL`, dashboard API `/health`, and that MongoDB has `test_results` and `spec_endpoints`.

### Dashboard API returns 503 on readiness
- Cause: MongoDB is not reachable.
- Fix: verify `MONGO_URI`, MongoDB credentials, and the internal network path.

### UI tests are flaky
- Cause: browser timing, remote Selenium issues, or DOM changes.
- Fix: inspect page object waits, increase explicit wait usage, and confirm the remote browser image version.

## Log Interpretation
- **Python generator logs**: look for Grok request failures, JSON parse errors, and mock fallback notices.
- **Java logs**: look for Mongo retry messages, test failures, and stack traces.
- **Node logs**: look for request IDs, route names, and response times.

## Failure Investigation Workflow
1. Check the dashboard API `/ready` endpoint.
2. Check MongoDB connectivity.
3. Inspect the latest generator log.
4. Inspect Surefire reports in `test-engine/target/surefire-reports`.
5. Correlate failures with the request ID in the Node logs.
6. Re-run the affected layer in isolation.

## Performance Profiling Tips
- Time Grok generation per endpoint.
- Measure MongoDB query latency separately from API response time.
- Profile the `/api/results/trend` endpoint first when dashboards slow down.
- Measure browser startup and page load separately for UI suites.

## Escalation Guidance
- Platform issue: MongoDB, Docker, or CI failure.
- QA issue: generated tests, flakiness, or false positives.
- Security issue: secret exposure, auth bypass, or PII leakage.

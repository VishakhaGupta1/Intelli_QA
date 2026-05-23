# API Reference

## Dashboard API Base URL
- Local default: `http://localhost:3001/api`
- Override with `VITE_API_BASE_URL` for the UI and `PORT`/`CORS_ORIGINS` for the API.

## Endpoints

### POST `/api/auth/token`
Issues a JWT after validating `client_secret`.
- Request body:
```json
{
	"client_secret": "<strong-random-secret>",
	"subject": "dashboard-client"
}
```
- Successful response:
```json
{
	"token": "<jwt>",
	"tokenType": "Bearer",
	"expiresIn": "1h"
}
```
- Failure response:
```json
{ "error": "Invalid client secret" }
```
- Access control: `client_secret` must match the configured `CLIENT_SECRET`.

### GET `/api/results`
Returns test results and summary stats.
- Query params: `layer`, `status`, `days`
- Response fields: `results`, `stats`
- Data source: MongoDB `test_results`

### GET `/api/results/trend`
Returns daily trend data for the last N days.
- Query params: `days`
- Response: array of `{ date, totalTests, apiPassRate, uiPassRate }`
- Data source: MongoDB `test_results`

### GET `/api/defects`
Returns logged defects.
- Data source: MongoDB `defect_logs`
- Expected use: defect analysis and dashboard cards

### GET `/api/coverage`
Returns coverage summary.
- Data source: MongoDB `spec_endpoints` and passed `test_results`
- Response: `totalEndpoints`, `testedEndpoints`, `coveragePercent`, `byTag`

### GET `/api/flakiness`
Returns the top flaky tests.
- Data source: MongoDB `test_results`
- Response: grouped items with `testName`, `layer`, `failCount`, `rootCause`, `lastSeen`

### GET `/api/gap-report`
Returns the latest AI-generated gap report.
- Data source: MongoDB `gap_reports`
- Response: `report`, `flaggedEndpoints`, `coverageSummary`, `generatedAt`

### GET `/api/metrics`
Returns aggregate operational metrics.
- Data source: MongoDB and process uptime
- Response: `uptimeSeconds`, `testResults`, `defects`, `gapReports`, `coveragePercent`

### GET `/metrics`
Returns Prometheus-formatted metrics.
- Access control: IP allowlist only (`127.0.0.1`, `::1`, and the Docker internal subnet by default)
- Exposes default Node metrics plus custom counters/gauges/histograms

### GET `/health`
Returns API liveness.

### GET `/ready`
Returns API readiness based on MongoDB connectivity.

## Error Model
- Validation errors return:
```json
{
	"error": "Validation failed",
	"details": [
		{ "field": "limit", "message": "Must be between 1 and 1000" }
	]
}
```
- Most routes return JSON with `{ error: message }` on failure.
- The server also has a top-level error handler that returns `{ error: 'internal_server_error', requestId }`.

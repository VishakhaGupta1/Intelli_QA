# Deployment Checklist

## Pre-Deployment Validation
- Confirm `GROK_API_KEY` is present in CI secrets and in the production secret store.
- Confirm `MONGO_URI`, `MONGO_DB_NAME`, `BASE_URL`, `VITE_API_BASE_URL`, and `CORS_ORIGINS` are set for the target environment.
- Run `mvn test` in [test-engine](../test-engine) and verify the full suite passes.
- Run the generator against a real spec with Grok enabled and confirm the Java output compiles.
- Verify MongoDB connectivity and the dashboard API `/health` and `/ready` endpoints.
- Confirm the UI builds with `npm run build`.
- Check that all sensitive files are excluded by [.gitignore](../.gitignore).

## Recommended Deployment Order
1. MongoDB.
2. Dashboard API.
3. Selenium.
4. Test engine / generated test execution.
5. Dashboard UI.

## Deployment Procedure
- Apply environment variables and secrets first.
- Start MongoDB and verify it is reachable from the internal network only.
- Start the dashboard API and validate `/health` and `/ready`.
- Run the generator and then the Java test suite.
- Load the dashboard UI and verify it can read live data from the API.

## Health Check Procedure
- Check [dashboard-api/server.js](../dashboard-api/server.js) `/health` and `/ready`.
- Verify MongoDB ping succeeds.
- Verify the dashboard UI receives 200 responses from `/api/results`, `/api/coverage`, `/api/defects`, `/api/flakiness`, `/api/gap-report`, and `/api/metrics`.

## Rollback Procedure
- Revert to the previous container image or deployment artifact.
- Restore the previous MongoDB backup if data migration was involved.
- Keep the last known-good Surefire reports and generated Java files for comparison.
- If the dashboard API is the source of failure, stop it first and leave MongoDB intact.

## Disaster Recovery
- Back up MongoDB regularly.
- Export generated Java tests and Surefire artifacts to durable storage.
- Store CI artifacts for each deployment.
- Keep a documented way to rebuild the environment from scratch using the repo plus secrets.

## Deployment Notes
- Keep `ALLOW_MOCK_FALLBACK=false` in production unless you explicitly want the system to degrade to mock output.
- Do not expose Mongo Express publicly in production.
- Pin the Selenium image version before production rollout.

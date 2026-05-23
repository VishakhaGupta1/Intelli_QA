# Operations Runbook

## Start / Stop
### Local Start
- Start Docker Compose from the repository root.
- Ensure `MONGO_URI` points to the running MongoDB instance.
- Run the generator if you need to regenerate tests.
- Execute `cd test-engine && mvn test` to run the suite.

### Stop
- Stop the dashboard API first if you need to preserve MongoDB state.
- Stop the Selenium container next.
- Stop MongoDB last.
- Kill stray local `mongod` processes if a port collision remains.

## Monitoring
- Dashboard API: `/health`, `/ready`, `/api/metrics`.
- MongoDB: connection success/failure and write latency.
- Generator: per-endpoint generation latency and Grok error counts.
- Test engine: test counts, failure counts, flakiness classification, and Mongo write retries.
- UI: build success and API fetch failures.

## Common Issues and Fixes
- **Mongo port already allocated**: stop the host `mongod` process or change the host port mapping.
- **LLM unavailable**: verify `GROK_API_KEY`; if needed, enable mock fallback for non-production work.
- **Dashboard UI shows blank state**: check the API base URL and verify the dashboard API is reachable.
- **Tests fail but results are missing**: inspect Surefire output and `MongoResultWriter` logs.
- **Selenium session errors**: confirm the browser image version and remote URL.

## Credential Rotation
- Rotate `GROK_API_KEY` in the secret store and CI secrets.
- Rotate MongoDB credentials if auth is enabled.
- Update `.env` locally from the new secret values.
- Restart the generator, dashboard API, and test engine after rotation.

## Backups
- Run `./scripts/backup-mongo.sh` daily from cron or a scheduled task.
- Example cron entry: `0 2 * * * cd /path/to/qa-intelligence-platform-master && BACKUP_DIR=/backups ./scripts/backup-mongo.sh`
- Keep the backup directory on durable storage and copy archives off-host regularly.
- Use `./scripts/restore-mongo.sh /backups/YYYY-MM-DD-HH-MM.tar.gz` to restore a snapshot.

## Index Verification
- Run `node db-init/verify-indexes.js` after every deployment to confirm indexes are present.

## Escalation
- Escalate to platform ownership if MongoDB is unavailable.
- Escalate to QA engineering if generated tests become invalid or unstable.
- Escalate to security if any secret or PII leakage is suspected.

## On-Call Checklist
- Check `/ready` first.
- Check MongoDB connectivity next.
- Check Grok availability and generation latency.
- Check the latest Surefire report and dashboard API logs.

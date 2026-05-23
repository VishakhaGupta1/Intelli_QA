# Quick Reference

## Common Commands

### Start local stack
```powershell
docker compose up -d --build
```

### Get an auth token
```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:3001/api/auth/token -ContentType application/json -Body '{"client_secret":"<your-client-secret>"}'
```

### Check Prometheus metrics
```powershell
Invoke-WebRequest http://localhost:3001/metrics
```

### Verify MongoDB indexes
```powershell
node db-init/verify-indexes.js
```

### Run the Mongo backup
```powershell
bash ./scripts/backup-mongo.sh
```

### Rotate JWT secret
```powershell
# Update JWT_SECRET and CLIENT_SECRET in the secret store, then restart the dashboard API.
```

### Run generator
```powershell
cd ai-generator
python main.py --spec .\specs\sample-api.yaml
```

### Run Java tests
```powershell
cd test-engine
mvn test
```

### Build dashboard UI
```powershell
cd dashboard-ui
npm run build
```

### Start dashboard API
```powershell
cd dashboard-api
node server.js
```

## Common Environment Variables
- `GROK_API_KEY`: preferred LLM key.
- `MONGO_URI`: Mongo connection string.
- `MONGO_DB_NAME`: database name.
- `BASE_URL`: API under test.
- `SELENIUM_REMOTE_URL`: remote browser endpoint.
- `VITE_API_BASE_URL`: dashboard API base URL used by the React client.
- `CORS_ORIGINS`: comma-separated allowed origins.

## Useful Paths
- Generator output: [ai-generator/output/spec_endpoints.json](../ai-generator/output/spec_endpoints.json)
- Java tests: [test-engine/src/test/java/com/qaplatform/api/SampleApiTests.java](../test-engine/src/test/java/com/qaplatform/api/SampleApiTests.java)
- Surefire reports: [test-engine/target/surefire-reports](../test-engine/target/surefire-reports)
- Docker stack: [docker-compose.yml](../docker-compose.yml)

## First Things to Check When Broken
1. Dashboard API `/ready`
2. MongoDB connectivity
3. Grok API key / generation logs
4. Surefire reports
5. Browser/Selenium connectivity

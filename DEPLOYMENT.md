# Deploying IntelliQA to Render

## Prerequisites
- Render account (free at render.com)
- MongoDB Atlas free cluster (mongodb.com/atlas)

## Steps

### 1. Set up MongoDB Atlas
1. Create free cluster at mongodb.com/atlas
2. Create database user with readWrite access
3. Whitelist 0.0.0.0/0 for Render IP access
4. Copy connection string

### 2. Deploy to Render
1. Go to render.com -> New -> Blueprint
2. Connect your GitHub repo: VishakhaGupta1/IntelliQA
3. Render will detect render.yaml automatically
4. Set these environment variables in Render dashboard:
   - JWT_SECRET: (generate with: openssl rand -hex 32)
   - CLIENT_SECRET: (generate with: openssl rand -hex 32)
   - MONGO_URI: (your MongoDB Atlas connection string)
   - CORS_ORIGIN: (your Render dashboard-api URL)
5. Click Deploy

### 3. Verify deployment
curl https://intelliqa-dashboard-api.onrender.com/health

### 4. Get your auth token
curl -X POST https://intelliqa-dashboard-api.onrender.com/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_secret": "your-CLIENT_SECRET-value"}'

### 5. Point the dashboard UI at the deployed API
Set VITE_API_URL=https://intelliqa-dashboard-api.onrender.com in your
dashboard-ui build environment.
#!/usr/bin/env bash
set -euo pipefail

jwt_secret=$(openssl rand -hex 32)
client_secret=$(openssl rand -hex 32)

cat <<EOF
New rotation values:
JWT_SECRET=${jwt_secret}
CLIENT_SECRET=${client_secret}

Update these values in GitHub Environments:
- staging
- production

After updating the secrets, restart the dashboard-api container so it picks up the new values.
EOF
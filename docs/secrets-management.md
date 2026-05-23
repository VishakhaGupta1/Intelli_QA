# Secrets Management

## Secret Flow

Secrets follow this path:

1. Local development starts with a generated `.env` file created by `scripts/generate-secrets.sh`.
2. CI/CD uses the GitHub `staging` environment for scoped secret storage.
3. Runtime containers and jobs consume the secrets from their environment-specific configuration.

This keeps local bootstrap and CI separated while using the same secret names across stages.

## Rotation Schedule

- `JWT_SECRET`: every 90 days
- `CLIENT_SECRET`: every 90 days
- `MONGO_PASSWORD`: every 180 days
- `GROQ_API_KEY`: only on compromise or provider-side key rotation

## Rotation Procedure

### JWT_SECRET

1. Run `scripts/rotate-secrets.sh`.
2. Copy the new `JWT_SECRET` into the `staging` GitHub Environment.
3. Restart the dashboard API service.

### CLIENT_SECRET

1. Run `scripts/rotate-secrets.sh`.
2. Update the `CLIENT_SECRET` value in the `staging` GitHub Environment.
3. Restart any service that mints tokens.

### MONGO_PASSWORD

1. Generate a new `MONGO_PASSWORD` value with `scripts/generate-secrets.sh` or a one-off `openssl rand -hex 32` command.
2. Update the app user password in MongoDB and the matching secret in the `staging` GitHub Environment.
3. Restart `dashboard-api` and any pipeline jobs that use the database connection.

### GROQ_API_KEY

1. Revoke the old key in the Groq console.
2. Add the replacement to the `staging` GitHub Environment.
3. Re-run the generator and gap analysis jobs.

## Emergency Rotation

If a secret is suspected to be compromised:

1. Revoke or replace the secret immediately.
2. Update the `staging` GitHub Environment with fresh values.
3. Restart the dashboard API, generator jobs, and any other consumers.
4. Review logs for abnormal access.
5. Verify that the exposed value is no longer present in build logs, shell history, or artifacts.

## If a Secret Was Committed

1. Rotate the secret immediately.
2. Remove the value from the repository history if policy requires it.
3. Rebuild any affected containers or workflows with the new secret.
4. Confirm that the previous value has been revoked before resuming deployments.
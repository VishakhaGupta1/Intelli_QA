# GitHub Environment Setup

Use GitHub Environments to scope CI secrets by deployment stage instead of keeping them at the repository level.

## Environments To Create

Create one environment in **Settings → Environments**:

- `staging`

## Secret Names

Store these exact secret names in the environments:

- `GROQ_API_KEY`
- `JWT_SECRET`
- `CLIENT_SECRET`
- `MONGO_USERNAME`
- `MONGO_PASSWORD`
- `MONGO_INITDB_ROOT_USERNAME`
- `MONGO_INITDB_ROOT_PASSWORD`
- `GRAFANA_ADMIN_PASSWORD`

Suggested placement:

- `staging`: `GROQ_API_KEY`, `JWT_SECRET`, `CLIENT_SECRET`, `MONGO_USERNAME`, `MONGO_PASSWORD`, `MONGO_INITDB_ROOT_USERNAME`, `MONGO_INITDB_ROOT_PASSWORD`, `GRAFANA_ADMIN_PASSWORD`

## Operational Notes

- GitHub Environments keep the CI secrets scoped to the job that declares the environment.
- Do not duplicate these values in repository-level secrets unless you are migrating an old workflow.
- Rotate the staging environment secrets on a fixed schedule and immediately after any suspected exposure.
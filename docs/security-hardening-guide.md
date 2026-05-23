# Security Hardening Guide

## Immediate Actions
- Add authentication to the dashboard API.
- Add rate limiting to the dashboard API.
- Protect Mongo Express or remove it from production deployments.
- Pin external container image versions.
- Make production CORS origins explicit via `CORS_ORIGINS`.
- Redact or avoid logging any URI with embedded credentials.
- Redact PII before sending prompts to Grok.

## Short-Term Actions (1 to 2 Weeks)
- Add request validation and payload size limits.
- Store secrets in a real secrets manager, not in plaintext files.
- Add MongoDB authentication and network isolation.
- Add indexes for dashboard queries and trend calculations.
- Add structured audit logs for admin actions and deployment changes.
- Add security checks to CI for secrets and dependency vulnerabilities.

## Long-Term Actions (1 to 3 Months)
- Move to managed secret storage such as AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault.
- Add SSO or token-based authentication for the dashboard API and UI.
- Introduce PII classification and redaction for LLM prompts.
- Add a formal retention policy for logs and artifacts.
- Perform dependency pinning and automatic security patch tracking.
- Add container image signing and supply-chain validation.

## Secrets Management Recommendation
Use a centralized secrets manager in production and GitHub Secrets in CI. For local development, keep `.env` files untracked and separate from committed examples.

## Secret Rotation
- Rotate `JWT_SECRET` and `CLIENT_SECRET` together so token minting and verification stay aligned.
- Generate both values as high-entropy random strings with at least 32 characters.
- Update the production secret store first, then restart the dashboard API so the new values take effect.
- After rotation, invalidate old tokens by forcing a re-login or short token expiry window.

## MongoDB Security Recommendation
Use auth, bind only to the internal Docker or cluster network, and do not publish MongoDB to public interfaces. Keep backups encrypted and access-controlled.

## API Authentication Recommendation
Use JWT or a signed service token for the dashboard API. If the dashboard is only internal, place it behind an identity-aware proxy or VPN rather than leaving it public.

## Preventing PII Leakage to Grok
- Strip identifiers, emails, phone numbers, account numbers, and tokens before prompt construction.
- Keep prompt inputs limited to schema and synthetic examples.
- Log only sanitized summaries of prompts and responses.
- Consider a policy that blocks generation for specs marked as sensitive.

## Current Security Posture
- Good: env-based config, `.gitignore` exclusions, secret usage in CI, mock fallback for local testing.
- Weak: no auth, no rate limiting, and no dedicated secrets manager yet.

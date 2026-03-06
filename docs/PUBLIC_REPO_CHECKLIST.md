# Public Repo Checklist

Use this checklist before making the repository public.

## Repository Hygiene

- `.env` is ignored
- `data/whoop_tokens.json` is ignored
- `state/` and runtime logs are ignored
- no personal WHOOP payloads are tracked
- no secrets appear in markdown examples or screenshots

## Secret Review

- no WHOOP client credentials are committed
- no access tokens are committed
- no refresh tokens are committed
- no deployment secrets appear in tracked files
- any past leaked secret has been rotated before publication

## Documentation Review

- `README.md` describes the project without exposing private details
- `SECURITY.md` matches the real security posture
- strategy docs are public-safe and repository-relative
- setup instructions use placeholders, not live values

## Runtime Safety

- `APP_API_KEY` is required for any deployed WHOOP-backed endpoint
- logs do not capture authorization headers or token payloads
- `/auth/callback` is open only because the OAuth flow requires it
- protected routes are documented as protected routes

## Hosting Safety

- host secrets are configured outside git
- deployed logs have been spot-checked for sensitive data
- the hosted base URL uses HTTPS
- health and protected requests have been tested separately

## Commit History Review

- no sensitive files remain in the visible history you intend to publish
- no copied terminal output includes secrets
- no issue or PR templates expose personal data patterns

## Release-Day Check

- repository settings and Actions secrets have been re-checked
- public docs still reflect the intended current scope
- helper pages in `docs/` do not expose private data
- an external reader can understand the project without learning anything sensitive

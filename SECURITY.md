# Security Notes

This repository is safe to make public only if secrets and personal WHOOP data stay out of git and out of public logs.

## Never Commit

- `.env`
- `data/whoop_tokens.json`
- WHOOP access tokens
- WHOOP refresh tokens
- deployment secrets
- copied personal WHOOP payloads

## Runtime Expectations

- keep source code and docs public-safe
- keep secrets in local environment variables or hosting-provider secrets
- protect WHOOP-backed routes with `APP_API_KEY` in any deployed environment

## Protected Routes

When `APP_API_KEY` is set, these routes should be treated as private:

- `/whoop/profile`
- `/whoop/recovery`
- `/whoop/sleep`
- `/whoop/workouts`
- `/whoop/context`

`/auth/login` remains open so a browser can start the WHOOP OAuth flow.

`/auth/callback` remains open because WHOOP redirects there directly.

## API Key Usage

Clients can send the key as either:

```text
X-API-Key: your-secret
```

or:

```text
Authorization: Bearer your-secret
```

## Public Repo Rule

Anyone should be able to read every tracked file in this repository without gaining access to the operator's WHOOP account, tokens, or personal health data.

See [`docs/PRIVACY_AND_SECURITY_MODEL.md`](./docs/PRIVACY_AND_SECURITY_MODEL.md) for the full privacy and security model.

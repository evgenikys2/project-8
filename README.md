# WHOOP AI Assistant

WHOOP AI Assistant is a personal-first FastAPI service that turns WHOOP data into a compact health context for AI workflows.

The project already supports a working WHOOP OAuth flow, real data retrieval, and a consolidated `GET /whoop/context` endpoint. The strategic goal is to make that context reliably usable from an AI assistant, ideally including everyday mobile use, while keeping code public-safe and personal data private.

## Current Scope

- Single-user, personal-first backend
- Real WHOOP data ingestion with token refresh
- Stable endpoints for `profile`, `recovery`, `sleep`, `workouts`, and `whoop/context`
- Reduced assistant endpoint for GPT-style integrations
- API-key protection for private WHOOP endpoints
- Public-repo preparation without exposing secrets or personal data

## API Surface

- `GET /health`
- `GET /auth/login`
- `GET /auth/callback`
- `GET /whoop/profile`
- `GET /whoop/recovery`
- `GET /whoop/sleep`
- `GET /whoop/workouts`
- `GET /whoop/context`
- `GET /assistant/context`
- `GET /openapi/assistant-public.json`

## Documentation

Start with the docs hub:

- [`docs/README.md`](./docs/README.md)

Core strategy documents:

- [`docs/PROJECT_STRATEGY.md`](./docs/PROJECT_STRATEGY.md)
- [`docs/TECHNICAL_STRATEGY.md`](./docs/TECHNICAL_STRATEGY.md)
- [`docs/DEPLOYMENT_STRATEGY.md`](./docs/DEPLOYMENT_STRATEGY.md)
- [`docs/AI_INTEGRATION_STRATEGY.md`](./docs/AI_INTEGRATION_STRATEGY.md)
- [`docs/GPT_ACTION_SETUP.md`](./docs/GPT_ACTION_SETUP.md)
- [`docs/PRIVACY_AND_SECURITY_MODEL.md`](./docs/PRIVACY_AND_SECURITY_MODEL.md)
- [`docs/ROADMAP.md`](./docs/ROADMAP.md)

Operational and handoff docs:

- [`docs/PUBLIC_REPO_CHECKLIST.md`](./docs/PUBLIC_REPO_CHECKLIST.md)
- [`docs/PLANNING_BRIEF.md`](./docs/PLANNING_BRIEF.md)
- [`SECURITY.md`](./SECURITY.md)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Deploy on Render

The project includes a minimal [`render.yaml`](./render.yaml) for a first HTTPS deployment.

### Render setup

1. Create a new Web Service from this repository in Render.
2. Render should detect:
   - build command: `pip install -r requirements.txt`
   - start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables in Render:

```text
WHOOP_CLIENT_ID
WHOOP_CLIENT_SECRET
WHOOP_REDIRECT_URI
WHOOP_SCOPES
APP_BASE_URL
APP_API_KEY
```

### Recommended values

- `WHOOP_REDIRECT_URI`: your deployed callback URL, for example `https://your-service.onrender.com/auth/callback`
- `APP_BASE_URL`: your deployed base URL, for example `https://your-service.onrender.com`
- `APP_API_KEY`: a long random secret for protecting WHOOP-backed endpoints

Note:

- `/auth/login` stays open so a browser can begin the WHOOP OAuth flow
- `/whoop/*` endpoints remain protected by `APP_API_KEY`

### After deploy

Check:

```bash
curl https://YOUR_RENDER_DOMAIN/health
curl -H "X-API-Key: YOUR_APP_API_KEY" https://YOUR_RENDER_DOMAIN/whoop/context
curl https://YOUR_RENDER_DOMAIN/assistant/context
```

Required environment variables:

```env
WHOOP_CLIENT_ID=your_whoop_client_id
WHOOP_CLIENT_SECRET=your_whoop_client_secret
WHOOP_REDIRECT_URI=https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPO_NAME/callback/
WHOOP_SCOPES="offline read:profile read:recovery read:sleep read:workout"
APP_BASE_URL=http://localhost:8000
APP_API_KEY=replace_with_a_long_random_secret_for_private_endpoints
```

## Public Repo Safety

This repository is intended to become public, but runtime secrets and personal WHOOP data must remain private.

- Safe to publish: source code, docs, `.env.example`
- Never publish: `.env`, `data/whoop_tokens.json`, raw access tokens, refresh tokens, personal exports
- Use `APP_API_KEY` on any deployed environment that exposes WHOOP-backed endpoints
- Use `GET /assistant/context` for assistant integrations that need a reduced no-auth payload

See [`SECURITY.md`](./SECURITY.md) and [`docs/PRIVACY_AND_SECURITY_MODEL.md`](./docs/PRIVACY_AND_SECURITY_MODEL.md) for the full model.

## Product Direction

Near term:

- keep the backend stable and personal-first
- deploy a secure HTTPS version
- make the API assistant-ready

Later:

- enrich the AI context layer
- support friend-ready reuse
- evaluate a true multi-user architecture only after the single-user workflow is solid

# Privacy And Security Model

## Core Rule

This project is designed for public code and private data.

Everything in the repository should be safe to share publicly. Secrets, tokens, and personal WHOOP data must stay outside version control and outside public logs.

## Data Classification

### Public-Safe

- source code
- markdown documentation
- static helper pages
- `.env.example`
- deployment instructions that do not contain secrets

### Private Runtime Secrets

- WHOOP client credentials
- `APP_API_KEY`
- deployment provider secrets

### Private Personal Data

- WHOOP access tokens
- WHOOP refresh tokens
- live WHOOP profile, recovery, sleep, and workout data

## Repository Boundary

The repository should never become a storage location for:

- real credentials
- token files
- exported personal health data
- logs containing sensitive request data

This boundary is what makes a public repository possible.

## Current Security Model

Today the project uses a simple but appropriate model for a single-user service:

- secrets are loaded from environment variables
- tokens are stored outside git in `data/whoop_tokens.json`
- WHOOP-backed endpoints can be protected with `APP_API_KEY`
- `/auth/callback` remains open because WHOOP must redirect to it directly

## Authentication Posture

Current state:

- one trusted operator
- one shared application secret for private routes

This is acceptable for the current personal-first phase, but it is not the end-state for multi-user support.

## Logging And Diagnostics

Operational logs should help with uptime and debugging without capturing sensitive payloads.

Allowed:

- request path
- response status
- latency
- high-level error metadata

Not allowed:

- raw access tokens
- refresh tokens
- authorization headers
- full personal WHOOP payloads in logs

## Public Deployment Rules

Before any hosted deployment is treated as acceptable:

- `APP_API_KEY` must be enabled
- runtime secrets must be stored in the hosting provider, not in git
- health checks and logs must be reviewed for leakage risk
- public docs must remain generic and example-based

## Multi-User Security Direction

If the project becomes friend-ready or multi-user, the security model must evolve in a deliberate order:

1. per-user identity
2. per-user token isolation
3. stronger secret storage
4. clearer retention and deletion rules

The project should not claim multi-user readiness before those boundaries exist.

## Public Repository Readiness Standard

The repository is ready for public visibility only when an external observer can inspect every tracked file and learn nothing that would let them access the operator's WHOOP account or personal health data.

# Deployment Strategy

## Goal

Move from local-only use to a secure public HTTPS deployment that can support assistant access without weakening the privacy model.

## Deployment Philosophy

Deployment should make the existing single-user workflow reachable, not prematurely turn the project into a multi-user service.

That means:

- keep one trusted operator
- keep one WHOOP account
- keep secrets in host-managed environment variables
- keep the public surface narrow

## Environment Progression

### Stage 1: Local Development

Purpose:

- validate WHOOP OAuth
- inspect endpoint payloads
- develop the context contract

Characteristics:

- local `.env`
- local token file
- manual testing

### Stage 2: Private Hosted Deployment

Purpose:

- prove that the service runs cleanly over HTTPS
- validate environment variable handling and runtime behavior
- test remote access with API-key protection

Characteristics:

- one deployed backend
- secrets managed by the hosting provider
- no public browsing experience beyond necessary routes

### Stage 3: Assistant-Ready Hosted Deployment

Purpose:

- provide a stable API endpoint for assistant integration
- formalize schema expectations
- verify mobile-first usability

Characteristics:

- dependable HTTPS base URL
- stable auth story for AI access
- documented integration contract

## Host Requirements

The first deployment target should be chosen for simplicity and reliability, not for maximum scale.

Minimum requirements:

- HTTPS
- environment secret management
- predictable startup command
- simple logs and health checks
- low operational overhead for one operator

## Secret Handling

All secrets must live outside the repository:

- WHOOP client credentials
- `APP_API_KEY`
- any future deployment tokens

The deployed environment must never become a second place where personal data is accidentally published.

## API Exposure Rules

The deployed surface should stay intentionally small:

- `/health` may remain lightweight
- `/auth/callback` stays open because WHOOP redirects there directly
- WHOOP-backed routes should remain protected
- helper pages and docs should not expose secrets or user data

## Recommended Sequence

1. Finish public-repo hardening.
2. Choose one deployment platform and document its setup.
3. Deploy the existing backend without broadening scope.
4. Verify remote `health` and protected `whoop/context`.
5. Only then finalize the assistant integration path.

## What Not To Do Yet

- do not add multi-user complexity just to deploy
- do not widen public access to WHOOP endpoints
- do not couple deployment strategy to a future productization plan
- do not mix deployment hardening with unrelated backend refactors

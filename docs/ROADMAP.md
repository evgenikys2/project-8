# Roadmap

## Roadmap Logic

The roadmap prioritizes sequence over feature breadth. Each phase should reduce uncertainty for the next one.

## Phase 0: Working Personal Baseline

Status: completed

Outcomes:

- WHOOP OAuth works
- real data retrieval works
- token refresh works
- `GET /whoop/context` exists
- `APP_API_KEY` protection exists

Why it matters:

- the project has already proven the hardest product assumption: real WHOOP data can flow into an assistant-ready backend

## Phase 1: Public-Repo Hardening

Status: in progress

Objectives:

- make the repository safe to open publicly
- clean up documentation and strategy structure
- verify that secrets and personal data stay out of tracked files

Exit criteria:

- docs are coherent and public-safe
- security guidance is explicit
- public repo checklist can be passed without caveats

## Phase 2: Secure HTTPS Deployment

Status: next

Objectives:

- deploy the current single-user backend behind HTTPS
- move all runtime secrets to host-managed configuration
- validate remote health and authenticated WHOOP context access

Exit criteria:

- one stable hosted environment exists
- health checks are reliable
- `whoop/context` is reachable with authentication

## Phase 3: Assistant Integration

Status: next

Objectives:

- formalize the API contract for assistant use
- make the assistant fetch WHOOP context before advice
- validate the mobile-first workflow

Exit criteria:

- the assistant can consistently use fresh WHOOP context
- the owner can use the flow in routine daily use

## Phase 4: Context Enrichment

Status: planned

Objectives:

- improve answer quality with derived metrics and clearer summaries
- reduce prompt-time reasoning burden on the model

Candidate additions:

- recovery trend
- recent training load
- sleep debt or sleep consistency indicators
- today-readiness summary

Exit criteria:

- derived fields noticeably improve answer usefulness without making the API contract unstable

## Phase 5: Friend-Ready Reuse

Status: later

Objectives:

- let another person deploy or run the project safely with their own WHOOP account
- separate reusable open-source value from the original operator's private setup

Requirements:

- better onboarding docs
- stronger token isolation model
- clearer host and secret management guidance

Exit criteria:

- another trusted person can use the project without access to the original user's data

## Phase 6: Multi-User Product Evaluation

Status: optional

Objectives:

- decide whether the project should remain a strong personal tool or evolve into a broader product

Decision triggers:

- repeated friend-ready demand
- need for shared hosting
- need for user-level identity and account boundaries

This phase is intentionally deferred. It should begin only after the single-user path is genuinely smooth.

## Current Strategic Priority

The immediate priority is Phase 2 readiness: choose and document the first secure deployment path that preserves the current privacy model and enables the later assistant integration.

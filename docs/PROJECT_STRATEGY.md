# Project Strategy

## One-Sentence Vision

Make WHOOP data reliably available to an AI assistant so day-to-day health, recovery, training, and nutrition guidance can be grounded in real personal context.

## Project Snapshot

WHOOP AI Assistant is already past the prototype stage in one important sense: the backend works, OAuth works, token refresh works, and the project can already retrieve real data from WHOOP.

The strategic gap is not "can the API talk to WHOOP?" The gap is turning that working backend into a durable product path:

- safe to keep in a public repository
- useful from an AI assistant, ideally on mobile
- personal-first today
- reusable by friends later

## Problem Statement

Generic AI health advice is often too detached from the user's current physiological state. WHOOP provides meaningful recovery, sleep, and workout signals, but those signals are not yet flowing into a lightweight assistant workflow that is easy to use every day.

This project solves that by creating a small, secure context service that translates WHOOP data into an AI-ready interface.

## Product Strategy

### Primary Product Thesis

The product is not a dashboard. The product is a context layer for AI.

That means the most important output is not raw WHOOP payloads alone. The most important output is a stable, trusted context surface that an assistant can fetch before answering questions such as:

- Should I train hard today?
- How recovered am I compared with recent days?
- How should I think about nutrition or rest today?
- What matters most from my latest WHOOP data?

### Target User Progression

Current mode:

- one owner
- one WHOOP account
- personal daily use
- tolerance for some manual setup

Next mode:

- one owner
- public HTTPS deployment
- an AI assistant as the main consumption surface

Later mode:

- friend-ready reuse
- each person brings their own WHOOP credentials
- clean isolation between users

### Strategic Principles

1. Public code, private data.
   Code, docs, and examples can be open. Secrets, tokens, and personal health data cannot.
2. Personal-first before platform.
   The single-user experience should be excellent before any multi-user generalization.
3. One strong context endpoint beats many weak endpoints.
   `GET /whoop/context` should remain the main AI entry point.
4. Mobile usage is a real product requirement.
   The ideal flow must work from a phone-based assistant experience, not only from local scripts.
5. Sequencing matters more than feature count.
   Secure deployment and clean integration come before context enrichment and product polish.

## Strategy Stack

The strategy is intentionally split into clear layers:

- product strategy: define the project as an AI context layer, not a general dashboard
- technical strategy: keep the API narrow, stable, and context-first
- deployment strategy: move from local use to secure HTTPS without overbuilding
- AI integration strategy: make context retrieval a default step before meaningful advice
- privacy and security strategy: keep the repository public-safe while runtime data stays private
- expansion strategy: defer friend-ready and multi-user complexity until the single-user path is strong

## What This Project Is

- a secure WHOOP-backed API
- a compact health context source for AI
- a personal-first system designed for daily use
- an open-source-ready codebase with private runtime data

## What This Project Is Not Yet

- a multi-user SaaS
- a consumer health app with full onboarding
- a replacement for clinical guidance
- a broad analytics platform

## Success Criteria

### Near-Term Success

- repository is public-safe
- backend is reachable over HTTPS
- the assistant can fetch WHOOP context through a stable API contract
- the owner can use the system routinely from a mobile-first assistant experience

### Mid-Term Success

- context quality improves beyond raw payload delivery
- the docs are strong enough for an external developer to understand the product direction quickly
- deployment and operation remain low-friction for a single user

### Later Success

- another person can run the system without access to the original user's data
- multi-user design, if pursued, does not require rethinking the privacy model from scratch

## Strategic Decisions Already Made

- FastAPI is sufficient for the current backend scope.
- WHOOP remains the only upstream source for now.
- `APP_API_KEY` is the minimum acceptable protection for public exposure of private endpoints.
- The repository should optimize for eventual public visibility.
- The project should avoid mixing strategic documentation with active backend changes.

## Strategic Decisions Still Open

- which deployment target becomes the primary hosted path
- how narrow or broad the first assistant integration should be
- when to introduce derived metrics beyond the current context summary
- when friend-ready reuse becomes important enough to justify multi-user architecture work

## Document Map

- [`TECHNICAL_STRATEGY.md`](./TECHNICAL_STRATEGY.md)
- [`DEPLOYMENT_STRATEGY.md`](./DEPLOYMENT_STRATEGY.md)
- [`AI_INTEGRATION_STRATEGY.md`](./AI_INTEGRATION_STRATEGY.md)
- [`PRIVACY_AND_SECURITY_MODEL.md`](./PRIVACY_AND_SECURITY_MODEL.md)
- [`ROADMAP.md`](./ROADMAP.md)
- [`PUBLIC_REPO_CHECKLIST.md`](./PUBLIC_REPO_CHECKLIST.md)

This document is the top-level strategy source of truth. Detailed execution and risk boundaries live in the supporting documents above.

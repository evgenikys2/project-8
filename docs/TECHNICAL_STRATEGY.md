# Technical Strategy

## Purpose

The technical strategy is to keep the system small, understandable, and reliable while making it increasingly useful for AI consumption.

## Current Technical Baseline

The current backend already provides:

- WHOOP OAuth authorization
- token exchange and refresh
- token persistence in a local file store
- FastAPI endpoints for profile, recovery, sleep, workouts, and context
- API-key protection for WHOOP-backed endpoints

This is a strong base for a personal-first product. The strategy should preserve that simplicity.

## Core Technical Principle

Favor a narrow, stable interface over a broad but fragile platform.

That principle drives several choices:

- keep `GET /whoop/context` as the main AI-facing endpoint
- use raw endpoints as supporting surfaces, not the primary assistant contract
- avoid premature infrastructure layers while the project is still single-user

## Architecture Direction

### Layer 1: WHOOP Ingestion

Responsibilities:

- OAuth
- token refresh
- upstream WHOOP API calls
- normalization of raw WHOOP responses

### Layer 2: Context Aggregation

Responsibilities:

- fetch the latest profile, recovery, sleep, and workouts
- produce a compact, AI-friendly response shape
- gradually add derived fields that reduce reasoning overhead for the model

### Layer 3: Secure API Exposure

Responsibilities:

- expose a stable HTTPS API
- enforce request authentication
- protect logs, secrets, and personal data
- provide a predictable schema for AI integrations

### Layer 4: Future User Isolation

Responsibilities for a later phase:

- per-user tokens
- per-user storage boundaries
- stronger identity and session handling

## API Strategy

### Primary Endpoint

`GET /whoop/context` should remain the default entry point for AI usage because it reduces orchestration complexity and encourages a stable prompt pattern.

### Supporting Endpoints

`/whoop/profile`, `/whoop/recovery`, `/whoop/sleep`, and `/whoop/workouts` should continue to exist for debugging, inspection, and future advanced integrations.

### Schema Direction

The API should move toward:

- explicit field naming
- stable summary fields
- minimal ambiguity around timestamps and recency
- versionable behavior if the response shape becomes richer later

## Data Strategy

The system should distinguish between three classes of data:

1. public repository data
2. private runtime secrets
3. private personal WHOOP data

Technical design should keep those boundaries obvious at all times.

Near term:

- keep secrets in environment variables
- keep tokens out of git
- avoid storing unnecessary WHOOP history locally

Later:

- use per-user encrypted token storage if multi-user support is introduced
- define retention and deletion rules before broadening persistence

## Observability Strategy

Observability should support debugging without leaking sensitive data.

- log request paths, statuses, and latency
- avoid raw token logging
- avoid raw authorization headers
- avoid persisting personal WHOOP payloads in logs

## Reliability Strategy

The service should behave predictably under normal upstream failures.

- pass through clear error context from WHOOP where safe
- surface rate-limit conditions explicitly
- keep the health endpoint simple and informative
- avoid hidden background complexity unless it clearly improves reliability

## Friend-Ready Technical Direction

The friend-ready path should reuse the current architecture in stages instead of replacing it all at once.

Expected additions later:

- identity layer
- per-user token vault
- stronger deployment secrets management
- onboarding flow that does not depend on the project owner's machine

The current strategy does not require implementing any of that yet.

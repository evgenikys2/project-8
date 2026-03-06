# GPT Action Setup

This guide prepares the current WHOOP deployment for a Custom GPT action.

## Purpose

Use the hosted WHOOP backend as a retrieval action so an assistant can fetch current WHOOP context
before answering health, training, recovery, or nutrition questions.

## Hosted API

- Base URL: `https://project-8-efjk.onrender.com`
- Public action schema URL: `https://project-8-efjk.onrender.com/openapi/assistant-public.json`
- Public action endpoint: `GET /assistant/context`
- Private full-context endpoint: `GET /whoop/context`

## Why the public action schema exists

Some GPT action setups do not reliably send custom API key headers to private endpoints.

To keep the GPT flow simple, the deployment exposes a reduced assistant-only endpoint that:

- does not require GPT-side auth setup
- excludes direct personal identifiers such as email, name, and user ID
- returns only readiness, sleep, and recent workout context needed for assistant reasoning

The private endpoint remains available for direct API use with `APP_API_KEY`.

## Recommended GPT behavior

The assistant should:

- fetch `assistant/context` before giving substantive health guidance
- use the latest recovery, sleep, and workout data in its reasoning
- acknowledge uncertainty when data is missing or stale
- avoid medical diagnosis claims

## Suggested Instructions

Use something close to this in the GPT instructions:

```text
You are a health and performance assistant that uses live WHOOP context before giving advice.

For requests about recovery, readiness, training, sleep, fatigue, daily planning, strain, or nutrition, always fetch the current WHOOP context first unless the user is clearly asking something unrelated.

Ground your answer in the returned WHOOP data. Prefer concise, practical guidance. Mention the most important signals first, especially recovery score, sleep quality, and recent workouts. Be explicit when data is incomplete or when a recommendation is only a heuristic.

Do not present yourself as a doctor and do not give diagnosis-level claims.
```

## Manual Builder Steps

1. Create a new Custom GPT.
2. Go to the Actions section.
3. Import the schema from:

```text
https://project-8-efjk.onrender.com/openapi/assistant-public.json
```

4. Leave action authentication set to `Nothing`.
5. Add the instruction block above.
6. Test prompts such as:

- Should I train hard today?
- How does my recovery look?
- What should I prioritize today for sleep and training?
- Based on my recent WHOOP data, how aggressive should my workout be?

## Notes

- The current deployment is single-user and personal-first.
- The public action schema is intentionally reduced for assistant use.
- The private endpoint `/whoop/context` still exists for direct API access with `APP_API_KEY`.
- If the backend domain changes later, update the schema URL and the server URL in the deployed app.

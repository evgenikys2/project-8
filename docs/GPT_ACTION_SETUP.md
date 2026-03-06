# GPT Action Setup

This guide prepares the current WHOOP deployment for a Custom GPT action.

## Purpose

Use the hosted WHOOP backend as a retrieval action so an assistant can fetch current WHOOP context
 before answering health, training, recovery, or nutrition questions.

## Hosted API

- Base URL: `https://project-8-efjk.onrender.com`
- OpenAPI schema URL: `https://project-8-efjk.onrender.com/openapi/assistant.json`
- Main action endpoint: `GET /whoop/context`

## Authentication

The action schema uses an API key in the query string:

- parameter name: `api_key`
- value: your `APP_API_KEY`

This was chosen because OpenAI's production notes for actions say custom headers are not supported.

## Recommended GPT behavior

The assistant should:

- fetch `whoop/context` before giving substantive health guidance
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
https://project-8-efjk.onrender.com/openapi/assistant.json
```

4. Configure the action to use your API key value for the schema's `api_key` requirement.
5. Add the instruction block above.
6. Test prompts such as:

- Should I train hard today?
- How does my recovery look?
- What should I prioritize today for sleep and training?
- Based on my recent WHOOP data, how aggressive should my workout be?

## Notes

- The current deployment is single-user and personal-first.
- The action retrieves the owner's WHOOP context, not multi-user data.
- If the backend domain changes later, update the schema URL and the server URL in the deployed app.

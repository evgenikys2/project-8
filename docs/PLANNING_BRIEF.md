# Planning Brief

Use the text below to start a new planning or implementation session for this repository.

```text
We are working on "WHOOP AI Assistant".

Project goal:
- connect WHOOP data to an AI assistant workflow
- make an AI assistant the main user surface, ideally including mobile use
- keep the repository public-safe while keeping secrets and personal data private

Current state:
- WHOOP OAuth is working
- real personal WHOOP data is already flowing
- the backend is FastAPI
- endpoints exist for profile, recovery, sleep, workouts, and whoop/context
- whoop/context is the main AI-ready endpoint
- APP_API_KEY protection exists for private WHOOP-backed routes
- the project is single-user and personal-first today

Strategic direction:
- first make the single-user assistant workflow reliable
- then harden public deployment and documentation
- only later consider friend-ready reuse or multi-user architecture

Important constraints:
- do not expose secrets, tokens, or personal data
- do not mix strategy/documentation work with unrelated backend refactors
- preserve the public-code/private-data boundary

Start with these documents:
- README.md
- docs/README.md
- docs/PROJECT_STRATEGY.md
- docs/ROADMAP.md
- docs/PRIVACY_AND_SECURITY_MODEL.md
- SECURITY.md

Work in a way that improves clarity, sequencing, and public-repo readiness.
```

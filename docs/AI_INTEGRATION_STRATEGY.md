# AI Integration Strategy

## Product Outcome

The ideal experience is simple:

1. the user opens the assistant
2. the assistant fetches fresh WHOOP context
3. the response uses that context to answer recovery, training, sleep, or nutrition questions

The long-term target is regular mobile use, not only desktop experimentation.

## Integration Principle

The assistant should fetch context first and reason second.

That is the core behavioral rule for any assistant integration path.

## Recommended Integration Shape

Use a narrow API contract centered on `GET /whoop/context`, supported by raw endpoints only when deeper inspection is needed.

This keeps the model behavior easier to control:

- one main call for most user questions
- less prompt complexity
- fewer failure modes in mobile usage

## Why This Matters

Without a defined strategy, an AI assistant will either:

- answer too generically
- rely on stale assumptions
- or require too many manual steps before each useful answer

The integration strategy exists to eliminate that gap.

## What The Assistant Should Be Good At

- training-readiness requests
- recovery-aware summaries
- sleep-informed guidance
- lightweight workout reflection
- context-grounded daily planning

## What The Assistant Should Avoid

- pretending to provide medical diagnosis
- over-claiming precision when data is incomplete
- answering without fresh context when the workflow expects a live fetch

## Integration Requirements

The backend contract should be:

- reachable over HTTPS
- authenticated
- schema-stable
- fast enough for normal interactive use

The assistant side should be:

- instructed to fetch WHOOP context before substantive advice
- explicit about uncertainty and limitations
- optimized for short, actionable mobile-friendly answers

## Rollout Sequence

### Phase 1

Make the backend deployment stable and publicly reachable with proper auth.

### Phase 2

Define the action-style API contract and test that the assistant can consistently fetch context.

### Phase 3

Tune instructions so the assistant uses WHOOP context well for everyday questions.

### Phase 4

Add richer derived fields only if they improve answer quality without making the API harder to maintain.

## Friend-Ready Implication

The first assistant integration can remain single-user. The friend-ready version should only arrive once there is a clear way to map each session to the correct user's WHOOP credentials and data boundary.

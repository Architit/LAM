# Repo Rollout Analysis Contract (RADRILONIUMA Ecosystem)

## Purpose
This contract defines the required output when the user requests:
- repository map / rollout status,
- phase rollout plan across repos/agents,
- ecosystem status dashboard.

This is **policy-only**: contracts-first, observability-first, derivation-only.
No automation, no runtime logic, no enforcement.

## Inputs (facts only)
Statuses MUST be derived from repo facts:
- git state (branch/HEAD/tags),
- presence of required governance artifacts,
- tests / smoke-tests results,
- referenced ROADMAP / DEV_LOGS entries (if present).

No assumptions, no speculation.

## Required Output
The agent MUST produce:

1) A table of repositories/agents with statuses:
- DONE / PENDING / BLOCKED
- short factual justification per row (1 line)

2) A phase rollout plan:
- ordered steps per phase/subphase,
- DoD (Definition of Done) per step,
- dependencies and blockers (facts only).

## Status Rules
- DONE: DoD satisfied and verifiable (tags/commits/docs/tests).
- PENDING: work not completed, but no blocker identified.
- BLOCKED: explicit blocker present (missing artifact, failing tests, missing access, unresolved conflicts).

## Non-goals
This contract MUST NOT:
- introduce scripts/CI rules,
- modify runtime code paths,
- fabricate statuses without evidence.

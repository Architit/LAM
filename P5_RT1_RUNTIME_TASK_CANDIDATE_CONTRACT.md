# P5.RT1 Runtime Task Candidate Contract (LAM)

## Purpose
Define governance-only candidate scope for the first runtime-facing Phase 5 task.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Candidate
- `task_id`: `P5.RT1`
- `task_name`: Runtime-facing task candidate definition
- `status`: DONE (governance-only)

## Candidate scope
- Fix candidate objective and explicit boundaries for first runtime-facing execution item.
- Define required evidence shape before any runtime action can be proposed.
- Define non-goals and out-of-scope runtime operations.

## Required record fields
- `candidate_id`
- `candidate_objective`
- `in_scope`
- `out_of_scope`
- `required_evidence`
- `risk_note`
- `boundary_note`
- `next_target`
- `timestamp_utc`

## Non-goals
- No runtime start command.
- No scheduler/job wiring.
- No automatic execution approval.

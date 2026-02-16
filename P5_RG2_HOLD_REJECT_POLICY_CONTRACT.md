# P5.RG2 Hold/Reject Decision Policy Contract (LAM)

## Purpose
Define governance-only decision policy for `hold` and `reject_scope` outcomes in runtime-facing Phase 5 gating.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Decision outcomes
- `allow_start`
- `hold`
- `reject_scope`

## Policy rules (governance-only)
1. `hold` is used when:
- eligibility is incomplete but remediable
- evidence is partial or requires clarification
- risk state is `needs_review`

2. `reject_scope` is used when:
- scope contradicts governance boundaries
- risk state is `blocked` or boundary is explicitly violated
- task intent is misaligned with declared phase/gate objective

3. `allow_start` is used only when:
- eligibility matrix is complete and acceptable
- no blocked boundary conditions exist

## Mandatory record fields
- `decision_id`
- `task_id`
- `decision_outcome`
- `decision_basis`
- `remediation_note` (required for `hold`)
- `rejection_reason` (required for `reject_scope`)
- `timestamp_utc`

## Non-goals
- No runtime task scheduler integration.
- No automatic policy enforcement.
- No CI behavior changes.

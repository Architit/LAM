# P5.RG3 Start-Approval Evidence Contract (LAM)

## Purpose
Define governance-only minimal evidence record required before starting the first runtime-facing Phase 5 task.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Required evidence blocks
1. Eligibility block
- Link to RG1 matrix record and resolved decision values.

2. Decision block
- Link to RG2 decision policy outcome (`allow_start` | `hold` | `reject_scope`).

3. Risk block
- Risk register references and current risk class summary.

4. Boundary block
- Explicit `no-runtime-change` for governance-only artifacts and scope boundary for runtime-facing start task.

## Minimal record fields
- `approval_id`
- `task_id`
- `eligibility_ref`
- `decision_ref`
- `risk_ref`
- `boundary_note`
- `approval_outcome`: `approved` | `deferred` | `rejected`
- `approver_scope`
- `timestamp_utc`

## Non-goals
- No runtime launcher.
- No automated approval workflow.
- No permission or identity automation.

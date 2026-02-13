# P5.RT3 Runtime Start Decision Record Contract (LAM)

## Purpose
Define governance-only final record format for runtime-facing start decision after RT1/RT2 closure.

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

## Required evidence references
- RT candidate reference: `P5_RT1_RUNTIME_TASK_CANDIDATE_CONTRACT.md`
- RT preflight reference: `P5_RT2_RUNTIME_PREFLIGHT_CHECKLIST_CONTRACT.md`
- Gate decision references:
  - `P5_RG1_ELIGIBILITY_MATRIX_CONTRACT.md`
  - `P5_RG2_HOLD_REJECT_POLICY_CONTRACT.md`
  - `P5_RG3_START_APPROVAL_EVIDENCE_CONTRACT.md`

## Required record fields
- `decision_id`
- `task_id`
- `decision_outcome`
- `decision_rationale`
- `evidence_refs`
- `risk_boundary_note`
- `operator_ack`
- `next_phase_note`
- `timestamp_utc`

## Non-goals
- No runtime start trigger.
- No workflow automation.
- No scheduler or launcher coupling.

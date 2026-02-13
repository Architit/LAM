# P5.RT2 Runtime Preflight Checklist Contract (LAM)

## Purpose
Define governance-only preflight checklist for the first runtime-facing Phase 5 start candidate.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Checklist scope
- Validate required artifacts exist before runtime-facing start decision.
- Validate evidence links are explicit and traceable.
- Validate boundary/risk notes are present and non-contradictory.

## Required preflight checks (read-only)
1. Contract presence check
- `P5_RUNTIME_TASK_WAVE_CONTRACT.md`
- `P5_RT1_RUNTIME_TASK_CANDIDATE_CONTRACT.md`
- `P5_RT2_RUNTIME_PREFLIGHT_CHECKLIST_CONTRACT.md`

2. Decision-wave dependency check
- `P5_RUNTIME_FACING_GATE_DECISION_CONTRACT.md`
- `P5_RG1_ELIGIBILITY_MATRIX_CONTRACT.md`
- `P5_RG2_HOLD_REJECT_POLICY_CONTRACT.md`
- `P5_RG3_START_APPROVAL_EVIDENCE_CONTRACT.md`

3. Snapshot and map alignment check
- `DEV_MAP.md`, `ROADMAP.md`, `DEV_LOGS.md`
- `WORKFLOW_SNAPSHOT_STATE.md`, `NEW_CHAT_INIT_MESSAGE`

## Required record fields
- `preflight_id`
- `task_id`
- `checks_passed`
- `checks_pending`
- `risk_boundary_note`
- `next_target`
- `timestamp_utc`

## Non-goals
- No runtime execution command.
- No launcher/integration wiring.
- No automatic promotion to start.

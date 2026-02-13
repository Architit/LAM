# P5.G3 Operator Checklist Contract (LAM)

## Purpose
Define governance-only operator decision checklist required before starting any runtime-facing Phase 5 task.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Operator checklist (governance-only)
1. Scope check
- Confirm the task is explicitly marked as `runtime-facing` or `governance-only`.

2. Boundary check
- Confirm `no-runtime-change` marker exists for governance-only tasks.
- Confirm closed-state references (`P2.4`, `P4 follow-up`, `P5 prep`) are not contradicted.

3. Evidence check
- Confirm required evidence fields from `P5_G1_EVIDENCE_PROFILE_CONTRACT.md` are mapped for the task.

4. Risk check
- Confirm risk entries are classified per `P5_G2_RISK_BOUNDARY_REGISTER_CONTRACT.md`.
- Confirm `RISK-HIGH/CRITICAL` entries are reflected in `DEV_LOGS.md`.

5. Start decision
- Decision values: `allow_start` | `hold_for_clarification` | `reject_scope`
- Decision note is mandatory and must be UTC timestamped.

## Non-goals
- No runtime enforcement hooks.
- No automated gate execution.
- No CI/pipeline behavior changes.

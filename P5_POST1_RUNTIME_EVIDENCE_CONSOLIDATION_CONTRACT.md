# P5.POST1 Runtime Evidence Consolidation Contract (LAM)

## Purpose
Define governance-only consolidation record for runtime-facing evidence gathered in P5 RT wave.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Consolidation scope
- Consolidate references from:
  - `P5_RT1_RUNTIME_TASK_CANDIDATE_CONTRACT.md`
  - `P5_RT2_RUNTIME_PREFLIGHT_CHECKLIST_CONTRACT.md`
  - `P5_RT3_RUNTIME_START_DECISION_RECORD_CONTRACT.md`
- Normalize evidence block format for follow-up governance review.

## Required evidence blocks
1. `candidate_evidence_ref`
2. `preflight_evidence_ref`
3. `start_decision_ref`
4. `risk_boundary_ref`
5. `consistency_note`

## Required record fields
- `consolidation_id`
- `task_id`
- `evidence_refs`
- `coverage_status`
- `open_items`
- `next_target`
- `timestamp_utc`

## Non-goals
- No runtime execution.
- No workflow automation.
- No change to execution path.

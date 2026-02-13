# P6.T3 Operator Action Boundary Checklist Contract (LAM)

## Purpose
Define governance-only checklist for operator action boundaries in Phase 6 prep.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Checklist scope
- Confirm read-only boundaries for control plane views.
- Confirm forbidden live-control actions in prep stage.
- Confirm auditability requirements for future action proposals.

## Required checklist blocks
1. `read_only_actions`
2. `forbidden_actions`
3. `evidence_capture_requirements`
4. `risk_boundary_requirements`
5. `approval_gate_note`

## Required record fields
- `checklist_id`
- `task_id`
- `boundary_checks`
- `exceptions`
- `next_target`
- `timestamp_utc`

## Non-goals
- No operator command execution.
- No runtime state mutation.
- No direct integration with runtime controls.

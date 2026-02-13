# P6.T1 Control Plane Surface Inventory Contract (LAM)

## Purpose
Define governance-only inventory contract for Phase 6 control plane operator surfaces.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Inventory scope
- Operator surface categories:
  - agent state/health views
  - provider health/cost views
  - log/trace filter views
  - profile switch and policy-state views

## Required inventory blocks
1. `surface_id`
2. `surface_goal`
3. `data_inputs` (read-only sources)
4. `visibility_scope`
5. `boundary_note`

## Required record fields
- `inventory_id`
- `task_id`
- `surfaces_catalog`
- `coverage_note`
- `open_gaps`
- `next_target`
- `timestamp_utc`

## Non-goals
- No UI runtime implementation.
- No live control actions.
- No execution path changes.

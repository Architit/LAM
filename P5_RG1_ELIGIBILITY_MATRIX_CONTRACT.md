# P5.RG1 Eligibility Matrix Contract (LAM)

## Purpose
Define governance-only eligibility matrix for runtime-facing Phase 5 task starts.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Eligibility dimensions
- `scope_ready`: `yes` | `no`
- `evidence_ready`: `yes` | `partial` | `no`
- `risk_state`: `acceptable` | `needs_review` | `blocked`
- `boundary_clear`: `yes` | `no`

## Decision matrix (governance-only)
- `allow_start` if:
  - `scope_ready=yes`
  - `evidence_ready=yes`
  - `risk_state=acceptable`
  - `boundary_clear=yes`

- `hold` if:
  - any dimension is `partial` or `needs_review`
  - and no dimension is `blocked`/`no` on boundary

- `reject_scope` if:
  - `boundary_clear=no` or `risk_state=blocked`

## Record fields
- `task_id`
- `eligibility_decision`: `allow_start` | `hold` | `reject_scope`
- `matrix_snapshot` (all dimension values)
- `decision_note`
- `timestamp_utc`

## Non-goals
- No runtime gate enforcement.
- No automatic decision engine.
- No scheduler or workflow automation.

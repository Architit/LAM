# Z.RUNTIME.T3 Start Decision Record Contract (LAM)

## Purpose
Define decision record shape for `Z.RUNTIME.T1` start approval/rejection.

Hard constraints:
- governance-only
- derivation-only
- no runtime logic
- no execution-path impact

## Decision fields
- `decision_id`
- `task_wave_id` (`z.runtime.t1`)
- `decision` (`approved` | `rejected` | `hold`)
- `reason`
- `evidence_refs`
- `operator`
- `timestamp_utc`
- `next_target`

## Decision boundary
- `approved` requires full preflight PASS and explicit user gate.
- `hold/rejected` requires residual risk and remediation notes.

## Outcome
- Deterministic start decision template is fixed for runtime-facing wave governance.

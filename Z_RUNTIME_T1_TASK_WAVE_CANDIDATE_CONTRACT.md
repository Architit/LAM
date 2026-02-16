# Z.RUNTIME.T1 Task Wave Candidate Contract (LAM)

## Purpose
Define the first runtime-facing Z task wave candidate at governance level only.

Hard constraints:
- governance-only
- derivation-only
- no runtime logic
- no execution-path impact

## Candidate scope
- Candidate id: `z.runtime.t1`
- Focus: bounded runtime-facing activation plan for Agent SDK backend path under explicit user gate.
- Scope type: preparation-to-execution boundary definition only.

## Non-goals
- no provider routing changes
- no live backend switching
- no CI/runtime enforcement toggles

## Entry criteria
1. `Z.RUNTIME.PREP` is CLOSED.
2. Risk register is available and referenced.
3. Ops preflight checklist is available and referenced.
4. Explicit user approval for T1 wave start is captured.

## Evidence refs
- `risk_ref`: `Z_RUNTIME_RISK_BOUNDARY_REGISTER_CONTRACT.md`
- `ops_ref`: `Z_RUNTIME_OPS_PREFLIGHT_CHECKLIST_CONTRACT.md`
- `snapshot_ref`: `WORKFLOW_SNAPSHOT_STATE.md`
- `approval_ref`: user gate `+++` recorded in session/logs

## Outcome
- Runtime-facing wave candidate is formally defined and ready for preflight validation.

# Z.RUNTIME Execution Wave Contract (LAM)

## Purpose
Open the first runtime execution wave under explicit approval, with strict execution-path guardrails and rollback plan.

## Status
- Package: `Z.RUNTIME.EXEC.W1`
- State: OPEN (execution-approved boundary)
- Decision prerequisite: `Z_RUNTIME_START_DECISION_RECORD.md` with `approved`

## Guardrails (mandatory)
1. Scope-limited execution only (no broad refactors).
2. One change-wave at a time; each wave must be reversible.
3. Runtime-facing changes require evidence after each step.
4. Any failed preflight or smoke check => immediate HOLD.

## Execution-path boundaries
- Allowed:
  - additive, bounded runtime hooks defined by wave tasks
  - observability evidence updates
- Forbidden:
  - implicit provider-chain changes outside approved wave scope
  - silent contract-schema breaking changes
  - concurrent multi-wave runtime mutations

## Rollback plan
- R1: stop wave, keep branch state and capture failure evidence.
- R2: revert only wave commits (no destructive reset).
- R3: publish rollback note in `DEV_LOGS.md` + update `ROADMAP.md`/`DEV_MAP.md`.
- R4: return to user-gated selection state.

## Wave queue (initial)
1. EXEC.W1.T1 - minimal runtime hook enablement (bounded)
2. EXEC.W1.T2 - smoke/observability verification
3. EXEC.W1.T3 - post-wave decision record (continue/hold)

## Evidence references
- `start_decision_ref`: `Z_RUNTIME_START_DECISION_RECORD.md`
- `preflight_ref`: `Z_RUNTIME_T2_PREFLIGHT_VALIDATION_CONTRACT.md`
- `risk_ref`: `Z_RUNTIME_RISK_BOUNDARY_REGISTER_CONTRACT.md`
- `snapshot_ref`: `WORKFLOW_SNAPSHOT_STATE.md`

## Non-goals
- no ecosystem-wide rollout in this wave
- no protocol rewrite
- no bypass of explicit user gate for next wave

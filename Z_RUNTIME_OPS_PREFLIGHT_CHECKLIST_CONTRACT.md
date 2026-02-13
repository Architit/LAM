# Z.RUNTIME Ops Preflight Checklist Contract (LAM)

## Purpose
Define operator-first preflight checklist for runtime-facing Z package selection.

Hard constraints:
- governance-only
- derivation-only
- no runtime logic
- no execution-path impact

## Preflight checklist blocks
1. branch_state_check (`git status --short` clean)
2. docs_order_check (`DEV_LOGS -> ROADMAP -> DEV_MAP -> WORKFLOW_SNAPSHOT_STATE`)
3. mirror_alignment_check (`LAM/default/*` reflects root changes)
4. evidence_link_check (risk/ops/asr refs present)
5. explicit_user_gate_check (numbered selection captured)

## Required records
- `checklist_id`
- `operator`
- `timestamp_utc`
- `check_results`
- `residual_risks`
- `next_target`

## Outcome
- Deterministic preflight boundary is fixed before any runtime-facing Z package activation.

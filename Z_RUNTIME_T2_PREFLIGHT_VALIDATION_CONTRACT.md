# Z.RUNTIME.T2 Preflight Validation Contract (LAM)

## Purpose
Define preflight validation for `Z.RUNTIME.T1` candidate before any start decision.

Hard constraints:
- governance-only
- derivation-only
- no runtime logic
- no execution-path impact

## Validation checklist
1. candidate_contract_present
2. risk_controls_complete
3. ops_checklist_complete
4. mirror_alignment_pass
5. asr_traceability_present
6. explicit_user_gate_present

## Hold/Reject rules
- HOLD if any checklist item is missing evidence.
- REJECT if any proposed step changes runtime behavior without separate approved execution package.

## Rollback note
- On HOLD/REJECT: keep phase pointer unchanged and return to user-gated selection state.

## Outcome
- Preflight validation boundary is fixed and auditable for start decision stage.

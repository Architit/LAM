# Z.RUNTIME Risk Boundary Register Contract (LAM)

## Purpose
Define facts-only risk boundaries for first runtime-facing Z package selection.

Hard constraints:
- governance-only
- derivation-only
- no runtime logic
- no execution-path impact

## Required risk blocks
1. interface_regression_risk
2. provider_path_instability_risk
3. observability_gap_risk
4. rollback_gap_risk
5. operator_misfire_risk

## Required control fields
- `risk_id`
- `impact_scope`
- `detection_signal`
- `control_action`
- `hold_reject_rule`
- `evidence_ref`

## Hold/Reject policy (facts-only)
- HOLD if any mandatory evidence field is missing.
- REJECT if change implies runtime logic without explicit package approval.

## Outcome
- Risk boundary is fixed for first runtime-facing Z selection cycle.

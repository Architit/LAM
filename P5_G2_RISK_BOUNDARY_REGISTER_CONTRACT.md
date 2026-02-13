# P5.G2 Risk Boundary Register Contract (LAM)

## Purpose
Define governance-only risk boundary register for phase5 memory/retrieval changes.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Risk classes
- `RISK-LOW`: documentation inconsistency or missing metadata
- `RISK-MEDIUM`: boundary ambiguity that may cause operator misalignment
- `RISK-HIGH`: governance contradiction affecting phase pointer or closure claims
- `RISK-CRITICAL`: risk claim that could be interpreted as runtime behavior/enforcement

## Register fields
- `risk_id`
- `risk_class`
- `risk_scope`
- `risk_trigger`
- `impact_note`
- `mitigation_note` (governance-only)
- `owner_scope`
- `status`: `open` | `mitigated` | `accepted`
- `timestamp_utc`

## Escalation notes
- `RISK-HIGH` and `RISK-CRITICAL` require explicit entry in `DEV_LOGS.md` before next task start.
- Any risk touching runtime semantics must include explicit `no-runtime-change` marker.
- No automatic remediation or enforcement is introduced by this contract.

## Non-goals
- No runtime risk engine.
- No blocker automation.
- No CI gate mutation.

# P4 Follow-up F1 Contract (Cost-Aware Routing, Governance-Only)

## Purpose
Define cost-aware routing contract boundaries and evidence format without changing runtime behavior.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This step defines contract fields and evidence templates only.

## Cost-Aware Contract Draft

### A) Cost budget fields (contract level)
- `cost_budget_usd_max` (float, optional): maximum allowed projected request cost.
- `cost_mode` (enum): `strict|prefer_low_cost|advisory`.
- `cost_source` (enum): `provider_table|historical_avg|manual`.
- `cost_decision` (enum): `accept|defer|fallback|reject`.

### B) Evidence fields (governance logs/contracts)
- `provider_candidate`
- `estimated_cost_usd`
- `budget_usd_max`
- `cost_mode`
- `cost_decision`
- `reason_code`
- `timestamp_utc`

### C) Boundary rules
- Cost-aware rules are declarative in this phase.
- No provider order change is applied by this contract alone.
- No enforcement in runtime path is introduced.

## DoD (F1)
- D1: contract file is published and linked from DEV_MAP/ROADMAP.
- D2: evidence field set is fixed and auditable.
- D3: strict non-goal stated: no runtime behavior changes.

## Non-goals
- No adapter code changes.
- No policy.py behavior changes.
- No CI pipeline changes.

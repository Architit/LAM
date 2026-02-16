# P4 Follow-up F3 Contract (Policy-v3 Config, Governance-Only)

## Purpose
Define policy-v3 configuration contract boundaries and schema outline without changing runtime behavior.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This step defines schema and migration boundaries only.

## Policy-v3 Config Contract Draft

### A) Schema outline (governance contract)
- `policy_version` (string): expected value `v3-draft`.
- `profiles` (object): named profile definitions (`ci`, `smoke`, `balanced`, `precision`, etc.).
- `selection_rules` (array): declarative selection clauses.
- `constraints` (object): cost/quality/availability boundaries.
- `evidence` (object): trace fields required for governance logs.

### B) Validation boundaries
- Schema validation is declarative in this phase.
- Missing/unknown fields are logged as governance findings, not runtime blockers.
- Migration path is documented as `v2 -> v3 (governance-only)`.

### C) Boundary rules
- No automatic config loading is introduced.
- No runtime enforcement of policy-v3 is introduced.
- No execution-path behavior change is introduced.

## DoD (F3)
- D1: contract file is published and linked from DEV_MAP/ROADMAP.
- D2: schema outline and migration boundaries are fixed and auditable.
- D3: strict non-goal stated: no runtime behavior changes.

## Non-goals
- No adapter code changes.
- No policy.py behavior changes.
- No CI pipeline changes.

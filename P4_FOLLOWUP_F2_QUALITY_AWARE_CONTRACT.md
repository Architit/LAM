# P4 Follow-up F2 Contract (Quality-Aware Routing, Governance-Only)

## Purpose
Define quality-aware routing contract boundaries and profile evidence mapping without changing runtime behavior.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This step defines quality profile semantics and evidence fields only.

## Quality-Aware Contract Draft

### A) Quality profile fields (contract level)
- `quality_profile` (enum): `balanced|precision|throughput|safety_bias`.
- `quality_intent` (string): normalized intent class used by governance mapping.
- `quality_priority` (enum): `high|medium|low`.
- `quality_decision` (enum): `accept|defer|fallback|reject`.

### B) Mapping evidence fields (governance logs/contracts)
- `intent_class`
- `quality_profile`
- `profile_reason_code`
- `provider_chain_view`
- `quality_decision`
- `trace_id` (if present)
- `timestamp_utc`

### C) Boundary rules
- Quality profile mapping is declarative in this phase.
- No provider order/runtime selection behavior is modified by this contract alone.
- No enforcement/runtime guard is introduced.

## DoD (F2)
- D1: contract file is published and linked from DEV_MAP/ROADMAP.
- D2: profile mapping evidence fields are fixed and auditable.
- D3: strict non-goal stated: no runtime behavior changes.

## Non-goals
- No adapter code changes.
- No policy.py behavior changes.
- No CI pipeline changes.

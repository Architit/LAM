# P4 Follow-up Backlog Contract (cost/quality/policy-v3)

## Purpose
Define a governance-only backlog after P4.1/P4.2/P4.3 closure.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This contract captures backlog planning only. It does not change router runtime behavior.

## Backlog Items (P4 follow-up)

### F1) Cost-aware routing contract
- Define cost budget fields for provider selection traces.
- Add governance evidence format for cost decisions in logs/contracts.
- DoD:
  - contract draft published
  - no provider order/runtime changes
  - references added to DEV_MAP/ROADMAP

### F2) Quality-aware routing contract
- Define intent/quality profile mapping as contract artifacts.
- Fix evidence boundaries between profile intent and final provider chain.
- DoD:
  - profile mapping draft published
  - read-only evidence blocks updated
  - no runtime changes

### F3) Policy v3 config contract
- Define config schema outline (`yaml/json`) and validation boundaries.
- State strict non-goals: no enforcement/no auto-application in runtime.
- DoD:
  - schema draft published
  - migration notes documented (v2 -> v3, governance-only)
  - no runtime changes

### F4) Provider metrics contract
- Define normalized provider metrics set (success/error/latency/tokens/cost).
- Bind metrics evidence format to observability logs and governance docs.
- DoD:
  - metrics contract draft published
  - evidence template added
  - no runtime changes

## Execution Order (recommended)
1. F1 cost-aware contract
2. F2 quality-aware contract
3. F3 policy-v3 schema contract
4. F4 provider metrics contract

## Non-goals
- No router implementation changes.
- No CI workflow changes.
- No cross-repo runtime rollout claims.

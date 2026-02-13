# P5.T2 Retrieval Boundary Contract (LAM)

## Purpose
Define governance-only boundaries for retrieval routing order and evidence in Phase 5 preparation.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Boundary statement
- Retrieval flow order is fixed at policy level:
  - memory/search evidence is consulted before LLM synthesis.
- This contract sets governance semantics only.
- It does not enable runtime routing, enforcement, or adapter behavior.

## Decision points (governance-only)
1. Input classification boundary
- Identify whether request requires memory retrieval, search retrieval, both, or none.

2. Evidence assembly boundary
- Record which retrieval source categories were considered before model response policy.

3. Fallback semantics boundary
- If retrieval evidence is unavailable, policy records explicit `retrieval_unavailable` state.
- No runtime fallback automation is introduced by this contract.

## Observability evidence fields
- `retrieval_mode`: `memory` | `search` | `memory+search` | `none`
- `retrieval_status`: `available` | `partial` | `unavailable`
- `retrieval_note`: short governance note describing why the mode/status was selected
- `decision_scope`: `governance-only`

## Non-goals
- No runtime retrieval implementation.
- No prompt-template changes.
- No provider/tool invocation logic.
- No cross-repo enforcement claims.

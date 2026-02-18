# SEMANTIC_SELECTION_PATTERN_CONTRACT

## Purpose
Define a governance-only semantic selection pattern for identity, routing, and snapshot synchronization across the ecosystem.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime auto-enforcement
- NO execution-path side effects

## Identity Layer (canonical triplet)
- Architect name (true name): stable semantic identity of entity
- Public name (call sign): human-facing alias
- System ID: machine-stable identifier

Reference mapping:
- `Loarachspoiszat` -> `Larpat` -> `LRPT`
- `Tendshpoisat` -> `Taspit` -> `TSPT`

## Semantic Selection Layers
1. Identity selection
- Input: semantic entity context
- Output: canonical triplet (`true_name`, `call_sign`, `system_id`)

2. Policy selection
- Input: constraints and governance intent
- Output: selected policy boundaries (`allow`, `hold`, `reject_scope`)
- Contract references:
  - `P5_RG1_ELIGIBILITY_MATRIX_CONTRACT.md`
  - `P5_RG2_HOLD_REJECT_POLICY_CONTRACT.md`
  - `LAM/default/contracts/semantic/PolicyConstraint.v1.md`

3. Route selection
- Input: task envelope + provider constraints
- Output: `selected_chain`
- Implementation references:
  - `Roaudter-agent/src/roaudter_agent/policy.py` (`select_chain`)
  - `Roaudter-agent/src/roaudter_agent/router.py` (`selected_chain`)

4. Snapshot selection
- Input: accepted/confirmed/planned protocol state
- Output: synchronized snapshot artifact for home origin
- Semantic expansion:
  - `snapshoot` = Save-to-Note of Applies Protocol Sync Home Origin Task

## Snapshot Record (required fields)
- `task_id`
- `entry_point`
- `storage_target`
- `home_origin`
- `poisat_slot` (outpost/integration slot/address)
- `selection_basis`
- `selected_policy_state` (`allow` | `hold` | `reject_scope`)
- `selected_chain` (if route layer is used)
- `timestamp_utc`

## Non-goals
- No replacement of existing runtime routers.
- No implicit override of RG1/RG2 governance contracts.
- No identity auto-generation without explicit governance context.

## Definition Notes
- `T` means `task`.
- `end/entry` means session boundary entry point.
- `s` means storage.
- `h` means home.
- `poisat` means outpost/point/integration slot/address.

## Compliance Rule
Any governance update touching identity, selection, or snapshot semantics MUST:
1. reference this contract id (`SEMANTIC_SELECTION_PATTERN_CONTRACT`),
2. include a semantic governance tag,
3. preserve backward compatibility of the canonical triplet fields.

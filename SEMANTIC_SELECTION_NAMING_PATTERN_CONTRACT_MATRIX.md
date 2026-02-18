# SEMANTIC_SELECTION_NAMING_PATTERN_CONTRACT_MATRIX

## Purpose
Define the canonical matrix for semantic-selection naming across ecosystem entities using the mandatory triplet:
- `true_name`
- `call_sign`
- `system_id`

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Naming Pattern
Each entity MUST expose exactly one semantic triplet:
1. `true_name` (architect-level canonical identity)
2. `call_sign` (public operational alias)
3. `system_id` (machine-stable address key)

## Contract Matrix

| domain_scope | entity_key | true_name | call_sign | system_id | role | lifecycle_state | naming_status | activation_gate |
|---|---|---|---|---|---|---|---|---|
| root_container | LRPT_ROOT | Loarachspoiszat | Larpat | LRPT | structural root container | ACTIVE | CANONICAL | OPEN |
| task_domain_home | TSPT_HOME | Tendshpoisat | Taspit | TSPT | task-home semantic domain | ACTIVE | CANONICAL | OPEN |
| legacy_alias_check | TSPT_ALIAS_VARIANT | Tendshpoisat | Tashpit | TSPT | alias compatibility check | HOLD | NON_CANONICAL_ALIAS | CLOSED_UNTIL_GOV_DECISION |
| requested_seed | AYA_PENDING | UNRESOLVED_TRUE_NAME | Ayaearias | AYA | requested ecosystem seed | HOLD | PENDING_TRIPLET_GOVERNANCE | CLOSED_UNTIL_NAMING_CONTRACT |
| requested_seed | ELARION_PENDING | UNRESOLVED_TRUE_NAME | Elarion | ELR | archive-core lineage seed | HOLD | PENDING_TRIPLET_GOVERNANCE | CLOSED_UNTIL_NAMING_CONTRACT |
| requested_seed | ELAFEI_PENDING | UNRESOLVED_TRUE_NAME | Elafei | ELF | requested ecosystem seed | HOLD | PENDING_TRIPLET_GOVERNANCE | CLOSED_UNTIL_NAMING_CONTRACT |
| repo_domain | LAM_TEST_AGENT_ARRIERGUARD | Aryargvardshpoisat | Arrierguard | ARGD | ecosystem arrierguard recovery/sustainment agent | ACTIVE | CANONICAL | OPEN |

## Selection Rules
1. `system_id` MUST be unique ecosystem-wide.
2. `true_name` is immutable after canonical activation.
3. `call_sign` change requires governance decision record.
4. Any entity with `naming_status != CANONICAL` is `HOLD` for subtree promotion.
5. No entity may be promoted to ACTIVE without full triplet and evidence trail.

## Activation Protocol
To move `HOLD -> ACTIVE`:
1. propose triplet in governance note,
2. validate uniqueness (`system_id`, triplet collision),
3. record decision in `ROADMAP.md` and `DEV_LOGS.md`,
4. update this matrix atomically.

## Non-goals
- No runtime registry behavior.
- No auto-generated true-name activation.
- No implicit promotion from alias-only records.

## Evidence Sources
- `NAMING_MODEL.md`
- `SEMANTIC_SELECTION_PATTERN_CONTRACT.md`
- `KIT_CATALOG_V2.md`

# P5.T3 Domain Partitioning Contract (LAM)

## Purpose
Define governance-only domain partitioning boundaries for memory and knowledge scope in Phase 5 preparation.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Domain partitions
1. `RADRILONIUMA`
- Governance/system-level project memory scope.
- Cross-repo policy and synchronization context.

2. `TRIANIUMA`
- Kingdom/world domain memory scope.
- Narrative/domain context separated from governance-layer facts.

## Partitioning rules (governance-only)
- Domain tag is mandatory in memory-related governance evidence: `domain = RADRILONIUMA | TRIANIUMA`.
- Cross-domain links must be explicit (`cross_domain_ref`) and justified in a short note.
- No implicit merge between domains is allowed in governance records.
- Ownership boundary must be documented per artifact: `owner_repo`, `owner_scope`.

## Traceability fields
- `domain`
- `owner_repo`
- `owner_scope`
- `cross_domain_ref` (optional)
- `partition_note`

## Non-goals
- No runtime memory router.
- No storage schema migration.
- No retrieval implementation or ranking logic.
- No automatic enforcement.

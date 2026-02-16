# MemoryIndexKey v1

## Purpose
Canonical indexing key representation for MemoryRecord.
Defines *how memory can be addressed and grouped*, not retrieval or storage.

## Source
- MemoryRecord v1
- SemanticEvent v1 / SemanticFailure v1 (indirect via MemoryRecord)

## Invariants
- Read-only derivation
- No storage/retrieval coupling
- Deterministic for the same inputs
- Low-cardinality where possible (index-friendly)
- Keys are declarative and portable across backends

## Status of this contract
- Contract-only (no implementation implied)
- Stable identifiers and field names (v1): additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### index_key_id
- type: string
- meaning: stable identifier of this index key record
- derivation: SHOULD be deterministic hash of (memory_id, key_kind, scope, key)

### key_kind
- type: string (enum)
- allowed:
  - trace_id
  - task_id
  - agent
  - event_type
  - failure_class
  - tag
  - concept
  - entity
- notes:
  - v1 keeps kinds minimal and cross-agent; add only when general

### key
- type: string
- meaning: the normalized indexable value
- invariants:
  - MUST be normalized (trimmed, lowercased where applicable)
  - SHOULD be short (backend-friendly)

### scope
- type: object
- required keys:
  - tier: string (enum: short_term | long_term)
- optional keys:
  - namespace: string          # logical partition, e.g. "system", "project", "domain:<x>"
  - agent: string             # if the key is intended to be agent-local
- notes:
  - scope is declarative; not a storage partition

### provenance
- type: object
- required keys:
  - memory_id: string
  - derived_from: string (enum: semantic_event | semantic_failure)
  - source_id: string          # semantic_event_id or failure_id
- optional keys:
  - payload_kind: string       # from MemoryRecord.memory_payload.payload_kind

### key_metrics
- type: object (map)
- meaning: semantic rollup relevant to indexing (e.g., importance, frequency hints)
- invariant: MAY be empty object, but field MUST exist
- guidance:
  - numeric scalars, low-cardinality strings only
  - no raw logs, no large payloads

## Notes
Contract-only artifact.
No implementation implied.

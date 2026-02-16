# MemoryRecord v1

## Purpose
Canonical representation of a memory primitive derived from SemanticEvent / SemanticFailure.
Defines memory *structure*, not storage or retrieval.

## Source
- SemanticEvent v1
- SemanticFailure v1 (optional)
- trace / metrics snapshot (read-only)

## Invariants
- Read-only derivation
- No storage/retrieval coupling
- Deterministic identity for the same semantic inputs
- Does not modify SemanticEvent v1 / SemanticFailure v1 (sources remain the truth)

## Status of this contract
- Contract-only (no implementation implied)
- Stable identifiers and field names (v1): additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### memory_id
- type: string
- meaning: stable identifier of the memory record
- derivation: SHOULD be deterministic hash of (trace_id, task_id, memory_type, payload_fingerprint)

### memory_type
- type: string (enum)
- allowed:
  - episodic        # event-like, narrative/traceable experience
  - semantic        # distilled facts / concepts
  - procedural      # how-to / patterns / routines
  - preference      # stable user/system preferences (non-sensitive; see governance)
- notes:
  - v1 focuses on generality; avoid agent-specific types

### retention_policy
- type: object
- required keys:
  - tier: string (enum: short_term | long_term)
  - ttl_seconds: integer (>= 0)     # 0 allowed meaning "no TTL declared" (implementation decides)
- optional keys:
  - importance: number (0..1)       # semantic importance score (derivation-only)
  - decay: string (enum: none | linear | exponential)
- invariants:
  - policy is declarative; not a storage decision

### memory_context
- type: object
- required keys:
  - trace_id: string
  - task_id: string
  - semantic_event_id: string
- optional keys:
  - parent_task_id: string
  - span_id: string
  - agent: string
  - source_failure_id: string       # if derived primarily from a SemanticFailure
  - tags: array[string]             # low-cardinality labels

### memory_payload
- type: object
- required keys:
  - payload_kind: string (enum: summary | fact | rule | pattern | pointer)
  - payload: object                 # JSON-compatible payload (structured)
- optional keys:
  - payload_fingerprint: string     # stable fingerprint for grouping/dedup
  - references: array[object]       # optional pointers (e.g., {kind, id, uri})

### memory_metrics
- type: object (map)
- meaning: semantic rollup relevant to memory derivation and usefulness
- invariant: MAY be empty object, but field MUST exist
- guidance:
  - prefer numeric scalars and low-cardinality strings
  - do not embed raw logs here

## Notes
Contract-only artifact.
No implementation implied.

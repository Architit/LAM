# ReflectionSnapshot v1

## Purpose
Canonical read-only snapshot for reflective analysis derived from Semantic* and Memory* contracts.
Defines *what the system can observe about itself*, not actions or decisions.

## Source
- SemanticEvent v1
- SemanticFailure v1
- MemoryRecord v1
- MemoryIndexKey v1
- trace / metrics snapshot (read-only)

## Invariants
- Read-only derivation
- No side effects
- No storage/retrieval coupling
- Deterministic for the same inputs
- Does not modify source contracts (Semantic* / Memory*)

## Status of this contract
- Contract-only (no implementation implied)
- Stable identifiers and field names (v1): additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### snapshot_id
- type: string
- meaning: stable identifier of the reflection snapshot
- derivation: SHOULD be deterministic hash of (observation_window, reflection_context, input_fingerprints)

### observation_window
- type: object
- required keys:
  - start_utc: string (RFC3339 / ISO-8601)
  - end_utc: string (RFC3339 / ISO-8601)
- optional keys:
  - window_kind: string (enum: rolling | fixed | trigger_based)
- invariants:
  - start_utc <= end_utc

### reflection_context
- type: object
- required keys:
  - trace_ids: array[string]
- optional keys:
  - task_ids: array[string]
  - agents: array[string]
  - scope: string              # logical scope (system / project / domain)
  - trigger_event_id: string   # semantic_event_id that initiated snapshot

### salient_events
- type: array[object]
- meaning: semantically important events within the observation window
- item keys:
  - semantic_event_id: string
  - event_type: string
  - importance: number (0..1)
- guidance:
  - low cardinality, summarised selection only

### salient_failures
- type: array[object]
- meaning: semantically important failures within the observation window
- item keys:
  - failure_id: string
  - failure_class: string
  - importance: number (0..1)

### memory_candidates
- type: array[object]
- meaning: potential MemoryRecord candidates derived from reflection
- item keys:
  - semantic_source_id: string     # semantic_event_id or failure_id
  - proposed_memory_type: string  # episodic | semantic | procedural | preference
  - rationale: string             # short, human-readable explanation
- notes:
  - this is *proposal only*, not memory creation

### reflection_metrics
- type: object (map)
- meaning: aggregate metrics about the reflective snapshot
- invariant: MAY be empty object, but field MUST exist
- guidance:
  - numeric scalars, low-cardinality strings only
  - examples: event_count, failure_count, window_duration_ms

## Notes
Contract-only artifact.
No implementation implied.

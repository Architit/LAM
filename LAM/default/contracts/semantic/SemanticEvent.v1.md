# SemanticEvent v1

## Purpose
Canonical semantic representation derived from ResultEnvelope + trace + metrics.
This contract defines *meaning*, not behavior.

## Source
- ResultEnvelope v1
- trace_id / span_id / parent_task_id
- metrics (runtime, mandatory)

## Invariants
- Read-only derivation
- No side effects
- No storage or memory coupling
- Does not modify ResultEnvelope v1 (envelope remains the source of truth)
- Deterministic for the same (envelope + trace + metrics snapshot)

## Status of this contract
- Contract-only (no implementation implied)
- Stable identifiers and field names (v1): additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### semantic_id
- type: string
- meaning: stable identifier of the derived semantic event
- derivation: SHOULD be deterministic hash of (trace_id, span_id, task_id, event_type) or equivalent stable scheme

### event_type
- type: string (enum)
- allowed:
  - task.received
  - task.enqueued
  - task.dequeued
  - task.started
  - task.completed
  - task.failed
  - provider.selected
  - provider.attempted
  - provider.fallback
  - provider.retry
  - result.emitted
- notes:
  - v1 is intentionally small; add new values only when they generalize across agents

### temporal_context
- type: object
- required keys:
  - observed_at_utc: string (RFC3339 / ISO-8601, timezone-aware, UTC recommended)
- optional keys:
  - duration_ms: number (>= 0)
  - latency_ms: number (>= 0)

### execution_context
- type: object
- required keys:
  - trace_id: string
  - task_id: string
- optional keys:
  - parent_task_id: string
  - span_id: string
  - agent: string
  - component: string
  - provider_used: string
  - attempt: integer (>= 1)

### outcome_summary
- type: object
- required keys:
  - status: string (enum: ok | error)
- optional keys:
  - error_class: string
  - error_message: string
  - result_kind: string

### semantic_metrics
- type: object (map)
- meaning: semantic rollup of metrics relevant to meaning/interpretation
- invariant: MAY be empty object, but field MUST exist
- guidance:
  - Prefer numeric scalars and low-cardinality strings
  - Do not duplicate raw high-volume logs here

## Notes
This is a contract-only artifact.
No implementation implied.

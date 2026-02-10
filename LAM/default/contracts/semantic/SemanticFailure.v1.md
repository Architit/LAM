# SemanticFailure v1

## Purpose
Canonical semantic representation of failures derived from SemanticEvent and ResultEnvelope (status=error).
Defines *meaning of failure*, not handling.

## Source
- SemanticEvent v1
- ResultEnvelope v1 (error)
- trace / metrics snapshot

## Invariants
- Read-only derivation
- No retries, no handling logic
- No storage or memory coupling
- Deterministic for the same inputs
- Does not modify ResultEnvelope v1 or SemanticEvent v1 (sources remain the truth)

## Status of this contract
- Contract-only (no implementation implied)
- Stable identifiers and field names (v1): additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### failure_id
- type: string
- meaning: stable identifier of the derived failure record
- derivation: SHOULD be deterministic hash of (trace_id, span_id, task_id, failure_class, error_fingerprint)

### failure_class
- type: string (enum)
- allowed:
  - timeout
  - auth
  - rate_limit
  - quota
  - provider_unavailable
  - invalid_request
  - parsing
  - tool_error
  - upstream_error
  - unknown
- notes:
  - use lowest-cardinality class that preserves meaning across agents

### failure_scope
- type: object
- required keys:
  - scope: string (enum: agent | provider | orchestration | infrastructure)
- optional keys:
  - agent: string
  - provider: string
  - component: string

### failure_context
- type: object
- required keys:
  - trace_id: string
  - task_id: string
  - semantic_event_id: string
- optional keys:
  - parent_task_id: string
  - span_id: string
  - event_type: string           # copy from SemanticEvent.event_type when useful
  - attempt: integer (>= 1)
  - error_code: string           # normalized code (e.g., HTTP status, provider code)
  - error_message: string        # short, user-safe, no stack traces
  - error_fingerprint: string    # stable fingerprint for grouping (hash/normalized signature)

### failure_metrics
- type: object (map)
- meaning: semantic rollup of metrics relevant to failure interpretation
- invariant: MAY be empty object, but field MUST exist
- guidance:
  - prefer numeric scalars and low-cardinality strings
  - do not embed raw logs / stack traces here

## Notes
Contract-only artifact.
No implementation implied.

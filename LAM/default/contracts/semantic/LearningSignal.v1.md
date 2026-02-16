# LearningSignal v1

## Purpose
Canonical read-only representation of a *learning-relevant signal* derived from ReflectionSnapshot and underlying Semantic*/Memory* contracts.
Defines *what can be measured/attributed as a learning signal*, not adaptation, training, or any execution-path change.

## Source
- ReflectionSnapshot v1
- SemanticEvent v1 (indirect via ReflectionSnapshot)
- SemanticFailure v1 (indirect via ReflectionSnapshot)
- MemoryRecord v1 (indirect via ReflectionSnapshot)
- MemoryIndexKey v1 (indirect via ReflectionSnapshot)
- trace / metrics snapshot (read-only, if referenced by ReflectionSnapshot)

## Invariants
- Contract-only (no implementation implied)
- Read-only derivation
- No side effects
- Deterministic for the same inputs
- Does not modify source contracts (ReflectionSnapshot / Semantic* / Memory*)
- Does not modify runtime behavior directly
- No auto-learning, no self-modification, no influence on execution path

## Status of this contract
- Stable identifiers and field names (v1)
- Additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### signal_id
- type: string
- meaning: stable identifier of the learning signal instance
- derivation: SHOULD be deterministic hash of (snapshot_id, signal_kind, source_fingerprints, window)

### signal_kind
- type: string (enum)
- allowed:
  - error_gradient_proxy
  - reward_proxy
  - novelty_proxy
  - uncertainty_proxy
  - salience_proxy
  - memory_value_proxy
  - alignment_risk_proxy
  - efficiency_proxy
  - other
- notes:
  - kinds are descriptive; they do not imply any learning algorithm

### source
- type: object
- required keys:
  - snapshot_id: string                 # ReflectionSnapshot.snapshot_id
  - primary_source_type: string (enum: reflection_snapshot | semantic_event | semantic_failure | memory_record)
  - primary_source_id: string           # semantic_event_id | failure_id | memory_record_id | snapshot_id
- optional keys:
  - related_event_ids: array[string]    # semantic_event_id
  - related_failure_ids: array[string]  # failure_id
  - related_memory_ids: array[string]   # memory_record_id
  - trace_ids: array[string]            # copied from ReflectionSnapshot.reflection_context.trace_ids when useful
- invariants:
  - primary_source_type MUST be consistent with primary_source_id domain

### observation_window
- type: object
- required keys:
  - start_utc: string (RFC3339 / ISO-8601)
  - end_utc: string (RFC3339 / ISO-8601)
- optional keys:
  - window_kind: string (enum: rolling | fixed | trigger_based)
- derivation:
  - SHOULD align to ReflectionSnapshot.observation_window
- invariants:
  - start_utc <= end_utc

### signal_value
- type: object
- meaning: the quantified or qualified signal value
- required keys:
  - value_kind: string (enum: scalar | distribution | categorical | boolean | vector | scorecard)
  - value: any
- optional keys:
  - unit: string                     # e.g., "probability", "ratio", "ms", "score"
  - range: object                    # e.g., {min, max}
  - confidence: number (0..1)        # optional confidence estimate (derivation-only)
- guidance:
  - keep low-cardinality and audit-friendly

### attribution
- type: object
- meaning: what the signal is attributed to (descriptive, not causal proof)
- required keys:
  - attribution_kind: string (enum: event | failure | memory | context | mixed)
- optional keys:
  - factors: array[object]           # e.g., {field, reference_id, weight, note}
  - rationale: string                # short human-readable explanation
- notes:
  - attribution is explanatory metadata, not an enforcement/decision mechanism

### constraints
- type: object
- meaning: policy and governance overlays relevant to interpreting this signal
- required keys:
  - policy_constraint_ids: array[string]
- optional keys:
  - interpretation_limits: array[string]   # human-readable guardrails
- derivation:
  - MAY reference PolicyConstraint v1 if available for the snapshot context
- invariants:
  - field MUST exist (may be empty arrays)

### signal_metrics
- type: object (map)
- meaning: observability hints and metadata about the signal
- invariant: MAY be empty object, but field MUST exist
- examples:
  - computed_at_utc
  - producer
  - version
  - tags
  - priority

## Notes
Contract-only artifact.
No implementation implied.

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

## Fields
- semantic_id
- event_type
- temporal_context
- execution_context
- outcome_summary
- semantic_metrics

## Notes
This is a contract-only artifact.
No implementation implied.

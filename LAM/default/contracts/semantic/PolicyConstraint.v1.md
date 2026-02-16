# PolicyConstraint v1

## Purpose
Declarative constraints defining what the system is allowed or forbidden to adapt or propose.
Defines *boundaries*, not behavior or enforcement.

## Source
- ReflectionSnapshot v1
- Governance configuration (out-of-band)

## Invariants
- Contract-only (no implementation implied)
- Read-only derivation
- No side effects
- Does not modify runtime behavior directly
- Deterministic interpretation for the same inputs

## Status of this contract
- Stable identifiers and field names (v1)
- Additive changes allowed; breaking changes require v2

## Fields
All fields below are REQUIRED unless explicitly marked optional.

### constraint_id
- type: string
- meaning: stable identifier of the policy constraint
- derivation: MAY be governance-defined or deterministic hash of (constraint_scope, constraint_type, condition)

### constraint_scope
- type: object
- required keys:
  - level: string (enum: system | project | agent | component)
- optional keys:
  - agent: string
  - component: string
  - domain: string
- notes:
  - scope limits where the constraint applies; it is not an enforcement mechanism

### constraint_type
- type: string (enum)
- allowed:
  - forbid_proposal
  - allow_proposal
  - require_human_review
  - rate_limit_adaptation
  - freeze_learning
- notes:
  - types are declarative; semantics defined by governance

### condition
- type: object
- meaning: declarative condition under which the constraint is applicable
- required keys:
  - source: string (enum: reflection_snapshot | memory_record | semantic_event | semantic_failure)
- optional keys:
  - predicates: array[object]   # e.g., {field, op, value}
  - window: object              # optional temporal bounds
- notes:
  - condition is descriptive, not executable logic

### rationale
- type: string
- meaning: human-readable explanation for why this constraint exists
- guidance:
  - concise, audit-friendly, stable wording

### constraint_metrics
- type: object (map)
- meaning: metadata and observability hints about the constraint
- invariant: MAY be empty object, but field MUST exist
- examples:
  - priority
  - introduced_at
  - owner

## Notes
Contract-only artifact.
No implementation implied.

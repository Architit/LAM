# P4 Phase 4.3 A1 Contract (Adaptation Proposal Schema v1, Governance-Only)

timestamp_utc: 2026-02-16T23:04:00Z
scope: A1 schema contract for adaptation proposals
mode: contracts-first, observability-first, derivation-only

## Purpose
Define canonical proposal schema for Phase 4.3 adaptation artifacts.

Hard constraints:
- NO runtime logic
- NO execution-path impact
- NO auto-application

## Proposal Schema v1
- `proposal_id` (string, required)
- `source_context` (object, required)
  - `trace_id` (string, required)
  - `task_id` (string, required)
  - `phase` (string, required)
- `constraints_snapshot` (object, required)
  - `policy_version` (string, required)
  - `boundary_state` (string, required)
- `expected_effect` (string, required, governance semantics only)
- `risk_class` (enum: LOW|MEDIUM|HIGH, required)
- `evidence_refs` (array<string>, required)
- `non_goals_confirmation` (boolean, required; must be `true`)

## Validation Rules
- Missing required fields => `SCHEMA_INCOMPLETE` (governance finding only).
- Unknown fields allowed but must be logged as `SCHEMA_EXTENSION_CANDIDATE`.
- All timestamps referenced in evidence must be UTC.

## DoD
- schema published and referenced in roadmap
- validation boundaries explicitly declared
- no runtime-facing code changes

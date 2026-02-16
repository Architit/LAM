# P4 Phase 4.3 A4 Contract (Proposal Evidence Consolidation, Governance-Only)

timestamp_utc: 2026-02-16T23:28:00Z
scope: consolidate adaptation proposal evidence references
mode: contracts-first, observability-first, derivation-only

## Purpose
Define one canonical evidence bundle format for adaptation proposal review artifacts.

Hard constraints:
- NO runtime logic
- NO execution-path impact
- NO automatic state mutation

## Evidence Bundle v1
- `bundle_id`
- `proposal_id`
- `schema_ref` (A1)
- `evaluation_ref` (A2)
- `decision_ref` (A3)
- `trace_context` (`trace_id`, `task_id`, `phase`)
- `timestamp_utc`

## Validation
- all refs must resolve to existing markdown artifacts
- timestamp must be UTC
- missing refs => `BUNDLE_INCOMPLETE` (governance finding only)

## DoD
- bundle format published
- validation clauses explicit
- no runtime-facing code changes

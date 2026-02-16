# P4 Phase 4.3 A3 Contract (Adaptation Review Decision Record v1, Governance-Only)

timestamp_utc: 2026-02-16T23:04:00Z
scope: A3 decision record contract for adaptation proposal review
mode: contracts-first, observability-first, derivation-only

## Purpose
Define final decision record structure for reviewed adaptation proposals.

Hard constraints:
- NO runtime apply
- NO automatic policy activation
- NO execution-path impact

## Decision Record v1
- `decision_record_id` (string, required)
- `proposal_id` (string, required)
- `evaluation_id` (string, required)
- `decision` (enum: APPROVE_FOR_NEXT_GATE|HOLD|REJECT, required)
- `decision_reason` (string, required)
- `non_goals_confirmation` (boolean, required; must be `true`)
- `next_step_pointer` (string, required)
- `evidence_refs` (array<string>, required)

## Decision Semantics
- `APPROVE_FOR_NEXT_GATE`: proposal can advance to next governance gate only.
- `HOLD`: proposal requires additional evidence.
- `REJECT`: proposal closed for current wave.

## DoD
- decision schema published and linked in roadmap/logs
- explicit non-goals confirmation required
- no runtime-facing code changes

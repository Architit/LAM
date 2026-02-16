# P4 Phase 4.3 N3 Contract (Controlled Gate-Open Recommendation Draft, Governance-Only)

timestamp_utc: 2026-02-16T23:52:00Z
scope: draft recommendation for controlled next-gate opening
mode: contracts-first, observability-first, derivation-only

## Purpose
Define recommendation draft structure for controlled gate-open decision.

## Draft Fields
- `draft_id`
- `package_id` (N1)
- `boundary_revalidation_state` (N2 result)
- `recommended_gate_state` (`OPEN_REVIEW|HOLD_REVIEW`)
- `rationale`
- `evidence_refs`
- `operator_gate_required` (must be true)

## DoD
- draft schema published
- operator-gate requirement explicit
- no runtime-facing code changes

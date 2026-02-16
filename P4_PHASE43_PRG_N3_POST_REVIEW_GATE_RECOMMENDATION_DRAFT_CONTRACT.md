# P4 Phase 4.3 PRG N3 Contract (Post-Review Gate Recommendation Draft, Governance-Only)

timestamp_utc: 2026-02-17T00:21:00Z
scope: PHASE43_POST_REVIEW_GATE_PREP / n3
mode: contracts-first, observability-first, derivation-only

## Purpose
Draft recommendation for post-review gate state after PRG prep.

## Draft Fields
- `draft_id`
- `post_review_package_id` (PRG N1)
- `boundary_state` (PRG N2)
- `recommended_gate_state` (`OPEN_POST_REVIEW_GATE|HOLD_POST_REVIEW_GATE`)
- `reason`
- `evidence_refs`
- `operator_gate_required` (must be true)

## DoD
- draft schema published
- recommendation state enum fixed
- no runtime-facing changes

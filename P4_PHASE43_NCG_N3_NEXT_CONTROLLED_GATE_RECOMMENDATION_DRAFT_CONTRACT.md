# P4 Phase 4.3 NCG N3 Contract (Next Controlled Gate Recommendation Draft, Governance-Only)

timestamp_utc: 2026-02-17T00:58:00Z
scope: PHASE43_NEXT_CONTROLLED_GATE_PREP / n3
mode: contracts-first, observability-first, derivation-only

## Purpose
Draft recommendation for next controlled gate state.

## Draft Fields
- `draft_id`
- `next_controlled_package_id` (NCG N1)
- `boundary_state` (NCG N2)
- `recommended_gate_state` (`OPEN_NEXT_CONTROLLED_GATE|HOLD_NEXT_CONTROLLED_GATE`)
- `reason`
- `evidence_refs`
- `operator_gate_required` (must be true)

## DoD
- draft schema published
- recommendation enum fixed
- no runtime-facing changes

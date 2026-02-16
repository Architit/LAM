# P4 Phase 4.3 NCG N1 Contract (Next Controlled Package Consolidation, Governance-Only)

timestamp_utc: 2026-02-17T00:58:00Z
scope: PHASE43_NEXT_CONTROLLED_GATE_PREP / n1
mode: contracts-first, observability-first, derivation-only

## Purpose
Consolidate package refs for the next controlled gate prep.

## Inputs
- `P4_PHASE43_POST_REVIEW_GATE_EXECUTION_CONTRACT.md`
- `P4_PHASE43_POST_REVIEW_EXECUTION_POINTER_UPDATE_CONTRACT.md`
- `P4_PHASE43_POST_REVIEW_GATE_DECISION_CONTRACT.md`

## Output Schema
- `next_controlled_package_id`
- `execution_ref`
- `pointer_ref`
- `decision_ref`
- `evidence_refs`

## DoD
- schema published
- refs complete
- no runtime-facing changes

# P4 Phase 4.3 A5 Contract (Proposal Risk Stratification, Governance-Only)

timestamp_utc: 2026-02-16T23:28:00Z
scope: risk stratification model for adaptation proposals
mode: contracts-first, observability-first, derivation-only

## Purpose
Define governance review cadence by risk tier for adaptation proposals.

Hard constraints:
- NO runtime enforcement
- NO auto-blocking side effects
- NO policy auto-apply

## Risk Tiers
- `LOW`: review cadence standard, minimal escalation
- `MEDIUM`: review cadence elevated, explicit second-check required
- `HIGH`: review cadence strict, mandatory governance escalation note

## Tier Inputs
- `policy_boundary_compliance` result
- `reversibility` score
- `evidence_completeness` state
- `decision_confidence` score

## Output
- `risk_tier`
- `review_cadence`
- `escalation_required` (boolean)
- `rationale`

## DoD
- risk model published
- input/output fields fixed
- no runtime-facing code changes

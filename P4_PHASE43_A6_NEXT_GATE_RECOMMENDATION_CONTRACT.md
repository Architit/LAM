# P4 Phase 4.3 A6 Contract (Next-Gate Recommendation, Governance-Only)

timestamp_utc: 2026-02-16T23:28:00Z
scope: recommendation contract for next governance gate transition
mode: contracts-first, observability-first, derivation-only

## Purpose
Define deterministic recommendation record for advancing from A4/A5 outputs to the next governance gate.

Hard constraints:
- NO runtime execution
- NO automatic transition
- NO CI/runtime behavior changes

## Recommendation Record v1
- `recommendation_id`
- `bundle_id` (A4 evidence bundle)
- `risk_tier` (A5 output)
- `recommended_next_gate` (string)
- `recommendation_state` (`PROCEED_REVIEW|HOLD_REVIEW|REJECT_REVIEW`)
- `reason`
- `evidence_refs`
- `non_goals_confirmation` (must be true)

## Decision Semantics
- `PROCEED_REVIEW`: eligible for explicit manual governance approval.
- `HOLD_REVIEW`: needs additional evidence/risk clarification.
- `REJECT_REVIEW`: close current proposal for this wave.

## DoD
- recommendation schema published
- semantics and non-goals explicit
- no runtime-facing code changes

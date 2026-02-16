# P4 Phase 4.3 A2 Contract (Adaptation Evaluation Matrix v1, Governance-Only)

timestamp_utc: 2026-02-16T23:04:00Z
scope: A2 evaluation matrix contract for adaptation proposals
mode: contracts-first, observability-first, derivation-only

## Purpose
Define deterministic evaluation matrix for proposal review without runtime execution.

Hard constraints:
- NO runtime enforcement
- NO execution blocking side effects
- NO provider routing mutations

## Evaluation Axes
- `determinism`: proposal preserves deterministic interpretation.
- `observability`: proposal contains complete evidence refs and trace context.
- `reversibility`: proposal can be reverted at contract level without state mutation.
- `policy_boundary_compliance`: proposal respects declared non-goals and boundaries.

## Scoring Model (Governance-Only)
- each axis score: `0|1|2` (LOW|MEDIUM|HIGH confidence)
- aggregate band:
  - `7-8`: `ALLOW_REVIEW`
  - `4-6`: `HOLD_REVIEW`
  - `0-3`: `REVISE_REQUIRED`

## Output Contract
- `evaluation_id`
- `proposal_id`
- `axis_scores`
- `aggregate_score`
- `review_recommendation` (`ALLOW_REVIEW|HOLD_REVIEW|REVISE_REQUIRED`)
- `notes`

## DoD
- matrix model published and linked
- output schema fixed and auditable
- no runtime-facing code changes

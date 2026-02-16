# P5.POST3 Next Package Start Recommendation Contract (LAM)

## Purpose
Define governance-only recommendation record for next package start after `P5.POST` closure.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Recommendation scope
- Record one primary next-package recommendation and alternatives.
- Bind recommendation to evidence from POST1/POST2.
- Keep recommendation declarative, without execution trigger.

## Required recommendation blocks
1. `primary_recommendation`
2. `alternative_recommendations`
3. `evidence_refs`
4. `risk_note`
5. `boundary_note`

## Required record fields
- `recommendation_id`
- `task_id`
- `recommended_next_package`
- `alternatives`
- `rationale`
- `next_target`
- `timestamp_utc`

## Non-goals
- No runtime start command.
- No scheduler/job creation.
- No automation of acceptance flow.

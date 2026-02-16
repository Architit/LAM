# Z.T3 Compatibility DoD Contract (LAM)

## Purpose
Define governance-only compatibility DoD for Phase Z draft integration package.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Compatibility DoD scope
- Preserve existing codex/openai path as baseline.
- Keep Agent SDK backend path declarative and optional.
- Require evidence-only non-regression markers.

## Required DoD blocks
1. `baseline_path_unchanged`
2. `optional_backend_boundary`
3. `smoke_evidence_boundary`
4. `non_regression_assertions`
5. `release_readiness_note`

## Required record fields
- `dod_id`
- `task_id`
- `compatibility_checks`
- `residual_risks`
- `next_target`
- `timestamp_utc`

## Non-goals
- No runtime backend switching.
- No execution routing changes.
- No CI/runtime enforcement hooks.

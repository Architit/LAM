# Z.T1 Agent SDK Backend Integration Contract (LAM)

## Purpose
Define governance-only draft contract for Agent SDK integration as backend tool path.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Integration draft scope
- SDK is described as optional backend path under codex tool orchestration.
- Existing codex/openai path remains primary and unchanged.
- Integration points are declarative and evidence-first.

## Required integration blocks
1. `backend_role_definition`
2. `entrypoint_boundary`
3. `fallback_boundary`
4. `evidence_requirements`
5. `non_regression_note`

## Required record fields
- `integration_id`
- `task_id`
- `backend_scope`
- `compatibility_scope`
- `open_questions`
- `next_target`
- `timestamp_utc`

## Non-goals
- No SDK runtime wiring.
- No live backend switch logic.
- No execution path mutation.

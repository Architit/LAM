# P6.T2 Health Telemetry Profile Draft Contract (LAM)

## Purpose
Define governance-only draft profile for control plane health/telemetry visibility in Phase 6.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Profile draft scope
- Provider health summary visibility
- Cost/usage telemetry visibility
- Trace/log signal visibility
- Read-only operator dashboard boundaries

## Required profile blocks
1. `health_view_profile`
2. `cost_view_profile`
3. `trace_view_profile`
4. `alert_visibility_profile`
5. `read_only_boundary_note`

## Required record fields
- `profile_id`
- `task_id`
- `profile_blocks`
- `known_gaps`
- `risk_note`
- `next_target`
- `timestamp_utc`

## Non-goals
- No live alert automation.
- No runtime control actions.
- No execution path modifications.

# Z.T2 Smoke Contract Draft (LAM)

## Purpose
Define governance-only smoke contract draft for Phase Z integration validation.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Smoke draft scope
- One-command smoke invocation shape
- Minimal evidence envelope fields
- Pass/fail reporting semantics for governance records

## Required smoke blocks
1. `smoke_command_shape`
2. `input_boundary`
3. `expected_envelope_fields`
4. `trace_requirements`
5. `failure_capture_note`

## Required record fields
- `smoke_id`
- `task_id`
- `command_stub`
- `expected_result_shape`
- `evidence_stub`
- `next_target`
- `timestamp_utc`

## Non-goals
- No executable runtime smoke script.
- No CI pipeline change.
- No execution path modification.

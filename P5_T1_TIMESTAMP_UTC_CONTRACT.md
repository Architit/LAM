# P5.T1 Timestamp UTC Contract (LAM)

## Purpose
Define governance-only normalization rules for timezone-aware UTC timestamps in LAM contracts, logs, and snapshot artifacts.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Canonical timestamp formats
1. Event/log line format:
- `YYYY-MM-DD HH:MM UTC`
- Example: `2026-02-13 03:39 UTC`

2. Snapshot identity format:
- `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2026-02-13T03:39:28Z`

## Normalization rules
- Use UTC only; local timezone abbreviations are not allowed.
- Use explicit `UTC` suffix for human-readable log lines.
- Use explicit `Z` suffix for ISO 8601 snapshot timestamps.
- When both formats are present in one governance cycle, they must represent the same UTC moment family (no timezone drift).

## Evidence checklist (governance-only)
- `DEV_LOGS.md` entries use `YYYY-MM-DD HH:MM UTC`.
- `WORKFLOW_SNAPSHOT_STATE.md` identity timestamp uses ISO `...Z`.
- `ROADMAP.md` changelog references are date-accurate for the same cycle.
- Mirror files in `LAM/default/*` reflect the same phase pointer without conflicting timezone semantics.

## Non-goals
- No parser/runtime enforcement.
- No automatic conversion tooling.
- No migration of historical lines unless explicitly required by governance.

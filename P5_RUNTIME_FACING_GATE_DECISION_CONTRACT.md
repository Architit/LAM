# P5 Runtime-Facing Gate Decision Contract (LAM)

## Purpose
Define governance-only decision package for allowing or holding runtime-facing Phase 5 work after P5 execution-gate closure.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Decision package status
- Package: `P5.RG` (runtime-facing gate decision)
- Status: ACTIVE (governance-only)
- Prerequisite: `P5.EXEC` wave (`G1/G2/G3`) CLOSED

## Decision queue (ordered)
1. P5.RG1 - Runtime-facing eligibility matrix
- Define eligibility fields and acceptance policy for runtime-facing scope.

2. P5.RG2 - Hold/reject decision policy
- Define deterministic decision outcomes: `allow_start`, `hold`, `reject_scope`.

3. P5.RG3 - Start-approval evidence record
- Define minimal evidence record required before first runtime-facing phase5 task.

## DoD for decision package
- D1: `DEV_MAP.md` and `ROADMAP.md` explicitly mark `P5.RG` package ACTIVE.
- D2: queue `P5.RG1/P5.RG2/P5.RG3` is fixed and ordered.
- D3: `DEV_LOGS.md`, `WORKFLOW_SNAPSHOT_STATE.md`, and default mirrors are synchronized in one governance cycle.
- D4: no contradiction with closed states (`P2.4`, `P4` follow-up, `P5` prep, `P5.EXEC`).

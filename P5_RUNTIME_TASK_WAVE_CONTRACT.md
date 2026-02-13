# P5 Runtime Task Wave Contract (LAM)

## Purpose
Define governance-only planning package for the first runtime-facing Phase 5 task wave after gate-decision closure.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Wave status
- Wave: `P5.RT`
- Status: ACTIVE (governance-only planning)
- Prerequisite: runtime-facing gate decision wave (`P5.RG1/RG2/RG3`) CLOSED

## Runtime task wave queue (ordered)
1. P5.RT1 - Runtime-facing task candidate definition
- Define first candidate scope and explicit non-goals.

2. P5.RT2 - Runtime-facing preflight checklist
- Define read-only preflight checks and acceptance evidence.

3. P5.RT3 - Runtime-facing start decision record
- Define final governance record for start/no-start decision.

## DoD for this planning package
- D1: `DEV_MAP.md` and `ROADMAP.md` explicitly mark `P5.RT` planning wave ACTIVE.
- D2: queue `P5.RT1/P5.RT2/P5.RT3` is fixed and ordered.
- D3: `DEV_LOGS.md`, mirrors, and `WORKFLOW_SNAPSHOT_STATE.md` are synchronized in one cycle.
- D4: no contradiction with closed states (`P2.4`, `P4`, `P5 prep`, `P5.EXEC`, `P5.RG`).

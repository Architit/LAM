# Phase Z Prep Agent SDK Backlog Contract (LAM)

## Purpose
Define governance-only activation package for Phase Z (Agent SDK Integrations v0).

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Package status
- Package: `Z.PREP`
- Status: ACTIVE (governance-only)
- Prerequisite: `P6.PREP` CLOSED

## Ordered queue
1. Z.T1 - Agent SDK backend integration contract draft
- Define integration boundary for SDK-as-backend with no runtime hooks.

2. Z.T2 - Smoke contract draft
- Define one-command smoke contract and required evidence fields.

3. Z.T3 - Compatibility DoD contract draft
- Define non-regression DoD for existing codex/openai path.

## DoD for activation
- D1: `DEV_MAP.md` and `ROADMAP.md` mark `Z.PREP` ACTIVE.
- D2: queue `Z.T1/Z.T2/Z.T3` is fixed and ordered.
- D3: `DEV_LOGS.md`, mirrors, and `WORKFLOW_SNAPSHOT_STATE.md` are synchronized in one cycle.
- D4: no contradiction with closed states (`P5.POST`, `P6.PREP`).

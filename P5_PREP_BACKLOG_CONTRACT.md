# P5 Prep Backlog Contract (LAM)

## Purpose
Define the governance-only preparation backlog for Phase 5 (Memory & Knowledge Layer) in LAM.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This contract fixes the initial P5 prep queue and expected evidence format.
It does not introduce runtime behavior, enforcement, or automation.

## P5 prep queue (ordered)
1. P5.T1 - Timestamp normalization policy
- Publish governance contract for timezone-aware UTC timestamp policy across docs/events contracts.
- Fix evidence fields and acceptance checklist (policy-only).

2. P5.T2 - Retrieval routing boundary draft
- Publish governance draft for retrieval-before-LLM routing boundaries.
- Fix decision points, non-goals, and observability evidence blocks (policy-only).

3. P5.T3 - Domain memory partitioning draft
- Publish governance draft for RADRILONIUMA/TRIANIUMA memory domain partitioning.
- Fix naming, ownership, and traceability boundaries (policy-only).

## DoD for P5 prep start
- D1: `DEV_MAP.md` and `ROADMAP.md` explicitly mark P5 prep as ACTIVE.
- D2: P5 prep queue (`T1-T3`) is fixed and ordered.
- D3: `DEV_LOGS.md`, `WORKFLOW_SNAPSHOT_STATE.md`, and default mirrors are synchronized in the same governance cycle.
- D4: no contradiction with prior closed states (`P2.4` runtime closure and `P4` follow-up closure).

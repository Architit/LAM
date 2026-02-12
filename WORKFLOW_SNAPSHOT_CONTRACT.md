# Workflow Snapshot Contract (LAM)

## Purpose
This contract defines the repo-native snapshot used for deterministic context recovery in LAM.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Two-phase rule (`ssn rstrt`)
A) EXPORT in active chat:
- update `WORKFLOW_SNAPSHOT_STATE.md`
- capture current `git status -sb`
- refresh `NEW_CHAT_INIT_MESSAGE`

B) IMPORT in new chat:
- read `WORKFLOW_SNAPSHOT_STATE.md`
- run read-only sync: `pwd`, `git status -sb`, `git log -n 12 --oneline`
- continue from declared phase/stage

# Phase 3.2.C — Git Subtree Strategy (Contract)

This document defines the **contract-level** strategy for distributing ecosystem structural containers via **git subtree**.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

This is policy + documentation only. No subtree implementation is introduced here.

---

## 1. Scope

Phase 3.2.C defines:
- why subtree is the preferred distribution mechanism for ecosystem containers,
- the minimal rules for importing/updating subtree content,
- governance and observability expectations for subtree operations.

---

## 2. Non-goals (hard)

This contract MUST NOT introduce:
- scripts/automation that performs subtree operations,
- CI enforcement,
- runtime hooks,
- repository restructuring (no new directories/subtrees applied here).

---

## 3. Rationale (why subtree)

Subtree is preferred because it:
- keeps imported content **repo-native** (no submodule friction),
- supports **local adaptations** without breaking baseline history,
- allows reproducible vendor-style updates (pull/squash patterns),
- avoids multi-repo checkout requirements for contributors.

---

## 4. Contract Rules

### 4.1 Import rule
A subtree import MUST be:
- explicit (human/agent declared intent),
- reviewable (PR/commit shows the full diff),
- atomic (one logical import per commit series).

### 4.2 Update rule
A subtree update MUST:
- preserve local adaptations intentionally (documented in commit message),
- include provenance (source repo + ref),
- remain derivation-only (no hidden generated content).

### 4.3 Local adaptation rule
Local modifications to subtree-derived content MUST be:
- clearly labeled in commit messages,
- reviewable as deltas over imported baseline,
- not converted into runtime coupling.

---

## 5. Observability requirements

Every subtree import/update MUST capture:
- source repository identifier
- source ref (tag/commit)
- subtree prefix path (if used)
- resulting commit hash

These are governance-level records, not runtime outputs.

---

## 6. Governance & change management

Changes to subtree policy MUST be reflected in:
- ROADMAP.md (phase-level tracking)
- DEV_LOGS.md (completion log)

All changes must remain atomic and reversible.


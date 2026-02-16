# Phase 4.A — DevKit Subtree Distribution (Contract)

This document defines the contract-level policy for distributing DevKit
artifacts across the RADRILONIUMA ecosystem via git subtree.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

This phase introduces policy only. No subtree is created or modified here.

---

## 1. Scope

Phase 4.A defines:
- which DevKit artifacts are normative,
- how they are intended to be distributed,
- the governance model for cross-repo synchronization.

It does NOT implement subtree operations.

---

## 2. Normative Artifacts

The following files are considered governance-normative:

- INTERACTION_PROTOCOL.md
- TASK_SPEC.md
- NAMING_MODEL.md
- ECOSYSTEM_STRUCTURE.md
- SUBTREE_STRATEGY.md

These artifacts define ecosystem behavior and must remain non-runtime.

---

## 3. Distribution Model (Intent)

DevKit SHALL act as the canonical source of governance artifacts.

Other repositories MAY import governance artifacts via git subtree.

Subtree usage requirements:
- explicit prefix path
- explicit source repository
- explicit source ref (tag or commit)
- atomic commit series

No automatic enforcement is defined in this phase.

---

## 4. Update Model

When governance artifacts change in DevKit:

- downstream repositories must explicitly pull subtree updates,
- updates must be reviewable,
- provenance must be recorded in commit messages.

No background synchronization is allowed.

---

## 5. Separation of Concerns

DevKit:
- defines governance contracts,
- defines execution tooling,
- remains runtime-neutral.

LAM:
- defines runtime behavior,
- implements automation,
- may consume DevKit contracts but must not mutate them.

---

## 6. Observability

Every subtree import/update must record:
- source repo
- source ref
- subtree prefix
- resulting commit hash

This is a governance record, not runtime telemetry.


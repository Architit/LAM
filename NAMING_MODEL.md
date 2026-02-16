# Phase 3.2.B — Naming Model (Contract)

This document formalizes the **3-level naming model** for ecosystem structural entities.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

This is a structural contract only.

---

## 1. Naming Model — Mandatory Structure

Every ecosystem structural entity MUST define exactly three name levels:

1. **True-name**
   - Canonical architect-level identifier.
   - Immutable once established.
   - Represents the full semantic identity of the structure.

2. **Public nickname**
   - Human-facing call sign.
   - Short, memorable, ecosystem-visible.
   - May be used in documentation and discussion.

3. **System ID**
   - Machine identifier.
   - Compact, stable, uppercase ASCII.
   - Used for addressing, tagging, and structural referencing.

No entity may omit one of these levels.

---

## 2. Semantic Rules

- True-name encodes maximum semantic density.
- Public nickname encodes usability.
- System ID encodes structural addressability.
- The three names must remain internally consistent.

The naming model is a **system rule**, not a stylistic preference.

---

## 3. First Structural Instances (Reference)

### Root Container
- True-name: Loarachspoiszat
- Public nickname: Larpat
- System ID: LRPT

### Task-domain Home
- True-name: Tendshpoisat
- Public nickname: Taspit
- System ID: TSPT

These serve as canonical reference instances of the model.

---

## 4. Non-goals

This model MUST NOT:
- introduce runtime behavior,
- introduce registry logic,
- imply ownership hierarchy enforcement,
- modify execution paths.

It defines identity semantics only.

---

## 5. Observability & Governance

Any modification to naming rules MUST:
- be recorded in ROADMAP.md,
- be logged in DEV_LOGS.md,
- remain atomic and derivation-only.

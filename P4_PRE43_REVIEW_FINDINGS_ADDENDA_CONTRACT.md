# P4 Pre-4.3 Review Findings Addenda Contract (R1-R5, Governance-Only)

timestamp_utc: 2026-02-16T22:44:00Z
scope: closure addenda for Phase 4 pre-4.3 findings in LAM
mode: contracts-first, observability-first, derivation-only

## Purpose
Close review findings `R1..R5` before Phase 4.3 start without runtime logic changes.

Hard constraints:
- NO runtime logic
- NO execution-path impact
- NO enforcement side effects beyond contract wording

## Findings Closure

### R1 — Spec drift (missing fields in derivation references)
Decision:
- `ReflectionSnapshot.snapshot_id` derivation MUST use stable fields only:
  - `trace_id`
  - `task_id`
  - `created_at_utc`
  - `snapshot_kind`
- `LearningSignal.signal_id` derivation MUST use stable fields only:
  - `trace_id`
  - `source_snapshot_id`
  - `created_at_utc`
  - `signal_kind`
- `input_fingerprints` and `source_fingerprints` are explicitly NOT required fields in v1.x.

### R2 — Policy predicates underspecified
Decision:
- `PolicyConstraint.condition.predicates` minimal contract fixed:
  - `op`: one of `eq|neq|in|nin|gt|gte|lt|lte|exists`
  - `path`: dot-notation field path (example: `context.trace_id`)
  - `value`: scalar/list according to operator
- Group semantics:
  - default: implicit `AND`
  - optional explicit group: `all` (AND) / `any` (OR)
- Missing path semantics:
  - `exists`: evaluates `false` when path missing
  - all other ops on missing path: `UNSATISFIED` (non-fatal in governance-only mode)

### R3 — Policy/Learning boundary ambiguity
Decision:
- `freeze_learning` and `rate_limit_adaptation` are governance intent markers only.
- They MUST NOT imply runtime bridge or automatic execution control.
- Learning proxies/weights remain analysis metadata, not runtime control-plane commands.

### R4 — Derivation vs semantics wording split
Decision:
- Contract text is split into:
  - `Derivation Rules` (identifier construction / representational structure),
  - `Governance Semantics` (human/operator interpretation and policy meaning).
- No clause may mix derivation formulas with enforcement semantics.

### R5 — Missing explicit Non-Goals
Decision:
- PolicyConstraint Non-Goals are now explicit:
  - no runtime enforcement,
  - no execution blocking,
  - no conflict auto-resolution,
  - no policy-triggered mutation of runtime state.

## Phase 4.3 Entry Gate
- gate_state: OPEN
- prerequisite: `R1..R5` CLOSED in roadmap and logs
- runtime_impact: NONE

## Evidence
- `ROADMAP.md` (R1..R5 status set to DONE)
- `DEV_LOGS.md` (closure event recorded)
- `TASK_LIST.md` (follow-up pointer updated)

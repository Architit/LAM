# TASK_SPEC — Declarative Task Contract (DevKit)

**Scope:** This document defines the **canonical, declarative contract** for a *Task Spec* consumed/validated by tooling.  
**Source of Truth:** Real task specs live in **LAM / Taskarid**. DevKit defines **format + Task → Patch → devkit/patch.sh linkage** only.

## 1. Non-goals (hard constraints)

DevKit **MUST NOT** be any of the following:

- task registry / task storage authority
- task runner / task orchestrator
- runtime logic / execution-path branching
- new directories, subtree, depot implementation, README wiring, templates

This contract is **contracts-first**, **observability-first**, **derivation-only**, and introduces **NO runtime logic** and **NO execution-path impact**.

## 2. Terminology

- **Task Spec** — a declarative description of an operation.
- **Patch** — an artifact that can be applied via `devkit/patch.sh` (the *only* canonical patch executor).
- **Derivation** — provenance metadata describing how the spec/patch was produced.

## 3. Representation

A Task Spec **MUST** be representable as a single YAML document (recommended) or a JSON-equivalent structure.

- YAML encoding **MUST** be UTF-8.
- Keys **MUST** be stable; unknown keys **MAY** be ignored by consumers, but **MUST NOT** change semantics of required fields.

## 4. Required top-level fields

| Field | Type | Requirement | Notes |
|---|---:|---|---|
| `api_version` | string | **MUST** | Contract version of this format (e.g. `v1`). |
| `kind` | string | **MUST** | Fixed value: `TaskSpec`. |
| `meta` | object | **MUST** | Identity, ownership, lifecycle. |
| `intent` | object | **MUST** | Human meaning: purpose + constraints summary. |
| `patch_plan` | object | **MUST** | Declarative mapping to patch application. |
| `observability` | object | **MUST** | Traceability & audit expectations. |
| `derivation` | object | **MUST** | Provenance and reproducibility metadata. |

## 5. Field contracts (normative)

### 5.1 `meta` (identity)
`meta` **MUST** contain:

- `id` (string): stable machine identifier for the task (unique within its domain).
- `title` (string): short human label.
- `owner` (string): responsible party (team/user/system).
- `created_at` (string, RFC3339): creation timestamp.
- `labels` (array of string, optional): search tags.

### 5.2 `intent` (meaning)
`intent` **MUST** contain:

- `summary` (string): what the task is meant to accomplish.
- `constraints` (array of string): explicit constraints (e.g. “no runtime logic”, “derivation-only”).
- `risk` (string, optional): risk class / impact narrative.

### 5.3 `patch_plan` (Task → Patch → devkit/patch.sh)
`patch_plan` **MUST** contain:

- `executor` (string): **MUST** be `devkit/patch.sh`.
- `patches` (array of object): one or more patch units.

Each element of `patches` **MUST** contain:

- `path` (string): repo-relative path to the patch artifact.
- `format` (string): patch encoding label (e.g. `git-patch`).
- `apply_mode` (string): declarative mode (e.g. `index`), with no runtime branching.
- `scope` (string, optional): brief target scope (files/modules impacted).

### 5.4 `observability` (auditability)
`observability` **MUST** contain:

- `trace_id` (string): correlation id to link logs/patch/provenance.
- `signals` (array of string): expected observable outputs (e.g. “git diff clean after apply”, “tests unchanged”).
- `audit` (object, optional): structured references (issue/PR links, change request id).

**Rule:** Observability fields are **declarative**. They describe what should be observable; they do not trigger behavior.

### 5.5 `derivation` (provenance)
`derivation` **MUST** contain:

- `source` (string): origin system (e.g. `LAM/Taskarid`).
- `inputs` (array of string, optional): identifiers/refs used to derive this spec.
- `method` (string): derivation method label.
- `reproducibility` (string): expectations for reproducing the same patch plan (e.g. “deterministic given inputs”).

## 6. Compatibility & evolution

- Consumers **MUST** reject specs where `kind != TaskSpec` or missing required fields.
- Backward-incompatible changes **MUST** bump `api_version`.
- Adding optional fields is allowed if it preserves semantics of required fields.

## 7. Safety invariants (DevKit boundary)

This contract **MUST NOT** imply or require DevKit to:
- fetch/store canonical task specs
- execute tasks beyond applying declared patches via `devkit/patch.sh`
- introduce any runtime execution path changes


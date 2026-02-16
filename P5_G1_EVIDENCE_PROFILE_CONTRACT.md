# P5.G1 Evidence Profile Contract (LAM)

## Purpose
Define governance-only evidence profile for future memory/retrieval phase5 execution tasks.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Evidence profile fields
- `evidence_id`: stable identifier for one evidence unit
- `operation_scope`: `memory` | `retrieval` | `memory+retrieval`
- `input_class`: short task classification label
- `evidence_source`: `memory` | `search` | `mixed` | `none`
- `evidence_status`: `available` | `partial` | `unavailable`
- `decision_note`: short rationale for the selected scope/source/status
- `decision_scope`: fixed value `governance-only`
- `timestamp_utc`: ISO format `YYYY-MM-DDTHH:MM:SSZ`

## Acceptance markers (governance-only)
- All markers are documentation-level checks:
  - marker A: fields present in governance record
  - marker B: values constrained to listed enums
  - marker C: UTC timestamp format is explicit
  - marker D: no runtime behavior claims in evidence note

## Non-goals
- No runtime instrumentation.
- No logger/adapter code changes.
- No enforcement pipeline.

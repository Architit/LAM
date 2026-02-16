# P4 Follow-up F4 Contract (Provider Metrics, Governance-Only)

## Purpose
Define normalized provider metrics contract and evidence template without changing runtime behavior.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This step defines metrics schema and governance evidence format only.

## Provider Metrics Contract Draft

### A) Normalized metrics set
- `provider_name` (string)
- `success_count` (int)
- `error_count` (int)
- `latency_ms_p50` (float)
- `latency_ms_p95` (float)
- `tokens_total` (int)
- `cost_usd_total` (float)
- `window_utc_start` (timestamp)
- `window_utc_end` (timestamp)

### B) Evidence template fields
- `trace_id` (optional)
- `intent_class` (optional)
- `provider_name`
- `status` (`ok|error`)
- `latency_ms`
- `tokens_total` (if available)
- `cost_usd_estimate` (if available)
- `reason_code`
- `timestamp_utc`

### C) Boundary rules
- Metrics contract is declarative in this phase.
- No collection agent/runtime hook is introduced by this contract.
- No execution-path behavior change is introduced.

## DoD (F4)
- D1: contract file is published and linked from DEV_MAP/ROADMAP.
- D2: normalized metrics schema and evidence template are fixed and auditable.
- D3: strict non-goal stated: no runtime behavior changes.

## Non-goals
- No adapter code changes.
- No policy.py behavior changes.
- No CI pipeline changes.

# P4.T2 Router Policy Profile Draft (ci/smoke parity)

## Purpose
Define a deterministic policy-profile draft for router behavior parity between CI and smoke governance runs.

This is a governance draft only:
- contracts-first
- observability-first
- derivation-only
- no runtime logic changes
- no execution-path impact

## Evidence Sources
- `LAM/default/agents/roaudter-agent/src/roaudter_agent/policy.py`
- `LAM/default/agents/roaudter-agent/src/roaudter_agent/registry.py`
- `scripts/test_entrypoint.sh`
- `P3_TEST_ENTRYPOINT_POLICY.md`

## Deterministic Policy Profile Draft

### A) Test profiles (execution contract)
- `ci`: minimal deterministic payload (3 tests) via `./devkit/check.sh --profile ci`.
- `smoke`: `ci` payload + runtime smoke test via `./devkit/check.sh --profile smoke`.

### B) Router hint profiles (selection contract)
- `local_only` -> chain starts with `ollama`.
- `cheap` -> `ollama -> gemini -> openai -> claude -> grok -> deepseek -> ollama_cloud`.
- `best` -> `claude -> openai -> gemini -> grok -> deepseek -> ollama -> ollama_cloud`.
- `fast` -> `gemini -> openai -> ollama -> claude -> grok -> deepseek -> ollama_cloud`.

### C) Strict selection
- `provider_hint` with `!` suffix (e.g. `openai!`) is strict:
  - no fallback
  - if unavailable, route returns error.

### D) Health/fallback boundary
- Health filtering is outside policy selection (`HealthMonitor` TTL/cooldown).
- Retry budget/backoff/fallback is router-level behavior (`RouterAgent.route`), not profile rewriting.

## P4.T2 DoD (Draft Completion)
- D1: Draft contract file exists and is referenced in governance maps.
- D2: Draft explicitly binds `ci/smoke` execution profiles to deterministic router profile semantics.
- D3: No runtime path/code change in this step.

## Non-Goals
- No provider order rewrites.
- No adapter parameter changes.
- No CI workflow modification.

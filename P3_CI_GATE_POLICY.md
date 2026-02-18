# P3.1 CI Gate Policy (devkit/check.sh)

## Purpose
Define the Phase 3.1 automation baseline for LAM CI using local DevKit gate commands.

## Scope
- Repository: `LAM` only.
- Policy layer only: no runtime-path logic changes.

## Gate Contract
- CI gate entrypoint: `./devkit/check.sh`.
- Bootstrap entrypoint: `./devkit/bootstrap.sh`.
- Python baseline: `3.12` (GitHub Actions CI).
- Bootstrap dependency source (mandatory): `requirements-dev.txt`.
- Required gate payload (current):
  - `tests/test_envelope_standard.py`
  - `tests/test_taskarid_comm_roaudter_trace.py`
  - `tests/test_comm_agent_envelope_enforcement.py`
- Required CI submodules (mandatory):
  - `LAM/default/agents/comm-agent`
  - `LAM/default/agents/codex-agent`
  - `LAM/default/agents/roaudter-agent`

## Submodule Integrity Rule (mandatory)
- Any submodule pointer used by `LAM` CI MUST resolve to a commit that is reachable on the remote submodule repository.
- Publish order is strict:
  1. push submodule commit to submodule remote branch;
  2. update pointer in `LAM`;
  3. push `LAM` branch.
- If any required submodule commit is unreachable, CI must fail in submodule init stage (fail-fast), not during test collection.

## Acceptance Criteria (DoD)
- `.github/workflows/ci.yml` uses local `devkit/bootstrap.sh` and local `devkit/check.sh`.
- Gate run is deterministic from repository content (no remote DevKit fetch in CI job).
- Required submodules are verified as initialized before test stage.
- `pytest` is available after bootstrap in CI runtime.
- Policy reflected in governance docs:
  - `DEV_MAP.md`
  - `DEV_LOGS.md`
  - `ROADMAP.md`
  - `WORKFLOW_SNAPSHOT_STATE.md`

## Non-Goals
- No expansion of test matrix in this step.
- No cross-repo rollout claims.
- No enforcement outside documented CI workflow.

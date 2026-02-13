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
- Required gate payload (current):
  - `tests/test_envelope_standard.py`
  - `tests/test_taskarid_comm_roaudter_trace.py`
  - `tests/test_comm_agent_envelope_enforcement.py`

## Acceptance Criteria (DoD)
- `.github/workflows/ci.yml` uses local `devkit/bootstrap.sh` and local `devkit/check.sh`.
- Gate run is deterministic from repository content (no remote DevKit fetch in CI job).
- Policy reflected in governance docs:
  - `DEV_MAP.md`
  - `DEV_LOGS.md`
  - `ROADMAP.md`
  - `WORKFLOW_SNAPSHOT_STATE.md`

## Non-Goals
- No expansion of test matrix in this step.
- No cross-repo rollout claims.
- No enforcement outside documented CI workflow.

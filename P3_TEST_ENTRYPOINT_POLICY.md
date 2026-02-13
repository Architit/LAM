# P3.2 Unified Test Entrypoint Policy

## Purpose
Define one reproducible test entrypoint contract for local runs and CI in LAM.

## Canonical Entrypoint
- `./devkit/check.sh` (delegates to `scripts/test_entrypoint.sh`).

## Profiles
- `ci`: deterministic CI payload.
- `smoke`: deterministic local smoke payload.
- `full`: full local test suite.

## Profile Definitions
- `ci`
  - `tests/test_envelope_standard.py`
  - `tests/test_taskarid_comm_roaudter_trace.py`
  - `tests/test_comm_agent_envelope_enforcement.py`
- `smoke`
  - CI payload +
  - `tests/test_runtime_smoke.py`
- `full`
  - `pytest -q` over full repository tests.

## Acceptance Criteria (DoD)
- CI workflow calls `./devkit/check.sh --profile ci`.
- Local reproducible smoke run exists via `./devkit/check.sh --profile smoke`.
- Governance docs reflect unified entrypoint and profile contract.

## Non-Goals
- No claim that `full` profile is always green in every environment.
- No cross-repo rollout changes in this step.

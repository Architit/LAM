# Runtime Proof Pytest Bootstrap Policy (P2.4 / Wave R5)

## Purpose
Define a minimal, deterministic bootstrap policy for repositories that have
`governance_done = DONE` but `runtime_proof = PENDING`.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This policy is governance-only. It does not enforce automation and does not
modify runtime code paths.

Interpretation:
- Python is the supported verification layer for runtime-proof evidence.
- Requirements below apply to CI/verification only.
- This is not a product runtime/execution-path requirement.

## Version Contract
- `python3 >= 3.10` is REQUIRED for runtime-proof validation.
- `pip` availability is REQUIRED for bootstrap (`python3 -m pip`).
- `pytest` is REQUIRED as the smoke test runner.

## Verification Boundary (Strict)
- `.venv` is the mandatory boundary for P2.4/R6 validation.
- Canonical runner: `.venv/bin/python -m pytest -q tests/test_runtime_smoke.py`.
- Fallback to system `python3` is NOT allowed for promotion evidence.

## Minimal Bootstrap Standard
For each target repository:
1. Ensure `python3` exists and satisfies version contract.
2. Create/refresh `.venv` (`python3 -m venv .venv`).
3. Ensure `.venv/bin/python -m pip` is available.
4. Install/upgrade `pytest` inside `.venv`.
5. Ensure `tests/test_runtime_smoke.py` exists (template in LAM).
6. Run `.venv/bin/python -m pytest -q tests/test_runtime_smoke.py`.
7. Record evidence (command, exit status, timestamp, branch, commit, python version).

## Acceptance
Runtime proof MAY be promoted from `PENDING` to `DONE` only when all facts are
documented in governance logs/checklists and are reproducible.

## Non-Goals
- No CI enforcement in this wave.
- No package manager standardization in this wave.
- No claims beyond observed repo facts.

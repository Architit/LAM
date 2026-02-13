# Runtime Proof Offline Wheelhouse Policy (P2.4 / R6.1)

## Purpose
Provide a deterministic fallback when `pytest` bootstrap from PyPI is blocked
by DNS/network limits during runtime-proof validation waves.

Hard constraints:
- contracts-first
- observability-first
- derivation-only
- NO runtime logic
- NO execution-path impact

## Scope
This policy applies to verification evidence for `runtime_proof` promotion.
It does not alter product runtime behavior.

## Offline Wheelhouse Contract
1. Prepare wheelhouse on a network-enabled host:
   - `python3 -m pip download --only-binary=:all: -d wheelhouse pytest`
2. Transfer `wheelhouse/` into target repo root.
3. Install in `.venv` without internet:
   - `.venv/bin/python -m pip install --no-index --find-links=wheelhouse pytest`
4. Verify runner:
   - `.venv/bin/python -m pytest --version`

## Evidence Requirements
- wheelhouse source details (host/date)
- install command used
- install result (success/failure)
- smoke run command/result

## Blocking Conditions
- `wheelhouse/` missing in offline mode
- `pytest` wheel missing or incompatible for local python/arch
- installation fails with `--no-index`

If blocked, `runtime_proof` remains `PENDING`.

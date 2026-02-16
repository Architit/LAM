# Runtime Proof Promotion Checklist (P2.4 / Wave R5)

Use this checklist before changing any repo status from `runtime_proof=PENDING`
to `runtime_proof=DONE`.

## Required Evidence
- [ ] Repository name
- [ ] Branch
- [ ] Commit hash used for validation
- [ ] Python version check (`python3 --version`, must be >= 3.10)
- [ ] `.venv` boundary confirmed (runner starts with `.venv/bin/python`)
- [ ] Test file path (`tests/test_runtime_smoke.py`)
- [ ] Runner command (`.venv/bin/python -m pytest -q tests/test_runtime_smoke.py`)
- [ ] Exit code (`0` required)
- [ ] UTC timestamp of execution
- [ ] Short output summary (pass/fail/skipped + reason)
- [ ] Governance note added to `DEV_LOGS.md` / rollout map
- [ ] If offline fallback used: wheelhouse path/source and `--no-index --find-links` command recorded

## Blocking Conditions
- `python3` missing or version < 3.10
- `.venv` missing or not used as runner boundary
- `pytest` unavailable and not bootstrapped
- offline mode selected but wheelhouse missing/incompatible
- smoke test file missing
- non-zero exit code
- evidence missing or non-reproducible

If any blocking condition is true, status remains `PENDING`.

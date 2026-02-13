# Runtime Proof Operator Blocks (P2.4 / Wave R5)

These blocks are copy-paste ready for downstream repositories.

Important:
- Closing heredoc markers must start at column 1 (no leading spaces/tabs).
- Use read-only checks before any edits.

## Block 1: Read-only Sync
```bash
pwd
git status -sb
git log -n 5 --oneline
```

## Block 2: Bootstrap `pytest` (online)
```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip --version
.venv/bin/python -m pip install -U pip pytest
.venv/bin/python -m pytest --version
```

## Block 2b: Bootstrap `pytest` (offline wheelhouse fallback)
```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip --version
test -d wheelhouse || { echo "wheelhouse missing"; exit 1; }
.venv/bin/python -m pip install --no-index --find-links=wheelhouse pytest
.venv/bin/python -m pytest --version
```

## Block 3: Seed smoke template
```bash
mkdir -p tests
cat > tests/test_runtime_smoke.py <<'PYEOF'
def test_runtime_smoke_marker():
    assert True
PYEOF
```

## Block 4: Execute smoke test
```bash
.venv/bin/python -m pytest -q tests/test_runtime_smoke.py
echo "exit_code=$?"
date -u +'%Y-%m-%dT%H:%M:%SZ'
git rev-parse --abbrev-ref HEAD
git rev-parse --short HEAD
.venv/bin/python --version
```

## Block 5: Evidence record skeleton
```bash
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
BR="$(git rev-parse --abbrev-ref HEAD)"
REV="$(git rev-parse --short HEAD)"
echo "- ${TS} | repo=<REPO> | branch=${BR} | rev=${REV} | test=tests/test_runtime_smoke.py | runner=.venv/bin/python -m pytest -q tests/test_runtime_smoke.py | py=$(.venv/bin/python --version 2>/dev/null | tr -d '\n') | exit_code=<CODE>" 
```

# P3.1 CI Gate Operator Blocks

Copy-paste blocks for local pre-push verification of CI gate behavior.

Important:
- Closing heredoc markers must start at column 1.
- Use quoted heredoc markers (`<<'EOF'`) for literal content with backticks.

## Block 1: Read-only sync
```bash
pwd
git status -sb
git log -n 5 --oneline
```

## Block 2: Local bootstrap
```bash
./devkit/bootstrap.sh
.venv/bin/python -m pytest --version
```

## Block 3: Verify required submodules are reachable
```bash
git submodule status LAM/default/agents/comm-agent
git submodule status LAM/default/agents/codex-agent
git submodule status LAM/default/agents/roaudter-agent
```

## Block 4: Run CI gate payload locally
```bash
./devkit/check.sh \
  tests/test_envelope_standard.py \
  tests/test_taskarid_comm_roaudter_trace.py \
  tests/test_comm_agent_envelope_enforcement.py
echo "exit_code=$?"
```

## Block 5: Evidence line
```bash
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
BR="$(git rev-parse --abbrev-ref HEAD)"
REV="$(git rev-parse --short HEAD)"
echo "- ${TS} | repo=LAM | branch=${BR} | rev=${REV} | gate=devkit/check.sh | payload=3-tests | exit_code=<CODE>"
```

# P3.2 Test Entrypoint Operator Blocks

## Block 1: Read-only sync
```bash
pwd
git status -sb
git log -n 5 --oneline
```

## Block 2: CI-equivalent gate
```bash
./devkit/check.sh --profile ci
echo "exit_code=$?"
```

## Block 3: Reproducible smoke profile
```bash
./devkit/check.sh --profile smoke
echo "exit_code=$?"
```

## Block 4: Explicit test list override
```bash
./devkit/check.sh \
  tests/test_envelope_standard.py \
  tests/test_taskarid_comm_roaudter_trace.py
echo "exit_code=$?"
```

## Block 5: Evidence line
```bash
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
BR="$(git rev-parse --abbrev-ref HEAD)"
REV="$(git rev-parse --short HEAD)"
echo "- ${TS} | repo=LAM | branch=${BR} | rev=${REV} | entrypoint=devkit/check.sh | profile=<ci|smoke|full> | exit_code=<CODE>"
```

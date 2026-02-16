# P4.T3 Router Operator Evidence Blocks (Governance-Only)

## Purpose
Provide deterministic, copy-paste operator blocks for P4 evidence capture without changing runtime logic.

Constraints:
- read-only sync first
- contracts-first
- observability-first
- derivation-only
- no runtime-path changes

## Block 1: Read-only sync
```bash
pwd
git status -sb
git log -n 12 --oneline
```

## Block 2: Policy/profile evidence (read-only)
```bash
rg -n "PROFILE_CHAINS|provider_hint|strict|model.*:cloud|intent" \
  LAM/default/agents/roaudter-agent/src/roaudter_agent/policy.py
```

## Block 3: Health/fallback evidence (read-only)
```bash
rg -n "ttl_seconds|cooldown_seconds|retry_max_attempts|retry_budget_ms|retry|fallback|roaudter\\.route|roaudter\\.result|roaudter\\.deliver" \
  LAM/default/agents/roaudter-agent/src/roaudter_agent/health.py \
  LAM/default/agents/roaudter-agent/src/roaudter_agent/router.py \
  LAM/default/agents/roaudter-agent/src/roaudter_agent/lam_entrypoint.py
```

## Block 4: ci/smoke profile evidence (read-only)
```bash
rg -n "profile=|--profile|ci\\)|smoke\\)|full\\)" scripts/test_entrypoint.sh devkit/check.sh
```

## Block 5: Optional verification run (non-mutating)
```bash
./devkit/check.sh --profile ci
echo "exit_code=$?"
./devkit/check.sh --profile smoke
echo "exit_code=$?"
```

## Block 6: Evidence line template
```bash
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
BR="$(git rev-parse --abbrev-ref HEAD)"
REV="$(git rev-parse --short HEAD)"
echo "- ${TS} | repo=LAM | branch=${BR} | rev=${REV} | phase=P4.T3 | evidence=router-policy+health-fallback+ci-smoke | exit_code=<CODE_OR_NA>"
```

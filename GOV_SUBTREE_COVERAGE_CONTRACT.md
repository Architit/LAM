# Governance Subtree Coverage Contract (LAM)

## Purpose
Provide facts-only coverage record for governance subtree artifacts:
- road/dev maps
- interaction protocols
- governance logs
- SoT ASR traceability

Hard constraints:
- governance-only
- derivation-only
- no runtime logic
- no execution-path impact

## Coverage scope
- Root docs:
  - `ROADMAP.md`
  - `DEV_MAP.md`
  - `DEV_LOGS.md`
  - `INTERACTION_PROTOCOL.md`
  - `INTERACTION_PROTOCOL_UPDATE_TEMPLATE.md`
  - `WORKFLOW_SNAPSHOT_STATE.md`
- Mirror docs:
  - `LAM/default/ROADMAP.md`
  - `LAM/default/DEV_MAP.md`
  - `LAM/default/DEV_LOGS.md`
- SoT ASR subtree:
  - `/home/architit/work/RADRILONIUMA-PROJECT/gov/asr/INDEX.md`
  - `/home/architit/work/RADRILONIUMA-PROJECT/gov/asr/sessions/*`

## Coverage matrix (facts-only)
1. Root governance maps/logs present and updated for latest Z.POST closure. PASS
2. Protocol + protocol update template present; template-backed update hard rule active. PASS
3. Root/default mirrors aligned on latest Z.POST and ASR sync markers. PASS
4. SoT ASR index contains latest LAM continuity sessions. PASS
5. Snapshot state includes current stage/next-target and SoT ASR references. PASS

## Residual note
- Mirror set intentionally covers maps/logs; `INTERACTION_PROTOCOL.md` has no `LAM/default` mirror by current repository design.

## Next target
- User-gated selection of first runtime-facing Z execution package (governance-only).

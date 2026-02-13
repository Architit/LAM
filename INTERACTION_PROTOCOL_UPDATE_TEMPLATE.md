# Interaction Protocol Update Template (LAM)

## Purpose
Template for deterministic updates to `INTERACTION_PROTOCOL.md` in governance-only mode.

## Update Record
- `update_id`:
- `timestamp_utc`:
- `author_scope`:
- `reason`:

## Change Scope
- `section_targets`: (e.g., `2`, `4.2`, `5.0`)
- `change_type`: `clarification` | `hard-rule` | `procedure` | `format`
- `impact_scope`: `governance-only`

## Required Assertions
- [ ] No runtime logic introduced.
- [ ] No execution-path impact introduced.
- [ ] `DEV_LOGS.md` updated before `ROADMAP.md`.
- [ ] `ROADMAP.md` updated before `INTERACTION_PROTOCOL.md`.
- [ ] `WORKFLOW_SNAPSHOT_STATE.md` refreshed after protocol update.

## Evidence
- `dev_logs_ref`:
- `roadmap_ref`:
- `protocol_ref`:
- `snapshot_ref`:

## Post-Update Gate
- `review_status`: `passed` | `needs-fix`
- `next_target`:

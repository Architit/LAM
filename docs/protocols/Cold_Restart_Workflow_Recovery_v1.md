# Cold Restart / Workflow Recovery Protocol (v1)

Applies when:
- device reboot
- terminal reset / new WSL session
- runtime environment lost

## 0. Guarantees
- All critical artifacts must live on disk (git).
- Nothing is assumed restored by default (cwd/branch/venv).
- Recovery is read-only first.

## 1. User Signal (mandatory)
Workflow resumes only after the user sends:
"вернулся, продолжаем Phase X.Y"

Without this signal, no commands are issued.

## 2. Assistant Context Re-Announcement (no commands)
Assistant must restate:
- Phase/Subphase
- last completed Action Block
- exact continuation point
- confirm cold restart mode

## 3. Environment Sync Block (read-only, max 2 commands)
- pwd
- git status -sb

Assistant pauses and waits for output.

## 4. Minimal Recovery Actions (only if required)
Only if the sync output demands it:
- cd into repo
- checkout the correct branch
- (optional) activate venv

Max 1–2 commands. No edits, tests, or commits here.

## 5. Resume Normal Workflow
Continue with standard cycle:
Context Sync → Action Block (1–3 cmds) → Safety Check → Verification → Governance

## Forbidden during recovery
- starting with write operations
- skipping Action Blocks
- mixing recovery + work changes

---

## Safety Check — Untracked Files (Addendum)

For newly created (untracked) files, an empty `git diff` on the first Safety Check is
**expected and correct behavior**.

### Required procedure
- If the file is untracked:
  - `git diff` MAY be empty — this is normal
  - The mandatory key diff MUST be performed via staged diff:
    ```bash
    git add <file>
    git diff --cached <file>
    ```
- A staged diff for new files is considered a **valid and complete Safety Check**.

This rule is mandatory for all contract-first workflows.

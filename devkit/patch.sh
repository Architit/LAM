#!/usr/bin/env bash
set -euo pipefail

# DevKit patch helper.
# Usage:
#   cat change.patch | devkit/patch.sh
# Applies patch via git in a reproducible way and stages the result (canonical diff).

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git not found in PATH" >&2
  exit 2
fi

# Must run inside a git worktree.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git repository" >&2
  exit 2
fi

# Read patch from stdin.
PATCH_FILE="$(mktemp)"
trap 'rm -f "$PATCH_FILE"' EXIT
cat > "$PATCH_FILE"

if [ ! -s "$PATCH_FILE" ]; then
  echo "ERROR: empty patch input" >&2
  exit 2
fi

# Apply and stage. Use 3-way merge to reduce false failures but still fail on conflicts.
git apply --index --3way "$PATCH_FILE"

echo "OK: patch applied and staged."
git diff --cached --stat

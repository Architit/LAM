#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "WORKFLOW_SNAPSHOT_STATE.md"


def _load_module():
    module_path = ROOT / "src" / "snapshot_pointer.py"
    spec = importlib.util.spec_from_file_location("snapshot_pointer_module", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load snapshot pointer module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: snapshot_active_target.py <active_next_target>", file=sys.stderr)
        return 2

    target = sys.argv[1].strip()
    if not target:
        print("active_next_target cannot be empty", file=sys.stderr)
        return 2

    mod = _load_module()
    text = SNAPSHOT.read_text(encoding="utf-8")
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    updated = mod.upsert_active_next_target(text, target, ts)
    SNAPSHOT.write_text(updated, encoding="utf-8")
    print(f"active_next_target={target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

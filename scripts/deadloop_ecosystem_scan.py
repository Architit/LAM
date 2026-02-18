#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCAN_FILES = [
    "DEV_LOGS.md",
    "ROADMAP.md",
    "TASK_LIST.md",
    "WORKFLOW_SNAPSHOT_STATE.md",
    "INTERACTION_PROTOCOL.md",
]


def _load_patterns_module() -> Any:
    module_path = ROOT / "src" / "deadloop_patterns.py"
    spec = importlib.util.spec_from_file_location("deadloop_patterns_mod", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load pattern module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _scan_repo(repo: Path, paths: list[str], pattern_mod: Any) -> dict[str, Any]:
    repo_hits: list[dict[str, Any]] = []
    for rel in paths:
        fp = repo / rel
        if not fp.exists() or not fp.is_file():
            continue
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        hits = pattern_mod.scan_text_for_patterns(lines)
        for h in hits:
            repo_hits.append(
                {
                    "file": str(fp),
                    "pattern_id": h.pattern_id,
                    "severity": h.severity,
                    "line_no": h.line_no,
                    "line": h.line,
                }
            )
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for h in repo_hits:
        sev = h["severity"]
        by_severity[sev] = by_severity.get(sev, 0) + 1
    return {"repo": str(repo), "hits": repo_hits, "summary": by_severity}


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="deadloop_ecosystem_scan",
        description="Scan ecosystem repos/files for deadloop risk patterns.",
    )
    parser.add_argument("--repo", action="append", default=[], help="Repo root path (repeatable).")
    parser.add_argument("--file", action="append", default=[], help="Relative file to scan (repeatable).")
    args = parser.parse_args()

    pattern_mod = _load_patterns_module()
    repos = [Path(p).resolve() for p in (args.repo or [str(ROOT)])]
    files = args.file or DEFAULT_SCAN_FILES

    results = [_scan_repo(repo, files, pattern_mod) for repo in repos]
    print(json.dumps({"scan": results}, ensure_ascii=False))

    has_critical = any(r["summary"].get("critical", 0) > 0 for r in results)
    return 7 if has_critical else 0


if __name__ == "__main__":
    raise SystemExit(main())

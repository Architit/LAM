"""Persistent metrics storage."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml


@dataclass
class Metrics:
    tests: int
    failures: int
    skipped: int


class MetricsStore:
    """Persist metrics as YAML."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def record(self, tests: int, failures: int, skipped: int) -> None:
        data = {"tests": tests, "failures": failures, "skipped": skipped}
        with open(self.path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(data, fh)

    def load(self) -> Metrics:
        if not self.path.exists():
            return Metrics(0, 0, 0)
        with open(self.path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        return Metrics(
            int(data.get("tests", 0)),
            int(data.get("failures", 0)),
            int(data.get("skipped", 0)),
        )

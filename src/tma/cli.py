"""Command line interface for TMA."""
from __future__ import annotations

import argparse
from pathlib import Path
import os

from .scheduler import schedule
from .storage import MetricsStore
from . import VERSION


def trigger(matrix: list[str]) -> None:
    schedule(matrix)


def status() -> None:
    report_dir = Path(os.getenv("TMA_REPORTS_DIR", "reports"))
    store = MetricsStore(report_dir / "metrics.yaml")
    metrics = store.load()
    print(metrics)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="tma")
    parser.add_argument("command", choices=["trigger", "status"])
    parser.add_argument("--matrix", nargs="*", default=[])
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    if args.command == "trigger":
        trigger(args.matrix)
    elif args.command == "status":
        status()


if __name__ == "__main__":
    main()

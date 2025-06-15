"""Collect test results into reports."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader
import os

from .storage import MetricsStore


def aggregate_results(matrix: list[str]) -> Dict[str, Any]:
    """Run pytest filtered by ``matrix`` and return metrics.

    Each entry in ``matrix`` is combined into a single expression passed to
    ``pytest`` via ``-k``. The values are also exposed as ``MATRIX_<index>``
    environment variables so tests may adapt behaviour based on the selected
    matrix options.
    """
    report_dir = Path(os.getenv("TMA_REPORTS_DIR", "reports"))
    report_dir = report_dir.expanduser()
    report_dir.mkdir(parents=True, exist_ok=True)
    xml_path = report_dir / "results.xml"
    html_path = report_dir / "results.html"

    cmd = ["pytest", "-q", f"--junitxml={xml_path}"]
    if matrix:
        expr = " and ".join(matrix)
        cmd += ["-k", expr]
    env = {**os.environ, **{f"MATRIX_{i}": v for i, v in enumerate(matrix)}}

    subprocess.run(cmd, check=False, env=env)

    tree = ET.parse(xml_path)
    root = tree.getroot()
    tests = int(root.attrib.get("tests", 0))
    failures = int(root.attrib.get("failures", 0))
    skipped = int(root.attrib.get("skipped", 0))
    store = MetricsStore(report_dir / "metrics.yaml")
    store.record(tests, failures, skipped)

    jinja_env = Environment(loader=FileSystemLoader(Path(__file__).parent))
    template = jinja_env.from_string(
        """<html><body><h1>Test Results</h1><pre>{{xml}}</pre></body></html>"""
    )
    html_path.write_text(template.render(xml=xml_path.read_text(encoding="utf-8")), encoding="utf-8")

    return {
        "tests": tests,
        "failures": failures,
        "skipped": skipped,
        "xml": str(xml_path),
        "html": str(html_path),
    }

"""Collect test results into reports."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader

from .storage import MetricsStore


def aggregate_results(matrix: list[str]) -> Dict[str, Any]:
    """Run pytest for given matrix and return metrics."""
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    xml_path = report_dir / "results.xml"
    html_path = report_dir / "results.html"

    subprocess.run(["pytest", "-q", f"--junitxml={xml_path}"], check=False)

    tree = ET.parse(xml_path)
    root = tree.getroot()
    tests = int(root.attrib.get("tests", 0))
    failures = int(root.attrib.get("failures", 0))
    skipped = int(root.attrib.get("skipped", 0))
    store = MetricsStore(report_dir / "metrics.yaml")
    store.record(tests, failures, skipped)

    env = Environment(loader=FileSystemLoader(Path(__file__).parent))
    template = env.from_string(
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

"""Celery-based scheduler using Redis broker."""
from __future__ import annotations

from celery import Celery
from typing import Any

from . import CONFIG
from .aggregator import aggregate_results


celery_app = Celery(
    "tma",
    broker=CONFIG.get("redis_url", "redis://localhost:6379/0"),
    backend=CONFIG.get("result_backend", CONFIG.get("redis_url", "redis://localhost:6379/0")),
)


@celery_app.task
def run_tests(matrix: list[str]) -> dict[str, Any]:
    """Run tests for a given matrix entry and return metrics."""
    return aggregate_results(matrix)


def schedule(matrix: list[str]) -> Any:
    """Enqueue test run."""
    return run_tests.delay(matrix)

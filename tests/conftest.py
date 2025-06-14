import asyncio
import importlib.util
import pytest


@pytest.fixture(autouse=True)
async def cleanup_tasks():
    """Wait briefly then cancel pending asyncio tasks after each test."""
    yield
    await asyncio.sleep(0.01)
    current = asyncio.current_task()
    tasks = [t for t in asyncio.all_tasks() if t is not current and not t.done()]
    for task in tasks:
        task.cancel()
    for task in tasks:
        try:
            await task
        except asyncio.CancelledError:
            pass


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "optional: test requires optional dependencies (opentelemetry-sdk)",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    try:
        sdk_spec = importlib.util.find_spec("opentelemetry.sdk")
    except ModuleNotFoundError:
        sdk_spec = None

    if sdk_spec is None:
        skip = pytest.mark.skip(reason="opentelemetry-sdk not installed")
        for item in items:
            if "optional" in item.keywords:
                item.add_marker(skip)

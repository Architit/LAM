import asyncio
import importlib.util
import os
import pytest
import aiohttp

pytest_asyncio = pytest.importorskip("pytest_asyncio")

# Deterministic local fallback for roaudter integration tests in constrained CI/sandbox.
os.environ.setdefault("ROAUDTER_OFFLINE_TEST_MODE", "1")


@pytest_asyncio.fixture(autouse=True)
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


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    try:
        sdk_spec = importlib.util.find_spec("opentelemetry.sdk")
    except ModuleNotFoundError:
        sdk_spec = None

    if sdk_spec is None:
        skip = pytest.mark.skip(reason="opentelemetry-sdk not installed")
        for item in items:
            if "optional" in item.keywords:
                item.add_marker(skip)


@pytest_asyncio.fixture()
async def http_client():
    """Yield a session and base url for an aiohttp app."""
    clients = []

    async def factory(
        app: "aiohttp.web.Application",
    ) -> tuple["aiohttp.ClientSession", str]:
        runner = aiohttp.web.AppRunner(app)
        await runner.setup()
        site = aiohttp.web.TCPSite(runner, "127.0.0.1", 0)
        try:
            await site.start()
        except OSError as exc:
            await runner.cleanup()
            pytest.skip(f"socket bind unavailable in this environment: {exc}")
        port = site._server.sockets[0].getsockname()[1]
        session = aiohttp.ClientSession()
        clients.append((runner, session))
        return session, f"http://127.0.0.1:{port}"

    yield factory

    for runner, session in clients:
        await session.close()
        await runner.cleanup()

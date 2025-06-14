import asyncio
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

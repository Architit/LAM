"""REST API exposing test triggers and metrics."""
from __future__ import annotations

import asyncio
from pathlib import Path
from aiohttp import web

from .scheduler import schedule
from .storage import MetricsStore


async def trigger_handler(request: web.Request) -> web.Response:
    matrix = await request.json()
    schedule(matrix.get("matrix", []))
    return web.json_response({"status": "scheduled"})


def metrics_handler(request: web.Request) -> web.Response:
    store = MetricsStore(Path("reports/metrics.yaml"))
    metrics = store.load().__dict__
    return web.json_response(metrics)


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/trigger", trigger_handler)
    app.router.add_get("/metrics", metrics_handler)
    return app


async def main() -> None:
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

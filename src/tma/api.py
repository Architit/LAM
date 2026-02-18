"""REST API exposing test triggers and metrics."""
from __future__ import annotations

import asyncio
from pathlib import Path
import os
from aiohttp import web

from .scheduler import schedule
from .storage import MetricsStore


async def trigger_handler(request: web.Request) -> web.Response:
    payload = await request.json()
    if not isinstance(payload, dict):
        raise web.HTTPBadRequest(reason="JSON body must be an object")

    matrix = payload.get("matrix", [])
    if not isinstance(matrix, list) or not all(isinstance(item, str) for item in matrix):
        raise web.HTTPBadRequest(reason="'matrix' must be a list of strings")

    schedule(matrix)
    return web.json_response({"status": "scheduled"})


async def metrics_handler(request: web.Request) -> web.Response:
    report_dir = Path(os.getenv("TMA_REPORTS_DIR", "reports"))
    store = MetricsStore(report_dir / "metrics.yaml")
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

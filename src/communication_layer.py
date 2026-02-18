# -*- coding: utf-8 -*-
"""External communication layer for LAM.

Provides simple helpers for interacting with third-party APIs. All
requests pass through this module allowing centralised auditing and
potential future enhancements such as rate limiting or asynchronous
operation.
"""

from __future__ import annotations

from typing import Any, Dict

import aiohttp
from opentelemetry import trace

from .logging_utils import get_json_logger

logger = get_json_logger(__name__)
tracer = trace.get_tracer(__name__)  # type: ignore[attr-defined]
_SENSITIVE_KEYS = {
    "authorization",
    "api_key",
    "token",
    "password",
    "secret",
    "access_token",
    "refresh_token",
}


def _sanitize(obj: Any) -> Any:
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for key, value in obj.items():
            if isinstance(key, str) and key.lower() in _SENSITIVE_KEYS:
                out[key] = "***"
            else:
                out[key] = _sanitize(value)
        return out
    if isinstance(obj, list):
        return [_sanitize(item) for item in obj]
    return obj


class CommunicationLayer:
    """Basic HTTP client used by LAM for outgoing requests.

    This class is designed to be used as an asynchronous context manager. A new
    :class:`aiohttp.ClientSession` is created on entering the context and
    properly closed on exit. This ensures that resources are correctly managed
    by callers without requiring explicit ``close`` calls.
    """

    def __init__(self) -> None:
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "CommunicationLayer":
        """Create the underlying HTTP session.

        Raises
        ------
        RuntimeError
            If the communication layer is already initialised.
        """
        if self._session is not None:
            raise RuntimeError("CommunicationLayer session already started")
        session = aiohttp.ClientSession()
        try:
            self._session = session
            return self
        except Exception:
            await session.close()
            self._session = None
            raise

    async def __aexit__(self, exc_type, exc, tb) -> bool:
        """Close the HTTP session on context exit."""
        try:
            return False
        finally:
            if self._session is not None:
                await self._session.close()
                self._session = None

    async def send_request(
        self, service: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a JSON POST request to ``service`` with ``payload``."""
        if self._session is None:
            raise RuntimeError(
                "CommunicationLayer is not initialised. Use 'async with'."
            )
        with tracer.start_as_current_span("send_request") as span:
            span.set_attribute("service", service)
            logger.info(
                "http_request",
                extra={"service": service, "payload": _sanitize(payload)},
            )
            async with self._session.post(
                service, json=payload, timeout=10
            ) as response:
                response.raise_for_status()
                text = await response.text()
                if not text:
                    return {}
                return await response.json()

    async def autonomous_interaction(
        self, service: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Initiate an outbound request without direct user prompting."""
        with tracer.start_as_current_span("autonomous_interaction"):
            return await self.send_request(service, payload)

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        if self._session is not None:
            await self._session.close()
            self._session = None


__all__ = ["CommunicationLayer"]

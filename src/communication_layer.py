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
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Close the HTTP session on context exit."""
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
        return await self.send_request(service, payload)

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        if self._session is not None:
            await self._session.close()
            self._session = None


__all__ = ["CommunicationLayer"]

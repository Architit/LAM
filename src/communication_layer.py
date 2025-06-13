# -*- coding: utf-8 -*-
"""External communication layer for LAM.

Provides simple helpers for interacting with third-party APIs. All
requests pass through this module allowing centralised auditing and
potential future enhancements such as rate limiting or asynchronous
operation.
"""

from __future__ import annotations

import json
from typing import Any, Dict

import aiohttp


class CommunicationLayer:
    """Basic HTTP client used by LAM for outgoing requests."""

    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    async def send_request(self, service: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON POST request to ``service`` with ``payload`` asynchronously."""
        async with self._session.post(service, json=payload, timeout=10) as response:
            response.raise_for_status()
            text = await response.text()
            if not text:
                return {}
            return await response.json()

    async def autonomous_interaction(self, service: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate an outbound request without direct user prompting."""
        return await self.send_request(service, payload)

    async def close(self) -> None:
        """Close the underlying HTTP session."""
        await self._session.close()


__all__ = ["CommunicationLayer"]

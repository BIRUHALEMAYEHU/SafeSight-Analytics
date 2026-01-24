from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Set

from fastapi import WebSocket


@dataclass(frozen=True)
class AlertMessage:
    """Structured alert payload for WebSocket clients."""

    type: str
    timestamp: str
    payload: Dict[str, Any]


class AlertStreamManager:
    """In-memory WebSocket connection manager for alert streaming."""

    def __init__(self) -> None:
        self._connections: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def connection_count(self) -> int:
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)

    async def broadcast(self, event_type: str, payload: Dict[str, Any]) -> None:
        message = AlertMessage(
            type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            payload=payload,
        )
        data = json.dumps(message.__dict__, default=str)

        async with self._lock:
            connections: List[WebSocket] = list(self._connections)

        stale: List[WebSocket] = []
        for websocket in connections:
            try:
                await websocket.send_text(data)
            except Exception:
                stale.append(websocket)

        if stale:
            async with self._lock:
                for websocket in stale:
                    self._connections.discard(websocket)


alert_stream = AlertStreamManager()

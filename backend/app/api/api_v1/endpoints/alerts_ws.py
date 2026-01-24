from typing import Any, Dict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from app.api.dependencies import require_role
from app.models.user import User as UserModel
from app.services.alert_stream import alert_stream

router = APIRouter()


@router.websocket("/stream")
async def alert_stream_ws(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time alert streaming."""
    await alert_stream.connect(websocket)
    try:
        while True:
            # Keep the connection alive and detect disconnects.
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await alert_stream.disconnect(websocket)


@router.post("/broadcast")
async def broadcast_alert(
    payload: Dict[str, Any],
    current_user: UserModel = Depends(require_role("admin"))
) -> Dict[str, Any]:
    """Broadcast a test alert to all connected WebSocket clients (admin only)."""
    await alert_stream.broadcast("alert", payload)
    return {
        "status": "sent",
        "connections": alert_stream.connection_count,
    }

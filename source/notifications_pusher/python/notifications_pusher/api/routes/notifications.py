from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from starlette.requests import Request

from notifications_pusher.logger import _logger
from notifications_pusher.api.utils.connection_manager import ConnectionManager, get_manager


router = APIRouter(prefix='/notifications')

@router.websocket("/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    manager: ConnectionManager = Depends(get_manager)
):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            _logger.error(data)
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
    except Exception as e:
        print(f"Unexpected error: {e}")
        await manager.disconnect(client_id)
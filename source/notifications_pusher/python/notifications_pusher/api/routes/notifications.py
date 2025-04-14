from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from starlette.requests import Request

from notifications_pusher.logger import _logger
from notifications_pusher.api.utils.connection_manager import ConnectionManager
from notifications_pusher.api.dependencies.get_current_user import get_current_user
from notifications_pusher.redis_utils.client import RedisClient


router = APIRouter(prefix='/notifications')
manager = ConnectionManager()

@router.websocket("/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    client_id: str,
    current_user: str = Depends(get_current_user)
):
    storage: RedisClient = websocket.app.state.redis_client
    await manager.connect(websocket, current_user, client_id, storage)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        _logger.error(f'{current_user} disconnected {client_id}')
        await manager.disconnect(client_id, current_user, storage)

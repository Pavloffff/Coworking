import asyncio

from fastapi import WebSocket
from starlette.websockets import WebSocketState

from notifications_pusher.logger import _logger
from notifications_pusher.redis_utils.client import RedisClient


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, current_user: str, client_id: str, storage: RedisClient):
        await websocket.accept()
        async with self.lock:
            _logger.error(current_user)
            self.active_connections[client_id] = websocket

    async def disconnect(self, client_id: str, storage: RedisClient):
        async with self.lock:
            websocket = self.active_connections.pop(client_id, None)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()
                
    # TODO: дописать
    async def send_to_user(self, storage: RedisClient, current_user: str):
        async with self.lock:
            pass

    async def send_to_client(self, message: str, client_id: str):
        async with self.lock:
            websocket = self.active_connections.get(client_id)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_text(message)

    async def broadcast(self, message: str):
        async with self.lock:
            for websocket in self.active_connections.values():
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_text(message)

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
            stored_data = await storage.get(current_user)
            if stored_data is not None:
                stored_data['connections'].append(client_id)
            else:
                stored_data = {'connections': [client_id]}
            await storage.put(current_user, stored_data)

    async def disconnect(self, client_id: str, current_user: str, storage: RedisClient):
        async with self.lock:
            websocket = self.active_connections.pop(client_id, None)
            stored_data = await storage.get(current_user)
            if stored_data is not None:
                connections = stored_data['connections']
                index = connections.index(client_id)
                connections = connections[:index] + connections[index+1:]
                stored_data['connections'] = connections
                await storage.put(current_user, stored_data)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()

    async def send_to_user(self, message: str, current_user: str, storage: RedisClient):
        async with self.lock:
            connections = await storage.get(current_user)
            if connections is not None:
                for conn in connections:
                    websocket = self.active_connections.get(conn)
                    if websocket and websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_text(message)        

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

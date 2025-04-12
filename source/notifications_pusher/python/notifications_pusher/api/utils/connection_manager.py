import asyncio

from fastapi import WebSocket
from starlette.websockets import WebSocketState
from contextlib import asynccontextmanager


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        async with self.lock:
            self.active_connections[client_id] = websocket

    async def disconnect(self, client_id: str):
        async with self.lock:
            websocket = self.active_connections.pop(client_id, None)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                await websocket.close()

    async def send_personal_message(self, message: str, client_id: str):
        async with self.lock:
            websocket = self.active_connections.get(client_id)
            if websocket and websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_text(message)

    async def broadcast(self, message: str):
        async with self.lock:
            for websocket in self.active_connections.values():
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_text(message)


@asynccontextmanager
async def get_connection_manager():
    manager = ConnectionManager()
    try:
        yield manager
    finally:
        pass

async def get_manager():
    async with get_connection_manager() as manager:
        yield manager

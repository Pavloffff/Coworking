from fastapi import Query, HTTPException, WebSocket, status
from fastapi.security import APIKeyHeader

from notifications_pusher.config import Config
from notifications_pusher.api.utils.token_processor import TokenProcessor


bearer_scheme = APIKeyHeader(name="Authorization", description="Bearer token")

async def get_current_user(
    websocket: WebSocket,
    token: str = Query(...),
) -> str:
    config: Config = websocket.app.state.config
    return TokenProcessor.verify(token, config.notifications_pusher_config.jwt_secret_key)

from fastapi import APIRouter
from .routes import (
    users,
    servers,
    activity_channels,
    chat_items,
    roles,
    user_roles,
    text_channels,
    voice_channels,
    user_servers
)

api_router = APIRouter()

api_router.include_router(users)
api_router.include_router(servers)
api_router.include_router(activity_channels)
api_router.include_router(chat_items)
api_router.include_router(roles)
api_router.include_router(text_channels)
api_router.include_router(voice_channels)
api_router.include_router(user_roles)
api_router.include_router(user_servers)

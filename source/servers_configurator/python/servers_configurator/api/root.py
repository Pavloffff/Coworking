from fastapi import APIRouter

from servers_configurator.api.routes import users

api_router = APIRouter()
api_router.include_router(users)

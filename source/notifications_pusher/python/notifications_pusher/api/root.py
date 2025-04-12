from fastapi import APIRouter
from .routes import notifications

api_router = APIRouter()

api_router.include_router(notifications)

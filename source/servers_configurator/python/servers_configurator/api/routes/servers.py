from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import UserScheme
from servers_configurator.password_utils.hasher import Hasher

router = APIRouter()


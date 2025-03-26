from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.models.message import Message

router = APIRouter()

@router.post('/send')
async def send_message(request: Request, message: Message):
    request.app.state.writer.write(message.model_dump())
    return message

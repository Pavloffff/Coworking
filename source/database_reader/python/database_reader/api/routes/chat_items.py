from fastapi import APIRouter, Depends
from starlette.requests import Request

from database_reader.api.dependencies.get_current_user import get_current_user
from database_reader.repositories.chat_item import ChatItemRepository


router = APIRouter(prefix='/chat-items')

@router.get('/text-channel')
async def get_text_channels_chat_items(
    request: Request,
    text_channel_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await ChatItemRepository.get_all(
            session=session,
            text_channel_id=text_channel_id
        )

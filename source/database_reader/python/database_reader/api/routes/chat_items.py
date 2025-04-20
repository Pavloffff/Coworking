from fastapi import APIRouter, Depends
from starlette.requests import Request

from database_reader.api.dependencies.get_current_user import get_current_user
from database_reader.repositories.chat_item import ChatItemRepository
from database_reader.repositories.user import UserRepository
from database_reader.schemas import ChatItemScheme


router = APIRouter(prefix='/chat-items')

@router.get('')
async def get_chat_items(
    request: Request,
    user_id: int = -1,
    text_channel_id: int = -1,
    text: str = '',
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await ChatItemRepository.get_all(
            session,
            user_id=user_id,
            text_channel_id=text_channel_id,
            text=text
        )

@router.get('/text-channel')
async def get_text_channels_chat_items(
    request: Request,
    text_channel_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        chat_items_data = await ChatItemRepository.get_all(
            session=session,
            text_channel_id=text_channel_id
        )
        chat_items = []
        for item in chat_items_data:
            user = await UserRepository.get(
                session, 
                user_id=item.user_id
            )
            chat_items.append(ChatItemScheme(
                chat_item_id=item.chat_item_id,
                text_channel_id=item.text_channel_id,
                text=item.text,
                file_url=item.file_url,
                user_data=f'{user.name}#{str(user.tag % 10000).zfill(4)}'
            ))
        return chat_items

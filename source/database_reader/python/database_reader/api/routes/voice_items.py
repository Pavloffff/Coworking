from fastapi import APIRouter, Depends
from starlette.requests import Request

from database_reader.api.dependencies.get_current_user import get_current_user
from database_reader.repositories.voice_item import VoiceItemRepository
from database_reader.schemas import VoiceItemScheme
from database_reader.repositories.user import UserRepository


router = APIRouter(prefix='/voice-items')

@router.get('')
async def get_voice_items(
    request: Request,
    user_id: int = -1,
    voice_channel_id: int = -1,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await VoiceItemRepository.get_all(
            session,
            user_id=user_id,
            voice_channel_id=voice_channel_id
        )

@router.get('/voice-channel')
async def get_voice_channels_voice_items(
    request: Request,
    voice_channel_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        voice_items_data = await VoiceItemRepository.get_all(
            session=session,
            voice_channel_id=voice_channel_id
        )
        voice_items = []
        for item in voice_items_data:
            user = await UserRepository.get(
                session,
                user_id=item.user_id
            )
            voice_items.append(VoiceItemScheme(
                voice_item_id=item.voice_item_id,
                voice_channel_id=item.voice_channel_id,
                user_id=user.user_id,
                user_data=f'{user.name}#{str(user.tag % 10000).zfill(4)}',
                server_id=0
            ))
        return voice_items

@router.get('{voice_item_id}')
async def get_voice_item(
    request: Request,
    voice_item_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await VoiceItemRepository.get(
            session,
            voice_item_id
        )

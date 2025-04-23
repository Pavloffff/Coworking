from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import VoiceItem, VoiceChannel
from database_configurator.repositories.base import BaseRepository


class VoiceItemRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        voice_channel_query = (
            select(VoiceChannel)
            .where(VoiceChannel.voice_channel_id == data['voice_channel_id'])
        )
        voice_channel = (await session.execute(voice_channel_query)).scalar_one_or_none()
        if voice_channel is None:
            return
        
        voice_item = VoiceItem(
            user_id=data['user_id'],
            voice_channel_id=data['voice_channel_id'],
        )
        session.add(voice_item)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(VoiceItem).where(VoiceItem.voice_item_id == data['voice_item_id'])
        await session.execute(statement=stmt)
        await session.commit()

    @staticmethod
    async def validate(session: AsyncSession, method: str, current_user: str, data: dict) -> bool:
        return True
    
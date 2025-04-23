from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import VoiceItem


class VoiceItemRepository:
    @staticmethod
    async def get_all(
        session: AsyncSession,
        voice_channel_id: int = -1,
        user_id: int = -1
    ):
        stmt = select(VoiceItem)
        if voice_channel_id > 0:
            stmt = stmt.where(VoiceItem.voice_channel_id == voice_channel_id)
        if user_id > 0:
            stmt = stmt.where(VoiceItem.user_id == user_id)
        response = await session.scalars(statement=stmt)
        return response.all()
    
    @staticmethod
    async def get(session: AsyncSession, voice_item_id: int) -> VoiceItem:
        stmt = select(VoiceItem).where(
            VoiceItem.voice_item_id == voice_item_id
        )
        response = await session.execute(stmt)
        return response.scalar_one_or_none()

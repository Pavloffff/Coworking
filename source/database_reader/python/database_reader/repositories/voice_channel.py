from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import VoiceChannel


class VoiceChannelRepository:
    @staticmethod
    async def get_all(session: AsyncSession, server_id: int = -1) -> VoiceChannel:
        stmt = select(VoiceChannel)
        if server_id > 0:
            stmt = stmt.where(VoiceChannel.server_id == server_id)
        response = await session.scalars(statement=stmt)
        return response.all()
    
    @staticmethod
    async def get(session: AsyncSession, voice_channel_id: int) -> VoiceChannel:
        stmt = select(VoiceChannel).where(
            VoiceChannel.voice_channel_id == voice_channel_id
        )
        response = await session.execute(stmt)
        return response.scalar_one_or_none()

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import VoiceChannel, Server
from database_configurator.repositories.base import BaseRepository


class VoiceChannelRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        server_query = select(Server).where(Server.server_id == data['server_id'])
        server = (await session.execute(server_query)).scalar_one_or_none()
        if server is None:
            return
        
        voice_channel = VoiceChannel(
            name=data['name'],
            server_id=data['server_id']
        )
        session.add(voice_channel)
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(VoiceChannel).where(VoiceChannel.voice_channel_id == data['voice_channel_id'])
        voice_channel = (await session.execute(query)).scalar_one_or_none()
        if voice_channel is None:
            return
        
        stmt = (
            update(VoiceChannel)
            .where(VoiceChannel.voice_channel_id == data['voice_channel_id'])
            .values(
                name=data['name']
            )
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(VoiceChannel).where(VoiceChannel.voice_channel_id == data['voice_channel_id'])
        await session.execute(stmt)
        await session.commit()

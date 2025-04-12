from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import TextChannel, Server
from database_configurator.repositories.base import BaseRepository


class TextChannelRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        server_query = select(Server).where(Server.server_id == data['server_id'])
        server = (await session.execute(server_query)).scalar_one_or_none()
        if server is None:
            return
        
        text_channel = TextChannel(
            name=data['name'],
            server_id=data['server_id']
        )
        session.add(text_channel)
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(TextChannel).where(TextChannel.text_channel_id == data['text_channel_id'])
        text_channel = (await session.execute(query)).scalar_one_or_none()
        if text_channel is None:
            return
        
        stmt = (
            update(TextChannel)
            .where(TextChannel.text_channel_id == data['text_channel_id'])
            .values(
                name=data['name']
            )
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(TextChannel).where(TextChannel.text_channel_id == data['text_channel_id'])
        await session.execute(stmt)
        await session.commit()
    
    @staticmethod
    async def validate(session: AsyncSession, method: str, current_user: str, data: dict) -> bool:
        return True

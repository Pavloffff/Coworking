from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import TextChannel


class TextChannelRepository:
    @staticmethod
    async def get_all(session: AsyncSession, server_id: int = -1):
        stmt = select(TextChannel)
        if server_id > 0:
            stmt = stmt.where(TextChannel.server_id == server_id)
        response = await session.scalars(statement=stmt)
        return response.all()

    @staticmethod
    async def get(session: AsyncSession, text_channel_id: int) -> TextChannel:
        stmt = select(TextChannel).where(
            TextChannel.text_channel_id == text_channel_id
        )
        response = await session.execute(stmt)
        return response.scalar_one_or_none()

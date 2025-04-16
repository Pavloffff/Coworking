from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import TextChannel


class TextChannelRepository:
    @staticmethod
    async def get_all(session: AsyncSession, server_id: int = -1) -> TextChannel:
        stmt = select(TextChannel)
        if server_id > 0:
            stmt = stmt.where(TextChannel.server_id == server_id)
        response = await session.scalars(statement=stmt)
        return response.all()

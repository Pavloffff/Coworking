from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import ChatItem


class ChatItemRepository:
    @staticmethod
    async def get_all(session: AsyncSession, text_channel_id: int = -1):
        stmt = select(ChatItem)
        if text_channel_id > 0:
            stmt = stmt.where(ChatItem.text_channel_id == text_channel_id)
        response = await session.scalars(statement=stmt)
        return response.all()

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import ChatItem


class ChatItemRepository:
    @staticmethod
    async def get_all(
        session: AsyncSession, 
        text_channel_id: int = -1, 
        text: str = '', 
        user_id: int = -1
    ):
        stmt = select(ChatItem)
        if text_channel_id > 0:
            stmt = stmt.where(ChatItem.text_channel_id == text_channel_id)
        if text != '':
            stmt = stmt.where(ChatItem.text == text)
        if user_id > 0:
            stmt = stmt.where(ChatItem.user_id == user_id)
        response = await session.scalars(statement=stmt)
        return response.all()
    
    @staticmethod
    async def get(session: AsyncSession, chat_item_id: int) -> ChatItem:
        stmt = select(ChatItem).where(
            ChatItem.chat_item_id == chat_item_id
        )
        response = await session.execute(stmt)
        return response.scalar_one_or_none()


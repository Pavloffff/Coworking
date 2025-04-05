from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import ChatItem, TextChannel
from database_configurator.repositories.base import BaseRepository


class ChatItemRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        text_channel_query = (
            select(TextChannel)
            .where(TextChannel.text_channel_id == data['text_channel_id'])
        )
        text_channel = (await session.execute(text_channel_query)).scalar_one_or_none()
        if text_channel is None:
            return
        
        chat_item = ChatItem(
            user_id=data['user_id'],
            text_channel_id=data['text_channel_id'],
            text=data['text'],
            file_url=data['file_url']
        )
        session.add(chat_item)
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(ChatItem).where(ChatItem.chat_item_id == data['chat_item_id'])
        chat_item = (await session.execute(query)).scalar_one_or_none()
        if chat_item is None:
            return
        
        stmt = (
            update(ChatItem)
            .where(ChatItem.chat_item_id == data['chat_item_id'])
            .values(
                text=data['text'],
                file_url=data['file_url']
            )
        )
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(ChatItem).where(ChatItem.chat_item_id == data['chat_item_id'])
        await session.execute(stmt)
        await session.commit()

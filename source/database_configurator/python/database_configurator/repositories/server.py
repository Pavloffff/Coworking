from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import Server, User
from database_configurator.repositories.base import BaseRepository


class ServerRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        owner_query = select(User).where(User.user_id == data['owner']['user_id'])
        owner = (await session.execute(owner_query)).scalar_one_or_none()
        if owner is None:
            return
        server = Server(
            owner_id=data['owner']['user_id'],
            name=data['name']
        )
        session.add(server)
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(Server).where(Server.server_id == data['server_id'])
        server = (await session.execute(query)).scalar_one_or_none()
        if server is None:
            return
        
        stmt = (
            update(Server)
            .where(Server.server_id == data['server_id'])
            .values(
                name=data['name']
            )
        )
        if data['owner']['user_id'] > 0:
            stmt = stmt.values(
                owner_id=data['owner']['user_id']
            )

        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(Server).where(Server.server_id == data['server_id'])
        await session.execute(stmt)
        await session.commit()

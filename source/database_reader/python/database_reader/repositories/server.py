from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import Server


class ServerRepository:
    @staticmethod
    async def get(session: AsyncSession, server_id: int) -> Server:
        stmt = select(Server).where(Server.server_id == server_id)
        response = await session.execute(stmt)
        return response.scalar_one_or_none()

    @staticmethod
    async def get_all(session: AsyncSession, name: str = '', server_id: int = -1):
        stmt = select(Server)
        if name != '':
            stmt = stmt.where(Server.name == name)
        if server_id > 0:
            stmt = stmt.where(Server.server_id == server_id)
        response = await session.scalars(statement=stmt)
        return response.all()

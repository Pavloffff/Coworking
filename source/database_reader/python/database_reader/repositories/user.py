from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import User

class UserRepository:
    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> User:
        stmt = select(User).where(User.user_id == user_id)
        return (await session.execute(stmt)).scalar_one_or_none()
    
    @staticmethod
    async def get_all(session: AsyncSession, email='', name='', tag=-1) -> list[User]:
        stmt = select(User)
        if email != '':
            stmt = stmt.where(User.email == email)
        if name != '':
            stmt = stmt.where(User.name == name)
        if tag >= 0:
            stmt = stmt.where(User.tag == tag)
        result = await session.scalars(statement=stmt)
        return result.all()

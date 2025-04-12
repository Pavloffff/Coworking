from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import User
from database_configurator.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        tag_query = select(func.max(User.tag)).limit(1)
        tag = ((await session.execute(tag_query)).scalar_one_or_none() or 0) + 1 
        user = User(
            name=data['name'],
            email=data['email'],
            avatar_url=data['avatar_url'],
            tag=tag,
            password_hash=data['password_hash'],
            password_salt=data['password_salt']
        )

        session.add(user)
        await session.commit()

    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(User).where(User.user_id == data['user_id'])
        user = (await session.execute(query)).scalar_one_or_none()    
        if user is None:
            return

        stmt = (
            update(User)
            .where(User.user_id == data['user_id'])
            .values(
                name=data['name'],
                email=data['email'],
                avatar_url=data['avatar_url']
            )
        )
        if data['password_hash'] != '':
            stmt = stmt.values(
                password_hash=data['password_hash'],
                password_salt=data['password_salt']
            )

        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(User).where(User.user_id == data['user_id'])
        await session.execute(stmt)
        await session.commit()
    
    @staticmethod
    async def validate(session: AsyncSession, method: str, current_user: str, data: dict) -> bool:
        return True

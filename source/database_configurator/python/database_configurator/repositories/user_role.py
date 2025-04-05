from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import UserRole, User, Role
from database_configurator.repositories.base import BaseRepository


class UserRoleRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        #TODO логику проверки вынести в отдельную утилиту database_utils.checker, сделать универсальную для всех классов
        user_query = select(User).where(User.user_id == data['user_id'])
        user = (await session.execute(user_query)).scalar_one_or_none()
        if user is None:
            return

        role_query = select(Role).where(Role.role_id == data['role_id'])
        role = (await session.execute(role_query)).scalar_one_or_none()
        if role is None:
            return
        
        user_role = UserRole(
            user_id=data['user_id'],
            role_id=data['role_id']
        )
        session.add(user_role)
        await session.commit()
        
    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(UserRole).where(UserRole.user_role_id == data['user_role_id'])
        user_role = (await session.execute(query)).scalar_one_or_none()
        if user_role is None:
            return
        
        stmt = (
            update(UserRole)
            .where(UserRole.user_role_id == data['user_role_id'])
            .values(
                user_id=data['user_id'],
                role_id=data['role_id']
            )
        )

        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(UserRole).where(Role.role_id == data['role_id'])
        await session.execute(stmt)
        await session.commit()

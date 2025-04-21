from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from database_configurator.repositories.base import BaseRepository
from database_configurator.repositories.user_role import UserRoleRepository
from database_configurator.models import Role, User


class UserServerRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        roles_stmt = select(Role).where(Role.server_id == data['server_id'])
        roles_stmt = roles_stmt.where(Role.name == 'common')
        roles_response = await session.execute(statement=roles_stmt)
        role = roles_response.scalar_one_or_none()
        user_name, user_tag = data['user_data'].split('#')
        user_stmt = select(User).where(User.name == user_name)
        user_response = await session.scalars(statement=user_stmt)
        users = user_response.all()
        target_user = None
        for user in users:
            if user.tag % 10000 == int(user_tag):
                target_user = user
                break
        if target_user is not None:
            await UserRoleRepository.insert(
                session=session,
                data={
                    'user_id': user.user_id,
                    'role_id': role.role_id
                }
            )

    @staticmethod
    async def update(session, data):
        return await super().update(session, data)

    @staticmethod
    async def delete(session, data):
        return await super().delete(session, data)
    
    # Этот метод для валидации ролей и прав доступа пользователей к БД
    @staticmethod
    async def validate(session: AsyncSession, method: str, current_user: str, data: dict) -> bool:
        return True

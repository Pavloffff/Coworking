from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import User, Right, Role, UserRole, RoleRight
from database_configurator.logger import _logger


class UserChecker:
    @staticmethod
    async def check(session: AsyncSession, current_user: str, server_id: int) -> list[Right]:
        user_query = select(User).where(User.email == current_user)
        user = (await session.execute(user_query)).scalar_one_or_none()
        if user is None:
            return []
        user_role_query = select(UserRole).where(UserRole.user_id == user.user_id)
        user_roles = (await session.execute(user_role_query)).all()
        role_ids = [user_role.role_id for user_role in user_roles]
        if server_id > 0:
            role_query = select(Role).where(
                (Role.server_id == server_id) & (Role.role_id.in_(role_ids))
            )
            role = (await session.execute(role_query)).scalar_one_or_none()
            if role is None:
                return []
            role_right_query = select(RoleRight).where(RoleRight.role_id == role.role_id)
            return list(
                (await session.execute(role_right_query)).all()
            )
        return ['write', 'speak']
    
    @staticmethod
    async def get_role(session: AsyncSession, current_user: str, server_id: int) -> str:
        user_query = select(User).where(User.email == current_user)
        user = (await session.execute(user_query)).scalar_one_or_none()
        user_role_query = select(UserRole).where(UserRole.user_id == user.user_id)
        user_roles = (await session.execute(user_role_query)).all()
        role_ids = [user_role[0].role_id for user_role in user_roles]
        role_query = select(Role).where(
            (Role.server_id == server_id) & (Role.role_id.in_(role_ids))
        )
        role = (await session.execute(role_query)).scalar_one_or_none()
        return role.name

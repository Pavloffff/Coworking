from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import User, Right, Role, UserRole, RoleRight


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
            role_query = select(Role).where(Role.server_id == server_id and Role.role_id in role_ids)
            role = (await session.execute(role_query)).scalar_one_or_none()
            if role is None:
                return []
            role_right_query = select(RoleRight).where(RoleRight.role_id == role.role_id)
            return list(
                (await session.execute(role_right_query)).all()
            )
        return ['write', 'speak']

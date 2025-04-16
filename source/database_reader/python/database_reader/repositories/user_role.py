from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import UserRole, User, Role


class UserRoleRepository:
    @staticmethod
    async def get_all(
        session: AsyncSession, 
        user_id: int = -1, 
        role_id: int = -1,
) -> list[UserRole]:
        stmt = select(UserRole)
        if user_id >= 0:
            stmt = stmt.where(UserRole.user_id == user_id)
        if role_id >= 0:
            stmt = stmt.where(UserRole.role_id == role_id)
        result = await session.scalars(statement=stmt)
        return result.all()

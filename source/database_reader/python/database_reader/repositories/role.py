from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import Role


class RoleRepository:
    @staticmethod
    async def get_all(session: AsyncSession, role_ids: list[int] = []) -> list[Role]:
        stmt = select(Role)
        if len(role_ids) > 0:
            stmt = stmt.where(Role.role_id.in_(role_ids))
        result = await session.scalars(statement=stmt)
        return result.all()

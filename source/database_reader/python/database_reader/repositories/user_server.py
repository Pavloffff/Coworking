from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_reader.models import UserRole, User
from database_reader.schemas.user_server import UserServer


class UserServerRepository:
    @staticmethod
    async def get(session: AsyncSession, user_data: str, server_id: int):
        user_name, user_tag = user_data.split('#')
        users_stmt = select(User).where(User.name == user_name)
        users_response = await session.scalars(statement=users_stmt)
        users = users_response.all()
        for user in users:
            if user.tag % 10000 == int(user_tag):
                return UserServer(
                    server_id=server_id,
                    user_data=user_data
                )

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import Server, User
from database_configurator.repositories.base import BaseRepository
from database_configurator.repositories.role import RoleRepository
from database_configurator.repositories.user_role import UserRoleRepository
from database_configurator.database_utils.user_checker import UserChecker


class ServerRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data: dict):
        owner_id = data['owner']['user_id']
        owner_query = select(User).where(User.user_id == owner_id)
        owner = (await session.execute(owner_query)).scalar_one_or_none()
        if owner is None:
            return
        server = Server(
            owner_id=owner_id,
            name=data['name']
        )
        session.add(server)
        await session.commit()
        await session.refresh(server)
        owner_role = await RoleRepository.insert(
            session=session,
            data={
                'server_id': server.server_id,
                'name': 'owner',
                'rights': list(
                    (await RoleRepository._get_all_rights(
                        session
                    )).keys()
                )
            }
        )
        await UserRoleRepository.insert(
            session=session,
            data={
                'user_id': owner_id,
                'role_id': owner_role.role_id
            }
        )
        await RoleRepository.insert(
            session=session,
            data={
                'server_id': server.server_id,
                'name': 'common',
                'rights': [
                    'write',
                    'speak'
                ]
            }
        )

    @staticmethod
    async def update(session: AsyncSession, data: dict):
        query = select(Server).where(Server.server_id == data['server_id'])
        server = (await session.execute(query)).scalar_one_or_none()
        if server is None:
            return
        
        stmt = (
            update(Server)
            .where(Server.server_id == data['server_id'])
            .values(
                name=data['name']
            )
        )
        if data['owner']['user_id'] > 0:
            stmt = stmt.values(
                owner_id=data['owner']['user_id']
            )

        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(Server).where(Server.server_id == data['server_id'])
        await session.execute(stmt)
        await session.commit()

    #TODO параллельно с фронтом смотреть на какие методы накладывать какую валидацию во всех репозиториях
    @staticmethod
    async def validate(session: AsyncSession, method: str, current_user: str, data: dict) -> bool:
        if method == 'add':
            return True
        return UserChecker.check(session, current_user, data['server_id'])

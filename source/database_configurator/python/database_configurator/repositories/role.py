from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.models import Server, Role, Right, RoleRight
from database_configurator.repositories.base import BaseRepository


class RoleRepository(BaseRepository):
    @staticmethod
    async def insert(session: AsyncSession, data):
        server_query = select(Server).where(Server.server_id == data['server_id'])
        server = (await session.execute(server_query)).scalar_one_or_none()
        if server is None:
            return
        
        rights: dict[str, int] = await RoleRepository._get_all_rights(session)
        rights_data = RoleRepository._check_rights(data['rights'], rights)
        if not rights_data[0]:
            return
        
        role = Role(
            name=data['name'],
            server_id=data['server_id']
        )
        session.add(role)
        await session.commit()
        await session.refresh(role)

        role_rights = RoleRepository._get_role_rights(role, rights_data[1])
        session.add_all(role_rights)
        await session.commit()
        return role

    @staticmethod
    async def update(session: AsyncSession, data):
        query = select(Role).where(Role.role_id == data['role_id'])
        role = (await session.execute(query)).scalar_one_or_none()
        if role is None:
            return
        
        rights: dict[str, int] = await RoleRepository._get_all_rights(session)
        rights_data = RoleRepository._check_rights(data['rights'], rights)
        if not rights_data[0]:
            return

        stmt = delete(RoleRight).where(RoleRight.role_id == data['role_id'])    
        await session.execute(stmt)

        stmt = (
            update(Role)
            .where(Role.role_id == data['role_id'])
            .values(
                name=data['name']
            )
        )

        await session.execute(stmt)
        role_rights = RoleRepository._get_role_rights(role, rights_data[1])
        session.add_all(role_rights)
        await session.commit()

    @staticmethod
    async def delete(session: AsyncSession, data: dict):
        stmt = delete(Role).where(Role.role_id == data['role_id'])
        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def _get_all_rights(session: AsyncSession):
        rights_query = select(Right)
        return {
            right[0].name: right[0].right_id for right in
            (await session.execute(rights_query)).all()
        }
    
    @staticmethod
    def _check_rights(rights_data: list[str], rights: dict[str, int]) -> tuple[bool, dict]:
        result = {}
        for right in rights_data:
            if right not in rights.keys():
                return False, {}
            result[right] = rights[right]
        return True, result
    
    @staticmethod
    def _get_role_rights(role: Role, rights: dict[str, int]) -> list[RoleRight]:
        role_rights: list[RoleRight] = []
        for _, right_id in rights.items():
            role_rights.append(RoleRight(
                role_id=role.role_id,
                right_id=right_id
            ))
        return role_rights

    @staticmethod
    async def validate(session: AsyncSession, method: str, current_user: str, data: dict) -> bool:
        return True

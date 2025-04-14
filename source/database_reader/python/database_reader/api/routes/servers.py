from fastapi import APIRouter, Depends
from starlette.requests import Request

from database_reader.api.dependencies.get_current_user import get_current_user
from database_reader.repositories import UserRepository, ServerRepository, UserRoleRepository, RoleRepository
from database_reader.models import Role


router = APIRouter(prefix='/servers')

@router.get('/user')
async def get_user_servers(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        user_data = await UserRepository.get_all(
            session,
            email=current_user
        )
        user = user_data[0]
        user_roles = await UserRoleRepository.get_all(
            session,
            user_id=user.user_id
        )
        role_ids = [user_role.role_id for user_role in user_roles]
        roles: list[Role] = await RoleRepository.get_all(
            session,
            role_ids=role_ids
        )
        servers = [
            await ServerRepository.get(session, server_id=role.server_id) for role in roles
        ]
        return servers

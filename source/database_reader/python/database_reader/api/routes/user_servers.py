from fastapi import APIRouter
from starlette.requests import Request

from database_reader.repositories.user_server import UserServerRepository


router = APIRouter(prefix='/user-servers')


@router.get('')
async def get_user_servers(
    request: Request,
    user_data: str = '',
    server_id: int = -1
):
    async with request.app.state.database_session() as session:
        user_server = await UserServerRepository.get(
            session,
            user_data,
            server_id
        )
        return [user_server]

from fastapi import APIRouter, Query, Depends
from starlette.requests import Request

from database_reader.api.dependencies.get_current_user import get_current_user
from database_reader.repositories.text_channel import TextChannelRepository


router = APIRouter(prefix='/text-channels')

@router.get('/server')
async def get_servers_text_channels(
    request: Request,
    server_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await TextChannelRepository.get_all(
            session,
            server_id=server_id
        )

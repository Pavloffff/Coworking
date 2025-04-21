from fastapi import APIRouter, Depends
from starlette.requests import Request

from servers_configurator.schemas import UserServerScheme
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user

router = APIRouter(prefix='/user-servers')


@router.post('/add')
async def add_user_server(
    request: Request,
    model: UserServerScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='user_server',
        model=model,
        method='add',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

@router.put('/update')
async def update_user_server(
    request: Request,
    model: UserServerScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='user_server',
        model=model,
        method='update',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

@router.delete('/delete')
async def delete_user_server(
    request: Request,
    model: UserServerScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='user_server',
        model=model,
        method='delete',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

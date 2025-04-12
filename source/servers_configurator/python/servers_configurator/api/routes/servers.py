from fastapi import APIRouter, Depends
from starlette.requests import Request

from servers_configurator.schemas import ServerScheme
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user


router = APIRouter(prefix='/servers')


@router.post('/add')
async def add_server(
    request: Request, 
    server: ServerScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='server',
        model=server,
        method='add',
        current_user=current_user
    )


@router.put('/update')
async def update_server(
    request: Request, 
    server: ServerScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='server',
        model=server,
        method='update',
        current_user=current_user
    )


@router.delete('/delete')
async def delete_server(
    request: Request,
    server: ServerScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='server',
        model=server,
        method='delete',
        current_user=current_user
    )

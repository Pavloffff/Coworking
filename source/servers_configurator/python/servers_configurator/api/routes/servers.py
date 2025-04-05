from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import ServerScheme
from servers_configurator.api.utils import Processor


router = APIRouter(prefix='/servers')


@router.post('/add')
async def add_server(request: Request, server: ServerScheme):
    return Processor.process_action(
        request=request,
        model_name='server',
        model=server,
        method='add'
    )


@router.put('/update')
async def update_server(request: Request, server: ServerScheme):
    return Processor.process_action(
        request=request,
        model_name='server',
        model=server,
        method='update'
    )


@router.delete('/delete')
async def delete_server(request: Request, server: ServerScheme):
    return Processor.process_action(
        request=request,
        model_name='server',
        model=server,
        method='delete'
    )

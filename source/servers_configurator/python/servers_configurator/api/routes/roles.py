from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import RoleScheme
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/roles')

@router.post('/add')
def add_role(request: Request, model: RoleScheme):
    return Processor.process_action(
        request=request,
        model_name='role',
        model=model,
        method='add'
    )

@router.put('/update')
def update_role(request: Request, model: RoleScheme):
    return Processor.process_action(
        request=request,
        model_name='role',
        model=model,
        method='update'
    )

@router.delete('/delete')
def delete_role(request: Request, model: RoleScheme):
    return Processor.process_action(
        request=request,
        model_name='role',
        model=model,
        method='delete'
    )

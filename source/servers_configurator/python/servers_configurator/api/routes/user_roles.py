from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import UserRoleScheme
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/user-roles')


@router.post('/add')
def add_user_role(request: Request, model: UserRoleScheme):
    return Processor.process_action(
        request=request,
        model_name='user_role',
        model=model,
        method='add'
    )

@router.put('/update')
def update_user_role(request: Request, model: UserRoleScheme):
    return Processor.process_action(
        request=request,
        model_name='user_role',
        model=model,
        method='update'
    )

@router.delete('/delete')
def delete_user_role(request: Request, model: UserRoleScheme):
    return Processor.process_action(
        request=request,
        model_name='user_role',
        model=model,
        method='delete'
    )

from fastapi import APIRouter, Depends
from starlette.requests import Request

from servers_configurator.schemas import RoleScheme
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user

router = APIRouter(prefix='/roles')

@router.post('/add')
async def add_role(
    request: Request, 
    model: RoleScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='role',
        model=model,
        method='add',
        current_user=current_user
    )

@router.put('/update')
async def update_role(
    request: Request, 
    model: RoleScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='role',
        model=model,
        method='update',
        current_user=current_user
    )

@router.delete('/delete')
async def delete_role(
    request: Request, 
    model: RoleScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='role',
        model=model,
        method='delete',
        current_user=current_user
    )

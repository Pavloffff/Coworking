from fastapi import APIRouter, Depends
from starlette.requests import Request

from servers_configurator.schemas import TextChannelScheme
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user

router = APIRouter(prefix='/text-channels')


@router.post('/add')
async def add_text_channel(
    request: Request,
    model: TextChannelScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='text_channel',
        model=model,
        method='add',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

@router.put('/update')
async def update_text_channel(
    request: Request,
    model: TextChannelScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='text_channel',
        model=model,
        method='update',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

@router.delete('/delete')
async def delete_text_channel(
    request: Request, 
    model: TextChannelScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='text_channel',
        model=model,
        method='delete',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

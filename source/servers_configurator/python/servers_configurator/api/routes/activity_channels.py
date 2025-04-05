from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import ActivityChannelScheme
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/activity-channels')

@router.post('/add')
async def add_activity_channel(request: Request, model: ActivityChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='activity_channel',
        model=model,
        method='add'
    )

@router.put('/update')
async def update_activity_channel(request: Request, model: ActivityChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='activity_channel',
        model=model,
        method='update'
    )

@router.delete('/delete')
async def delete_activity_channel(request: Request, model: ActivityChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='activity_channel',
        model=model,
        method='delete'
    )

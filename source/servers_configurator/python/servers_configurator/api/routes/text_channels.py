from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import TextChannelScheme
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/text-channels')


@router.post('/add')
def add_text_channel(request: Request, model: TextChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='text_channel',
        model=model,
        method='add'
    )

@router.put('/update')
def update_text_channel(request: Request, model: TextChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='text_channel',
        model=model,
        method='update'
    )

@router.delete('/delete')
def delete_text_channel(request: Request, model: TextChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='text_channel',
        model=model,
        method='delete'
    )

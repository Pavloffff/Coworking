from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import VoiceChannelScheme
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/voice-channels')


@router.post('/add')
async def add_voice_channel(request: Request, model: VoiceChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='voice_channel',
        model=model,
        method='add'
    )

@router.put('/update')
async def update_voice_channel(request: Request, model: VoiceChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='voice_channel',
        model=model,
        method='update'
    )

@router.delete('/delete')
async def delete_voice_channel(request: Request, model: VoiceChannelScheme):
    return Processor.process_action(
        request=request,
        model_name='voice_channel',
        model=model,
        method='delete'
    )

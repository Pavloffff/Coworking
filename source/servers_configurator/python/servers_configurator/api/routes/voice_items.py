from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from starlette.requests import Request

from servers_configurator.schemas import VoiceItemScheme
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user
from servers_configurator.logger import _logger


router = APIRouter(prefix='/voice-items')


@router.post('/add')
async def add_voice_item(
    request: Request,
    model: VoiceItemScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='voice_item',
        model=model,
        method='add',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

@router.put('/update')
async def update_voice_item(
    request: Request,
    model: VoiceItemScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='voice_item',
        model=model,
        method='update',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

@router.delete('/delete')
async def delete_voice_item(
    request: Request, 
    model: VoiceItemScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='voice_item',
        model=model,
        method='delete',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

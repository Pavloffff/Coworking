from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import ChatItemScheme
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/chat-items')

@router.post('/add')
def add_chat_item(request: Request, model: ChatItemScheme):
    return Processor.process_action(
        request=request,
        model_name='chat_item',
        model=model,
        method='add'
    )

@router.put('/update')
def update_chat_item(request: Request, model: ChatItemScheme):
    return Processor.process_action(
        request=request,
        model_name='chat_item',
        model=model,
        method='update'
    )

@router.delete('/delete')
def delete_chat_item(request: Request, model: ChatItemScheme):
    return Processor.process_action(
        request=request,
        model_name='chat_item',
        model=model,
        method='delete'
    )

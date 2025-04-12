import io
import json

from fastapi import APIRouter, File, UploadFile, Form, Depends
from fastapi.responses import StreamingResponse
from pydantic import parse_obj_as
from starlette.requests import Request

from servers_configurator.schemas import ChatItemScheme
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user
from servers_configurator.file_storage_utils import FileStorageClient


router = APIRouter(prefix='/chat-items')

@router.post('/add')
async def add_chat_item(
    request: Request, 
    file: UploadFile = File(None),
    model: str = Form(...),
    current_user: str = Depends(get_current_user)
):
    file_storage_client: FileStorageClient = request.app.state.file_storage_client
    
    model_dict = json.loads(model)
    model = ChatItemScheme(**model_dict)

    model: ChatItemScheme = parse_obj_as(ChatItemScheme, model)
    if file and model.file_url is not None:
        file_data = await file.read()
        model.file_url = file_storage_client.insert(file.filename, file_data)

    return Processor.process_action(
        request=request,
        model_name='chat_item',
        model=model,
        method='add',
        current_user=current_user
    )

@router.get('/file/{object_name}')
async def get_file(
    request: Request, 
    object_name: str,
    current_user: str = Depends(get_current_user)
):
    file_storage_client: FileStorageClient = request.app.state.file_storage_client
    file_data = file_storage_client.get(object_name)
    return StreamingResponse(
        io.BytesIO(file_data),
        media_type='application/octet-stream',
        headers={'Content-Disposition': f'attachment; filename={object_name}'}
    )

@router.put('/update')
async def update_chat_item(
    request: Request, 
    file: UploadFile = File(None),
    model: str = Form(...),
    current_user: str = Depends(get_current_user)
):
    model_dict = json.loads(model)
    model = ChatItemScheme(**model_dict)

    file_storage_client: FileStorageClient = request.app.state.file_storage_client
    model: ChatItemScheme = parse_obj_as(ChatItemScheme, model)
    if file and model.file_url is not None:
        file_data = await file.read()
        model.file_url = file_storage_client.insert(file.filename, file_data)

    #TODO удаление старого файла на database_configurator
    return Processor.process_action(
        request=request,
        model_name='chat_item',
        model=model,
        method='update',
        current_user=current_user
    )

@router.delete('/delete')
async def delete_chat_item(
    request: Request, 
    model: ChatItemScheme,
    current_user: str = Depends(get_current_user)
):
    file_storage_client: FileStorageClient = request.app.state.file_storage_client
    if model.file_url:
        file_storage_client.delete(model.file_url)
    return Processor.process_action(
        request=request,
        model_name='chat_item',
        model=model,
        method='delete',
        current_user=current_user
    )

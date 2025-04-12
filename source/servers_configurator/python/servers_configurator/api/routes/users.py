from fastapi import APIRouter, Depends
from starlette.requests import Request

from servers_configurator.schemas import UserScheme
from servers_configurator.password_utils.hasher import Hasher
from servers_configurator.api.utils import Processor
from servers_configurator.api.dependencies.get_current_user import get_current_user
from servers_configurator.logger import _logger

router = APIRouter(prefix='/users')


@router.post('/add')
async def add_user(
    request: Request, 
    user: UserScheme
):
    _logger.error(user)
    #TODO на database-configurator сделать проверку на существование юзера и добавление тега
    user.password_hash, user.password_salt = Hasher.hash(user.password_hash)
    return Processor.process_action(
        request=request,
        model_name='user',
        model=user,
        method='add',
        current_user=user.email,
        access_token=request.headers.get("Authorization")
    )


#TODO перед вызовом этого метода на фронте получить объект юзера с хешом и солью
@router.put('/update')
async def update_user(
    request: Request, 
    user: UserScheme,
    current_user: str = Depends(get_current_user)
):
    if user.password_hash != '':
        user.password_hash, user.password_salt = Hasher.hash(user.password_hash)
    return Processor.process_action(
        request=request,
        model_name='user',
        model=user,
        method='update',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )


@router.delete('/delete')
async def delete_user(
    request: Request,
    user: UserScheme,
    current_user: str = Depends(get_current_user)
):
    return Processor.process_action(
        request=request,
        model_name='user',
        model=user,
        method='delete',
        current_user=current_user,
        access_token=request.headers.get("Authorization")
    )

from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import UserScheme
from servers_configurator.password_utils.hasher import Hasher
from servers_configurator.api.utils import Processor

router = APIRouter(prefix='/users')


@router.post('/add')
async def add_user(request: Request, user: UserScheme):
    #TODO на database-configurator сделать проверку на существование юзера и добавление тега
    user.password_hash, user.password_salt = Hasher.hash(user.password_hash)
    return Processor.process_action(
        request=request,
        model_name='user',
        model=user,
        method='add'
    )


#TODO перед вызовом этого метода на фронте получить объект юзера с хешом и солью
@router.put('/update')
async def update_user(request: Request, user: UserScheme):
    if user.password_hash != '':
        user.password_hash, user.password_salt = Hasher.hash(user.password_hash)
    return Processor.process_action(
        request=request,
        model_name='user',
        model=user,
        method='update'
    )


@router.delete('/delete')
async def delete_user(request: Request, user: UserScheme):
    return Processor.process_action(
        request=request,
        model_name='user',
        model=user,
        method='delete'
    )

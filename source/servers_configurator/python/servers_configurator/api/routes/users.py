from fastapi import APIRouter
from starlette.requests import Request

from servers_configurator.schemas import UserScheme
from servers_configurator.password_utils.hasher import Hasher

router = APIRouter()


@router.post('/add')
async def add_user(request: Request, user: UserScheme):
    #TODO на database-configurator сделать проверку на существование юзера и добавление тега
    user.password_hash, user.password_salt = Hasher.hash(user.password_hash)
    message = {
        'method': 'add',
        'user': user.model_dump()
    }
    request.app.state.writer.write(message)
    return message
    

#TODO перед вызовом этого метода на фронте получить объект юзера с хешом и солью
@router.put('/update')
async def update_user(request: Request, user: UserScheme):
    user.password_hash, user.password_salt = Hasher.hash(user.password_hash)
    message = {
        'method': 'update',
        'user': user.model_dump()
    }
    request.app.state.writer.write(message)
    return message


@router.delete('/delete')
async def delete_user(request: Request, user: UserScheme):
    message = {
        'method': 'delete',
        'user': user.user_id
    }
    request.app.state.writer.write(message)
    return message
# Проверка пароля - в database_reader
# def verify_password(stored_hash, stored_salt, password, iterations):
#     salt = binascii.unhexlify(stored_salt)
#     new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
#     return stored_hash == binascii.hexlify(new_hash).decode()

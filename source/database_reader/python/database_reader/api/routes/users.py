import binascii
import hashlib
import binascii
from fastapi import APIRouter
from starlette.requests import Request

from database_reader.schemas import UserScheme
from database_reader.repositories import UserRepository
from database_reader.logger import _logger

router = APIRouter(prefix='/users')


@router.get('/{user_id}')
async def get_user(request: Request, user_id: int):
    session_pool = await request.app.state.database_session.create()
    async with session_pool() as session:
        return await UserRepository.get(session, user_id)

@router.get('')
async def get_users(request: Request, name='', tag=''):
    session_pool = await request.app.state.database_session.create()
    async with session_pool() as session:
        return await UserRepository.get_all(session, name, tag)

#TODO: добавить адрес электронной почты
@router.post('/login')
async def login(request: Request, user: UserScheme) -> bool:
    session_pool = await request.app.state.database_session.create()
    user_model = None
    async with session_pool() as session:
        users = await UserRepository.get_all(session, user.name, user.tag)
        _logger.error(users)
        if len(users) == 1:
            user_model = users[0]
    if user_model is None:
        return False
    iterations = 100000
    salt = binascii.unhexlify(user_model.password_salt)
    new_hash = hashlib.pbkdf2_hmac(
        'sha256', user.password_hash.encode(), salt, iterations
    )
    return user_model.password_hash == binascii.hexlify(new_hash).decode()

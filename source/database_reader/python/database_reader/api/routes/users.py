from fastapi import APIRouter
from starlette.requests import Request

from database_reader.schemas import UserScheme, AuthResponse
from database_reader.repositories import UserRepository
from database_reader.logger import _logger
from database_reader.config import Config
from database_reader.api.utils.password_hash_verifyer import PasswordHashVerifyer
from database_reader.api.utils.token_generator import TokenGenerator
from database_reader.redis_utils import RedisClient

router = APIRouter(prefix='/users')


@router.get('/{user_id}')
async def get_user(request: Request, user_id: int):
    session_pool = await request.app.state.database_session.create()
    async with session_pool() as session:
        return await UserRepository.get(session, user_id)

@router.get('')
async def get_users(request: Request, email='', name='', tag=''):
    session_pool = await request.app.state.database_session.create()
    async with session_pool() as session:
        return await UserRepository.get_all(session, email, name, tag)

#TODO: iterations вынести в конфиг
@router.post('/login')
async def login(request: Request, user: UserScheme) -> AuthResponse:
    config: Config = request.app.state.config
    redis_client: RedisClient = request.app.state.redis_client
    session_pool = await request.app.state.database_session.create()
    user_model = None
    async with session_pool() as session:
        users = await UserRepository.get_all(session, user.email)
        if len(users) > 0:
            user_model = users[0]
    if user_model is None:
        return AuthResponse(
            email=user.email,
            auth=False,
            access_token='',
            refresh_token=''    # not_a_secret
        )
    iterations = config.database_reader_config.password_hashing_iterations
    
    auth = PasswordHashVerifyer.verify(
        password=user.password_hash,
        password_hash=user_model.password_hash,
        salt_str=user_model.password_salt,
        iterations=iterations
    )
    refresh_token = TokenGenerator.generate(    # not_a_secret
        subject=user.email,
        expire=config.database_reader_config.refresh_token_expire_minutes,
        secret_key=config.database_reader_config.jwt_refresh_secret_key    
    )
    redis_client.put(
        user.email,
        {'refresh_token': refresh_token}    # not_a_secret
    )
    return AuthResponse(
        email=user.email,
        auth=auth,
        access_token=TokenGenerator.generate(
            subject=user.email,
            expire=config.database_reader_config.access_token_expire_minutes,
            secret_key=config.database_reader_config.jwt_secret_key
        ),
        refresh_token=refresh_token # not_a_secret
    )
    
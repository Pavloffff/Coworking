from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from database_reader.schemas import UserScheme, AuthResponse
from database_reader.repositories import UserRepository
from database_reader.logger import _logger
from database_reader.config import Config
from database_reader.api.utils.password_hash_verifyer import PasswordHashVerifyer
from database_reader.api.utils.token_processor import TokenProcessor
from database_reader.redis_utils import RedisClient
from database_reader.api.dependencies.get_current_user import get_current_user

router = APIRouter(prefix='/users')


@router.get('/{user_id}')
async def get_user(request: Request, user_id: int):
    session_pool = await request.app.state.database_session.create()
    async with session_pool() as session:
        return await UserRepository.get(session, user_id)

@router.get('')
async def get_users(
    request: Request,
    current_user: str = Depends(get_current_user),
    email='',
    name='',
    tag=-1
):
    session_pool = await request.app.state.database_session.create()
    async with session_pool() as session:
        return await UserRepository.get_all(session, email, name, tag)

@router.post('/login', response_model=AuthResponse)
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email"
        )
    
    iterations = config.database_reader_config.password_hashing_iterations
    
    auth = PasswordHashVerifyer.verify(
        password=user.password_hash,
        password_hash=user_model.password_hash,
        salt_str=user_model.password_salt,
        iterations=iterations
    )
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    refresh_token = TokenProcessor.generate(    # not_a_secret
        subject=user.email,
        expire=config.database_reader_config.refresh_token_expire_minutes,
        secret_key=config.database_reader_config.jwt_refresh_secret_key    
    )
    await redis_client.put(
        user.email,
        {'refresh_token': refresh_token}    # not_a_secret
    )
    return AuthResponse(
        email=user.email,
        auth=auth,
        access_token=TokenProcessor.generate(
            subject=user.email,
            expire=config.database_reader_config.access_token_expire_minutes,
            secret_key=config.database_reader_config.jwt_secret_key
        ),
        refresh_token=refresh_token # not_a_secret
    )

@router.post('/refresh')
async def refresh_token(
    request: Request,
    data: AuthResponse,
):
    config: Config = request.app.state.config
    redis_client: RedisClient = request.app.state.redis_client
    
    try:
        email = TokenProcessor.verify(
            token=data.refresh_token,
            secret_key=config.database_reader_config.jwt_refresh_secret_key
        )
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    stored_data = await redis_client.get(email)
    if not stored_data or stored_data.get("refresh_token") != data.refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token revoked")
    
    new_access_token = TokenProcessor.generate(
        subject=email,
        expire=config.database_reader_config.access_token_expire_minutes,
        secret_key=config.database_reader_config.jwt_secret_key
    )
    new_refresh_token = TokenProcessor.generate(
        subject=email,
        expire=config.database_reader_config.refresh_token_expire_minutes,
        secret_key=config.database_reader_config.jwt_refresh_secret_key    
    )
    await redis_client.put(email, {"refresh_token": new_refresh_token})
    
    return AuthResponse(
        email=email,
        auth=True,
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

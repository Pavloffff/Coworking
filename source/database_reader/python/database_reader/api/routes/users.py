from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from database_reader.schemas import UserScheme, AuthResponse
from database_reader.repositories import UserRepository, RoleRepository, UserRoleRepository
from database_reader.logger import _logger
from database_reader.config import Config
from database_reader.api.utils.password_hash_verifyer import PasswordHashVerifyer
from database_reader.api.utils.token_processor import TokenProcessor
from database_reader.redis_utils import RedisClient
from database_reader.api.dependencies.get_current_user import get_current_user

router = APIRouter(prefix='/users')

@router.get('/current')
async def get_user_by_token(
    request: Request, 
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        user_data = await UserRepository.get_all(session, email=current_user)
        return user_data[0]

# TODO сделать чтобы была мапа по ролям в ответе
@router.get('/server_id')
async def get_server_users(
    request: Request,
    server_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        roles = await RoleRepository.get_all(session, server_id=server_id)
        role_ids = [role.role_id for role in roles]
        user_roles = []
        for role_id in role_ids:
            user_roles_i = await UserRoleRepository.get_all(
                session,
                role_id=role_id
            )
            user_roles.extend(user_roles_i)
        user_ids = {user_role.user_id for user_role in user_roles}
        users = []
        for user_id in user_ids:
            users.append(
                await UserRepository.get(
                    session,
                    user_id=user_id
                )
            )
        return users

@router.get('/{user_id}')
async def get_user(
    request: Request, 
    user_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await UserRepository.get(session, user_id)

@router.get('')
async def get_users(
    request: Request,
    email: str = '',
    name: str = '',
    tag: int = -1
):
    _logger.error(email)
    _logger.error(name)
    _logger.error(tag)
    async with request.app.state.database_session() as session:
        _logger.error(type(tag))
        return await UserRepository.get_all(session, email, name, int(tag))

@router.post('/login', response_model=AuthResponse)
async def login(request: Request, user: UserScheme) -> AuthResponse:
    config: Config = request.app.state.config
    redis_client: RedisClient = request.app.state.redis_client
    user_model = None
    async with request.app.state.database_session() as session:
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
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

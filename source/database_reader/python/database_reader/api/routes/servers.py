from fastapi import APIRouter, Depends
from starlette.requests import Request

from database_reader.api.dependencies.get_current_user import get_current_user
from database_reader.repositories import (
    UserRepository, 
    ServerRepository, 
    UserRoleRepository, 
    RoleRepository, 
    TextChannelRepository, 
    ChatItemRepository,
    VoiceChannelRepository,
    VoiceItemRepository
)
from database_reader.models import Role
from database_reader.logger import _logger


router = APIRouter(prefix='/servers')

@router.get('')
async def get_servers(
    request: Request,
    name: str = '',
    server_id: int = -1,
    text_channel_id: int = -1,
    voice_channel_id: int = -1,
    chat_item_id: int = -1,
    voice_item_id: int = -1,
    user_id: int = -1,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        #TODO: переписать на нормальную архитектуру
        if text_channel_id > 0:
            text_channel = await TextChannelRepository.get(session, text_channel_id)
            return await ServerRepository.get_all(
                session,
                server_id=text_channel.server_id
            )
        elif voice_channel_id > 0:
            voice_channel = await VoiceChannelRepository.get(session, voice_channel_id)
            return await ServerRepository.get_all(
                session,
                server_id=voice_channel.server_id
            )
        elif chat_item_id > 0:
            chat_item = await ChatItemRepository.get(session, chat_item_id)
            text_channel = await TextChannelRepository.get(session, chat_item.text_channel_id)
            return await ServerRepository.get_all(
                session,
                server_id=text_channel.server_id
            )
        elif voice_item_id > 0:
            voice_item = await VoiceItemRepository.get(session, voice_item_id)
            voice_channel = await VoiceChannelRepository.get(session, voice_item.voice_channel_id)
            return await ServerRepository.get_all(
                session,
                server_id=voice_channel.server_id
            )
        elif user_id > 0:
            user_roles = await UserRoleRepository.get_all(
            session,
                user_id=user_id
            )
            role_ids = [user_role.role_id for user_role in user_roles]
            roles: list[Role] = await RoleRepository.get_all(
                session,
                role_ids=role_ids
            )
            servers = [
                await ServerRepository.get(session, server_id=role.server_id) for role in roles
            ]
            return servers
        else:
            return await ServerRepository.get_all(
                session,
                name=name,
                server_id=server_id
            )

@router.get('/user')
async def get_user_servers(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        user_data = await UserRepository.get_all(
            session,
            email=current_user
        )
        user = user_data[0]
        _logger.error(user)
        user_roles = await UserRoleRepository.get_all(
            session,
            user_id=user.user_id
        )
        _logger.error(user_roles)
        roles = set()
        for user_role in user_roles:
            role = await RoleRepository.get(session, user_role.role_id)
            roles.add(role)
        servers = [
            await ServerRepository.get(session, server_id=role.server_id) for role in roles
        ]
        return sorted(servers, key=lambda s: s.name)

@router.get('/{server_id}')
async def get_server(
    request: Request,
    server_id: int,
    current_user: str = Depends(get_current_user)
):
    async with request.app.state.database_session() as session:
        return await ServerRepository.get(session, server_id)

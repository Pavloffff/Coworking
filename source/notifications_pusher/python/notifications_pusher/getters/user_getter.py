import asyncio

from notifications_pusher.database_reader_utils.client import DatabaseReaderClient
from notifications_pusher.logger import _logger

class UserGetter:
    target_params = {
        'text_channel': 'text_channel_id',
        'voice_channel': 'voice_channel_id',
        'chat_item': 'chat_item_id',
        'voice_item': 'voice_item_id',
        'user': 'user_id',
        'server': 'server_id',
        'user_server': 'server_id'
    }

    @classmethod
    async def get(cls, client: DatabaseReaderClient, data: dict, model: str, access_token: str):
        _logger.error(f'BUG BUG BUG {data}')
        query_key = cls.target_params[model]
        params = {
            query_key: data[query_key]
        }
        _logger.error(params)
        servers = await client.get(
            endpoint='servers',
            params=params,
            access_token=access_token
        )
        users = []
        if servers is not None and isinstance(servers, list) and len(servers) > 0:
            for server in servers:
                server_users = await client.get(
                    endpoint=f'users/server_id?server_id={server["server_id"]}',
                    access_token=access_token
                )
                users.extend(server_users)
        return users

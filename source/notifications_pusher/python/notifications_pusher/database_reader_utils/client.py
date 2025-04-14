from aiohttp import ClientSession

from notifications_pusher.config.database_reader_config import DatabaseReaderConfig
from notifications_pusher.logger import _logger

class DatabaseReaderClient:
    def __init__(self, config: DatabaseReaderConfig):
        self._session = None
        self._url = f'http://{config.host}:{config.port}{config.api_v1_str}'

    async def get(self, endpoint: str, params: dict, access_token: str):
        session = await self._get_session()
        headers={}
        if access_token is not None:
            headers = {
                "Authorization": access_token
            }
        _logger.error(params)
        async with session.get(f'{self._url}/{endpoint}', params=params, headers=headers) as response:
            if response.status == 200:
                res_json = await response.json()
                _logger.error(res_json)
                return res_json
            else:
                return {'error': await response.text(encoding='utf-8')}

    async def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = ClientSession(trust_env=True)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

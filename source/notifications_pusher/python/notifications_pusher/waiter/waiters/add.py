import asyncio

from notifications_pusher.database_reader_utils.client import DatabaseReaderClient
from notifications_pusher.logger import _logger

#TODO эти константы передавать как параметры
RETRY_ATTEMPTS = 5
RETRY_TIMEOUT = 0.1

async def wait_add(client: DatabaseReaderClient, endpoint: str, data: dict, access_token: str):
    params = {}
    _logger.error(endpoint)
    endpoint = endpoint.replace('_', '-')
    for key, value in data.items():
        if key not in ['password_hash', 'password_salt'] and value is not None:
            if (isinstance(value, str) and value != '') or (isinstance(value, int) and value > 0):
                params[key] = value
    for _ in range(RETRY_ATTEMPTS):
        response = await client.get(endpoint=endpoint, params=params, access_token=access_token)
        _logger.error(response)
        if ((isinstance(response, dict) and 'error' in response.keys()) or 
            (isinstance(response, list) and len(response) == 0)):
            await asyncio.sleep(RETRY_TIMEOUT)
            continue
        return response, endpoint

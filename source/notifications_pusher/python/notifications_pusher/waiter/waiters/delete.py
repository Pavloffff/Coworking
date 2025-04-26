from notifications_pusher.database_reader_utils.client import DatabaseReaderClient
from notifications_pusher.logger import _logger

RETRY_ATTEMPTS = 5
RETRY_TIMEOUT = 0.1

#TODO: server_id вкинуть в schema, по нему и удалять
async def wait_delete(client: DatabaseReaderClient, endpoint: str, data: dict, access_token: str):
    for _ in range(RETRY_ATTEMPTS):
        response = await client.get(endpoint=f'{endpoint}/{id}', access_token=access_token)
        if 'error' in response.keys() and response['error'] == '{"detail":"Not Found"}':
            _logger.error(data['server_id'])
            return [{'server_id': data['server_id']}], 'server'

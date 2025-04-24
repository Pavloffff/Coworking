from notifications_pusher.database_reader_utils.client import DatabaseReaderClient
from notifications_pusher.logger import _logger

RETRY_ATTEMPTS = 5
RETRY_TIMEOUT = 0.1

#TODO: server_id вкинуть в schema, по нему и удалять
async def wait_delete(client: DatabaseReaderClient, endpoint: str, data: dict, access_token: str):
    id_str = endpoint[:-1] + '_id'
    id = data[endpoint[:-1] + '_id']
    _logger.error({id_str: id})
    servers = await client.get(
        endpoint='servers',
        params={id_str: id},
        access_token=access_token
    )
    _logger.error(servers)
    if len(servers) > 0:
        for _ in range(RETRY_ATTEMPTS):
            response = await client.get(endpoint=f'{endpoint}/{id}', access_token=access_token)
            if 'error' in response.keys() and response['error'] == '{"detail":"Not Found"}':
                _logger.error(servers[0]['server_id'])
                return [{'server_id': servers[0]['server_id']}]

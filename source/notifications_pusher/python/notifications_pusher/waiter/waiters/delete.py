from notifications_pusher.database_reader_utils.client import DatabaseReaderClient
from notifications_pusher.logger import _logger

RETRY_ATTEMPTS = 5
RETRY_TIMEOUT = 0.1


async def wait_delete(client: DatabaseReaderClient, endpoint: str, data: dict, access_token: str):
    pass

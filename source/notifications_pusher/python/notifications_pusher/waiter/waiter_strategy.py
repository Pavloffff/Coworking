from notifications_pusher.config import Config
from notifications_pusher.database_reader_utils.client import DatabaseReaderClient
from notifications_pusher.waiter.waiters import WAITERS


class WaiterStrategy:
    def __init__(self, config: Config):
        self._client = DatabaseReaderClient(
            config.database_reader_config
        )

    async def wait(self, model: str, method: str, data: dict, access_token: str):
        return await WAITERS[method](
            self._client,
            model + 's',
            data,
            access_token
        )

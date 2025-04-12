from notifications_pusher.config import Config
from notifications_pusher.kafka_utils import Reader
from notifications_pusher.logger import _logger
from notifications_pusher.waiter.waiter_strategy import WaiterStrategy


class NotificationsPusher:
    def __init__(self):
        self._config = Config.load()
        self._kafka_reader = Reader(
            config=self._config.kafka_config
        )
        self._waiter_strategy = WaiterStrategy(
            config=self._config
        )
    
    async def run(self):
        for message in self._kafka_reader.listen():
            try:
                _logger.error(f'Received message to push: {message}')
                await self._process_message(message)
            except Exception as ex:
                _logger.error(ex.with_traceback())
                continue
        
    async def _process_message(self, message: dict):
        model = message['model']
        method = message['method']
        data = message['data']
        access_token = message.get('access_token')
        
        response_flag = await self._waiter_strategy.wait(model, method, data, access_token)
        if response_flag:
            _logger.error(f'PUSHED {message}')

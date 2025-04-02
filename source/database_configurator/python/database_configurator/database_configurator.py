from database_configurator.config import Config
from database_configurator.logger import _logger
from database_configurator.kafka_utils import Reader
from database_configurator.database_session import DatabaseSession


class DatabaseConfigurator:
    def __init__(self):
        self._config: Config = Config.load()
        self._kafka_reader = Reader(
            config=self._config.kafka_config
        )
        self._session = DatabaseSession(
            config=self._config.database_config
        )
    
    async def run(self):
        session_pool = await self._session.create()
        for message in self._kafka_reader.listen():
            _logger.error(f'Received message: {message}')
            # _logger.error(f'{self._config.database_config.url}')
            _logger.error(session_pool.class_)

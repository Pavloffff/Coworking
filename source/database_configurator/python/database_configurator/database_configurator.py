from database_configurator.config import Config
from database_configurator.logger import _logger
from database_configurator.kafka_utils import Reader


class DatabaseConfigurator:
    def __init__(self):
        self._config: Config = Config.load()
        self._kafka_reader = Reader(
            config=self._config.kafka_config
        )
    
    def run(self):
        for message in self._kafka_reader.listen():
            _logger.error(f'Received message: {message}')
            _logger.error(f'{self._config.database_config.url}')

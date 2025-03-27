from database_configurator.config import _config
from database_configurator.logger import _logger
from database_configurator.kafka_utils import Reader, KafkaSettings


class DatabaseConfigurator:
    def __init__(self):
        self._kafka_reader = Reader(
            settings=KafkaSettings(
                host=_config.KAFKA_HOST,
                port=_config.KAFKA_PORT,
                topic='coworking_database_topic',
                initial_timeout=20,
                auto_offset_reset=_config.KAFKA_AUTO_OFFSET_RESET,
                enable_auto_commit=_config.KAFKA_ENABLE_AUTO_COMMIT,
                group_id=_config.KAFKA_GROUP_ID
            )
        )
    
    def run(self):
        for message in self._kafka_reader.listen():
            _logger.error(f'Received message: {message}')
        
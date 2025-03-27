import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from database_configurator.logger import _logger
from database_configurator.kafka_utils.settings import KafkaSettings

class Reader:
    def __init__(self, settings: KafkaSettings):
        self._host = settings.host
        self._port = settings.port
        self._topic = settings.topic
        self._initial_timeout = settings.initial_timeout
        self._auto_offset_reset = settings.auto_offset_reset
        self._enable_auto_commit = settings.enable_auto_commit
        self._group_id = settings.group_id
        self._codec = 'utf-8'
        self._consumer = self._connect()
        
    def _connect(self):
        while True:
            try:
                _logger.info(f"Attempt to connect to Kafka {self._host}:{self._port} ...")
                consumer = KafkaConsumer(
                    self._topic,
                    bootstrap_servers=[f'{self._host}:{self._port}'],
                    auto_offset_reset=self._auto_offset_reset,
                    enable_auto_commit=self._enable_auto_commit,
                    group_id=self._group_id
                )
                _logger.info("Connected to Kafka")
                return consumer
            except NoBrokersAvailable:
                _logger.warning("Kafka is not available. Retry at {self._initial_timeout} seconds")
                time.sleep(self._initial_timeout)

    def listen(self):
        for message in self._consumer:
            decoded_message = message.value.decode(self._codec)
            yield decoded_message

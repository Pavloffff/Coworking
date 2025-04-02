import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError

from servers_configurator.logger import _logger
from servers_configurator.config.kafka_config import KafkaConfig


class Writer:
    def __init__(self, settings: KafkaConfig):
        self._host = settings.host
        self._port = settings.port
        self._topic = settings.topic
        self._initial_timeout = settings.initial_timeout
        self._retry_timeout = settings.retry_timeout
        self._codec = 'utf-8'
        self._connect()

    def _connect(self):
        while True:
            try:
                _logger.debug(f"Attempt to connect to Kafka {self._host}:{self._port} ...")
                self._producer = KafkaProducer(
                    bootstrap_servers=[f'{self._host}:{self._port}']
                )
                _logger.debug("Connected to Kafka")
                break
            except NoBrokersAvailable:
                _logger.warning(f"Kafka is not available. Retry at {self._initial_timeout} seconds")
                time.sleep(self._initial_timeout)

    def write(self, message: dict):
        raw_message = json.dumps(message).encode(self._codec)
        while True:
            try:
                future = self._producer.send(self._topic, raw_message)
                result = future.get(timeout=self._retry_timeout)
                _logger.debug(f"Send message: {result}")
                break
            except KafkaError as e:
                _logger.error(f"Kafka send error: {e}")
                self._connect()
                time.sleep(self._retry_timeout)

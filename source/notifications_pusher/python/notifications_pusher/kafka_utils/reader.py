import time
import json
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from notifications_pusher.logger import _logger
from notifications_pusher.config.kafka_config import KafkaConfig


class Reader:
    def __init__(self, config: KafkaConfig):
        self._host = config.host
        self._port = config.port
        self._topic = config.topic
        self._initial_timeout = config.initial_timeout
        self._auto_offset_reset = config.auto_offset_reset
        self._enable_auto_commit = config.enable_auto_commit
        self._group_id = config.group_id
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
            decoded_message = json.loads(message.value.decode(self._codec))
            yield decoded_message

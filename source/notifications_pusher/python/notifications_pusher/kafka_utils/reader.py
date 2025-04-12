import asyncio
import json
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

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
        self._consumer = None

    async def _connect(self):
        while True:
            try:
                _logger.info(f"Connecting to Kafka {self._host}:{self._port}...")
                self._consumer = AIOKafkaConsumer(
                    self._topic,
                    bootstrap_servers=f'{self._host}:{self._port}',
                    auto_offset_reset=self._auto_offset_reset,
                    enable_auto_commit=self._enable_auto_commit,
                    group_id=self._group_id
                )
                await self._consumer.start()
                _logger.info("Connected to Kafka")
                return
            except KafkaError:
                _logger.warning(f"Kafka not available. Retrying in {self._initial_timeout} sec...")
                await asyncio.sleep(self._initial_timeout)

    async def listen(self):
        await self._connect()
        try:
            async for message in self._consumer:
                yield json.loads(message.value.decode())
        finally:
            await self._consumer.stop()
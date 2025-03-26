import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from database_configurator.logger import _logger

class Reader:
    def __init__(self, host: str, port: int, topic: str, group_id: str):
        self._host = host
        self._port = port
        self._topic = topic
        self._group_id = group_id
        self._codec = 'utf-8'
        self._consumer = self._connect()

    def _connect(self):
        """Подключается к Kafka, повторяя попытку при ошибке NoBrokersAvailable."""
        while True:
            try:
                _logger.info(f"Попытка подключения к Kafka по адресу {self._host}:{self._port} ...")
                consumer = KafkaConsumer(
                    self._topic,
                    bootstrap_servers=[f'{self._host}:{self._port}'],
                    auto_offset_reset='earliest',
                    enable_auto_commit=True,
                    group_id=self._group_id
                )
                _logger.info("Подключение к Kafka успешно!")
                return consumer
            except NoBrokersAvailable:
                _logger.warning("Kafka пока недоступна. Повторная попытка через 5 секунд...")
                time.sleep(5)

    def listen(self):
        """
        Блокирующий генератор, который возвращает сообщения по мере их поступления.
        Итерация по KafkaConsumer блокируется до появления нового сообщения.
        """
        for message in self._consumer:
            yield message

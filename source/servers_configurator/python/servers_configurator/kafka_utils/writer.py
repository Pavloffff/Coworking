import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError

from servers_configurator.logger import _logger

class Writer:
    def __init__(self, host: str, port: int, topic: str):
        self._host = host
        self._port = port
        self._topic = topic
        self._codec = 'utf-8'
        self._connect_producer()

    def _connect_producer(self):
        """Подключаемся к Kafka, повторяя попытку при ошибке NoBrokersAvailable."""
        while True:
            try:
                _logger.info(f"Попытка подключения к Kafka по адресу {self._host}:{self._port} ...")
                self._producer = KafkaProducer(
                    bootstrap_servers=[f'{self._host}:{self._port}']
                )
                _logger.info("Подключение к Kafka успешно!")
                break
            except NoBrokersAvailable:
                _logger.warning("Kafka пока недоступна. Повторная попытка через 5 секунд...")
                time.sleep(5)

    def write(self, message: dict):
        """Отправляет сообщение (dict) в Kafka в формате JSON с повторными попытками при ошибках."""
        raw_message = json.dumps(message).encode(self._codec)
        while True:
            try:
                # Отправляем сообщение и ждем подтверждения
                future = self._producer.send(self._topic, raw_message)
                result = future.get(timeout=10)
                _logger.info(f"Сообщение отправлено успешно: {result}")
                break
            except KafkaError as e:
                _logger.error(f"Ошибка при отправке сообщения в Kafka: {e}")
                _logger.info("Переподключаемся к Kafka и повторяем попытку через 5 секунд...")
                self._connect_producer()
                time.sleep(5)

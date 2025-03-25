import json

from kafka import KafkaConsumer


class Reader:
    def __init__(self, host: str, port: int, topic: str, group_id: str):
        # TODO: добавить класс для настроек кафки
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[f'{host}:{port}'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id
        )
        self._codec = 'utf-8'
        self._timeout = 1000

    def read(self, idx: int = -1):
        records = self._consumer.poll()
        return records.items()[idx].value.decode(self._codec)

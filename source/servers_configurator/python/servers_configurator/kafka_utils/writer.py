import json

from kafka import KafkaProducer


class Writer:
    def __init__(self, host: str, port: int, topic: str):
        self._producer = KafkaProducer(bootstrap_servers=[f'{host}:{port}'])
        self._topic = topic
        self._codec = 'utf-8'
    
    def write(self, message: dict):
        raw_message = json.dumps(message).encode(self._codec)
        self._producer.send(self._topic, raw_message)
        
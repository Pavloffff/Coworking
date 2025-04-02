from dataclasses import dataclass


@dataclass
class KafkaConfig:
    host: str
    port: int
    topic: str
    initial_timeout: int
    retry_timeout: int

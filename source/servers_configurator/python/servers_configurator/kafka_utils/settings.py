from dataclasses import dataclass

@dataclass
class KafkaSettings:
    host: str
    port: int
    topic: str
    initial_timeout: int
    retry_timeout: int

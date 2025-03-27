from dataclasses import dataclass

@dataclass
class KafkaSettings:
    host: str
    port: int
    topic: str
    initial_timeout: int
    auto_offset_reset: str
    enable_auto_commit: bool
    group_id: str

from dataclasses import dataclass


@dataclass
class KafkaConfig:
    host: str
    port: int
    topic: str
    group_id: str
    auto_offset_reset: str
    enable_auto_commit: bool

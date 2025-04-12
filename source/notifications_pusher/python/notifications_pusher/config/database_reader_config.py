from dataclasses import dataclass


@dataclass
class DatabaseReaderConfig:
    host: str
    port: int
    api_v1_str: str

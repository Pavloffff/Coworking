from dataclasses import dataclass


@dataclass
class DatabaseConfiguratorConfig:
    host: str
    port: int
    service_name: str

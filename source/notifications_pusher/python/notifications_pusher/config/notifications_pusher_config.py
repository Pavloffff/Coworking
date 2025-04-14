from dataclasses import dataclass


@dataclass
class NotificationsPusherConfig:
    service_name: str
    api_v1_str: str
    host: str
    port: int
    jwt_secret_key: str

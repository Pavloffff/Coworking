from dataclasses import dataclass


@dataclass
class ServersConfiguratorConfig:
    host: str
    port: int
    service_name: str
    api_v1_str: str
    jwt_secret_key: str
    jwt_refresh_secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

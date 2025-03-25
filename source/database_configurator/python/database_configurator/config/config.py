from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_GROUP_ID: str

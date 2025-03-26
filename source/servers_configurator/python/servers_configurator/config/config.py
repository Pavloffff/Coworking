from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    KAFKA_HOST: str = 'coworking-kafka'
    KAFKA_PORT: int = 9092

_config = Config()

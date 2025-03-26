from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    HOST: str = '0.0.0.0'
    PORT: int = 80
    KAFKA_HOST: str = 'coworking-kafka'
    KAFKA_PORT: int = 9092
    SERVICE_NAME: str = 'coworking-service-configurator'
    API_V1_STR: str = '/api/v1'

_config = Config()

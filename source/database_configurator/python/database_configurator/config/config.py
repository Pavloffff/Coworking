from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    # model_config['HOST'] - TODO add from venv and review
    HOST: str = '0.0.0.0'
    PORT: int = 80
    KAFKA_HOST: str = 'coworking-kafka'
    KAFKA_PORT: int = 9092
    KAFKA_GROUP_ID: str = 'coworking-postgres-group'
    KAFKA_AUTO_OFFSET_RESET: str = 'earliest'
    KAFKA_ENABLE_AUTO_COMMIT: bool = True
    DATABASE_URL: str = 'postgresql://postgres:mysecretpassword@coworking-database:5432/coworking'

_config = Config()

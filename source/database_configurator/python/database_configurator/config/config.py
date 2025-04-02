import os

from dataclasses import dataclass
from pathlib import Path

from database_configurator.config.kafka_config import KafkaConfig
from database_configurator.config.database_configurator_config import DatabaseConfiguratorConfig
from database_configurator.config.database_config import DatabaseConfig
from database_configurator.config.exceptions.improperly_configured import ImproperlyConfigured


@dataclass
class Config:
    database_configurator_config: DatabaseConfiguratorConfig
    kafka_config: KafkaConfig
    database_config: DatabaseConfig

    @classmethod
    def load(cls):
        return Config(
            database_configurator_config=DatabaseConfiguratorConfig(
                host=cls.getenv('HOST'),
                port=cls.getenv('PORT', int),
                service_name=cls.getenv('SERVICE_NAME')
            ),
            kafka_config=KafkaConfig(
                host=cls.getenv('KAFKA_HOST'),
                port=cls.getenv('KAFKA_PORT', int),
                topic=cls.getenv('KAFKA_DATABASE_TOPIC'),
                auto_offset_reset=cls.getenv('KAFKA_AUTO_OFFSET_RESET'),
                enable_auto_commit=cls.getenv('KAFKA_ENABLE_AUTO_COMMIT', bool),
            ),
            database_config=DatabaseConfig(
                driver=cls.getenv('DATABASE_DRIVER'),
                user=cls.getenv('DATABASE_USER') #TODO допилить
            )
        )
    
    @classmethod
    def getenv(cls, var_name: str, cast_to=str):
        try:
            value = os.environ[var_name]
            return cast_to(value)
        except KeyError:
            raise ImproperlyConfigured(var_name)
        except ValueError:
            raise ValueError(f"The value {var_name} can't be cast to {cast_to}.")

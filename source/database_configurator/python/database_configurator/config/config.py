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
                service_name=cls.getenv('SERVICE_NAME')
            ),
            kafka_config=KafkaConfig(
                host=cls.getenv('KAFKA_HOST'),
                port=cls.getenv('KAFKA_PORT', int),
                topic=cls.getenv('KAFKA_DATABASE_TOPIC'),
                auto_offset_reset=cls.getenv('KAFKA_AUTO_OFFSET_RESET'),
                enable_auto_commit=bool(cls.getenv('KAFKA_ENABLE_AUTO_COMMIT', int)),
                group_id=cls.getenv('KAFKA_DATABASE_GROUP_ID'),
                initial_timeout=cls.getenv('KAFKA_INITIAL_TIMEOUT')
            ),
            database_config=DatabaseConfig(
                user=cls.getenv('DATABASE_USER'),
                password=cls.getenv('DATABASE_PASSWORD'),
                host=cls.getenv('DATABASE_HOST'),
                port=cls.getenv('DATABASE_PORT', int),
                database=cls.getenv('DATABASE_NAME')
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

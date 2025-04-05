import os

from dataclasses import dataclass

from servers_configurator.config.kafka_config import KafkaConfig
from servers_configurator.config.file_storage_config import FileStorageConfig
from servers_configurator.config.servers_configurator_config import ServersConfiguratorConfig
from servers_configurator.config.exceptions.improperly_configured import ImproperlyConfigured


@dataclass
class Config:
    servers_configurator_config: ServersConfiguratorConfig
    kafka_config: KafkaConfig
    file_storage_config: FileStorageConfig

    @classmethod
    def load(cls):
        return Config(
            servers_configurator_config=ServersConfiguratorConfig(
                host=cls.getenv('HOST'),
                port=cls.getenv('PORT', int),
                service_name=cls.getenv('SERVICE_NAME'),
                api_v1_str=cls.getenv('API_V1_STR')
            ),
            kafka_config=KafkaConfig(
                host=cls.getenv('KAFKA_HOST'),
                port=cls.getenv('KAFKA_PORT', int),
                topic=cls.getenv('KAFKA_DATABASE_TOPIC'),
                initial_timeout=cls.getenv('KAFKA_INITIAL_TIMEOUT', int),
                retry_timeout=cls.getenv('KAFKA_RETRY_TIMEOUT', int)
            ),
            file_storage_config=FileStorageConfig(
                host=cls.getenv('FILE_STORAGE_HOST'),
                port=cls.getenv('FILE_STORAGE_PORT', int),
                access_key=cls.getenv('FILE_STORAGE_ACCESS_KEY'),
                secret_key=cls.getenv('FILE_STORAGE_SECRET_KEY'),
                bucket_name=cls.getenv('FILE_STORAGE_BUCKET_NAME')
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

import os

from dataclasses import dataclass

from database_reader.config.file_storage_config import FileStorageConfig
from database_reader.config.database_config import DatabaseConfig
from database_reader.config.database_reader_config import ServersConfiguratorConfig
from database_reader.config.exceptions.improperly_configured import ImproperlyConfigured


@dataclass
class Config:
    database_reader_config: ServersConfiguratorConfig
    database_config: DatabaseConfig
    file_storage_config: FileStorageConfig

    @classmethod
    def load(cls):
        return Config(
            database_reader_config=ServersConfiguratorConfig(
                host=cls.getenv('HOST'),
                port=cls.getenv('PORT', int),
                service_name=cls.getenv('SERVICE_NAME'),
                api_v1_str=cls.getenv('API_V1_STR')
            ),
            database_config=DatabaseConfig(
                user=cls.getenv('DATABASE_USER'),
                password=cls.getenv('DATABASE_PASSWORD'),
                host=cls.getenv('DATABASE_HOST'),
                port=cls.getenv('DATABASE_PORT', int),
                database=cls.getenv('DATABASE_NAME')
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

import os

from dataclasses import dataclass

from database_reader.config.file_storage_config import FileStorageConfig
from database_reader.config.database_config import DatabaseConfig
from database_reader.config.database_reader_config import DatabaseReaderConfig
from database_reader.config.redis_config import RedisConfig
from database_reader.config.exceptions.improperly_configured import ImproperlyConfigured


@dataclass
class Config:
    database_reader_config: DatabaseReaderConfig
    database_config: DatabaseConfig
    file_storage_config: FileStorageConfig
    redis_config: RedisConfig

    @classmethod
    def load(cls):
        return Config(
            database_reader_config=DatabaseReaderConfig(
                host=cls.getenv('HOST'),
                port=cls.getenv('PORT', int),
                service_name=cls.getenv('SERVICE_NAME'),
                api_v1_str=cls.getenv('API_V1_STR'),
                jwt_secret_key=cls.getenv('JWT_SECRET_KEY'),
                jwt_refresh_secret_key=cls.getenv('JWT_REFRESH_SECRET_KEY'),
                access_token_expire_minutes=cls.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', int),
                refresh_token_expire_minutes=cls.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', int),
                password_hashing_iterations=cls.getenv('PASSWORD_HASHING_ITERATIONS', int)
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
            ),
            redis_config=RedisConfig(
                host=cls.getenv('REDIS_HOST'),
                port=cls.getenv('REDIS_PORT', int),
                password=cls.getenv('REDIS_PASSWORD'),
                db=cls.getenv('REDIS_DB', int)
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

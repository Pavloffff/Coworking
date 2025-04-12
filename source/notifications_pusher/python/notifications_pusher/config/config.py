import os

from dataclasses import dataclass

from notifications_pusher.config.kafka_config import KafkaConfig
from notifications_pusher.config.notifications_pusher_config import NotificationsPusherConfig
from notifications_pusher.config.exceptions.improperly_configured import ImproperlyConfigured
from notifications_pusher.config.database_reader_config import DatabaseReaderConfig


@dataclass
class Config:
    notifications_pusher_config: NotificationsPusherConfig
    kafka_config: KafkaConfig
    database_reader_config: DatabaseReaderConfig

    @classmethod
    def load(cls):
        return Config(
            notifications_pusher_config=NotificationsPusherConfig(
                service_name=cls.getenv('SERVICE_NAME'),
                api_v1_str=cls.getenv('API_V1_STR'),
                host=cls.getenv('HOST'),
                port=cls.getenv('PORT', int)
            ),
            kafka_config=KafkaConfig(
                host=cls.getenv('KAFKA_HOST'),
                port=cls.getenv('KAFKA_PORT', int),
                topic=cls.getenv('KAFKA_DATABASE_TOPIC'),
                auto_offset_reset=cls.getenv('KAFKA_AUTO_OFFSET_RESET'),
                enable_auto_commit=bool(cls.getenv('KAFKA_ENABLE_AUTO_COMMIT', int)),
                group_id=cls.getenv('KAFKA_NOTIFICATIONS_GROUP_ID'),
                initial_timeout=cls.getenv('KAFKA_INITIAL_TIMEOUT', int)
            ),
            database_reader_config=DatabaseReaderConfig(
                host=cls.getenv('DATABASE_READER_HOST'),
                port=cls.getenv('DATABASE_READER_PORT', int),
                api_v1_str=cls.getenv('DATABASE_READER_ENDPOINT')
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

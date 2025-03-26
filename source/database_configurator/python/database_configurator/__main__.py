from database_configurator.logger import _logger

from database_configurator.config import _config
from database_configurator.kafka_utils import Reader

def main():
    reader = Reader(
        host=_config.KAFKA_HOST,
        port=_config.KAFKA_PORT,
        group_id=_config.KAFKA_GROUP_ID,
        topic='coworking_database_topic'
    )
    for msg in reader.listen():
        decoded = msg.value.decode(reader._codec)
        _logger.error(f"Получено сообщение: {decoded}")

if __name__ == "__main__":
    main()

import time
import random

from servers_configurator.config import _config
from servers_configurator.kafka_utils import Writer

from servers_configurator.logger import _logger

def main():
    writer = Writer(
        host=_config.KAFKA_HOST,
        port=_config.KAFKA_PORT,
        topic='database_topic'
    )
    while True:
        time.sleep(1)
        _logger.debug({'message': random.randrange(0, 10)})
        writer.write({'message': random.randrange(0, 10)})

if __name__ == "__main__":
    main()

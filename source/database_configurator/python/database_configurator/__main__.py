from database_configurator.kafka_utils import Reader
from database_configurator.logger import _logger

def main():
    reader = Reader()
    while True:
        _logger.info(reader.read())

if __name__ == "__main__":
    main()

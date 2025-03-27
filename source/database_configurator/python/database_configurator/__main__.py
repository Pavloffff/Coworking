from database_configurator.logger import _logger

from database_configurator.config import _config
from database_configurator.kafka_utils import Reader
from database_configurator.database_configurator import DatabaseConfigurator


if __name__ == "__main__":
    app = DatabaseConfigurator()
    app.run()

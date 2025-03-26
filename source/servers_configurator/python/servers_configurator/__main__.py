import time
import random


from servers_configurator.logger import _logger
from servers_configurator.servers_configurator import ServersConfigurator


if __name__ == "__main__":
    _logger.info('Starting database configurator')
    app = ServersConfigurator()
    app.run()

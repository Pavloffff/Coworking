import asyncio

from database_configurator.logger import _logger
from database_configurator.database_configurator import DatabaseConfigurator


if __name__ == "__main__":
    app = DatabaseConfigurator()
    asyncio.run(app.run())

import asyncio

from database_configurator.logger import _logger
from database_configurator.database_configurator import DatabaseConfigurator


if __name__ == "__main__":
    app = DatabaseConfigurator()
    app.run()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        _logger.info("Shutting down database configurator...")
    except Exception as e:
        _logger.error(f"Critical error: {e}")

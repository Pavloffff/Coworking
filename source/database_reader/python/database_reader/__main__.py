from database_reader.logger import _logger
from database_reader.database_reader import DatabaseReader


if __name__ == "__main__":
    _logger.info('Starting database reader')
    app = DatabaseReader()
    app.run()

from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.config import Config
from database_configurator.logger import _logger
from database_configurator.kafka_utils import Reader
from database_configurator.database_session import DatabaseSession
from database_configurator.repositories import RepositoriesFactory

#TODO вернуть логгеры все на INFO
class DatabaseConfigurator:
    def __init__(self):
        self._config: Config = Config.load()
        self._kafka_reader = Reader(
            config=self._config.kafka_config
        )
        self._session = DatabaseSession(
            config=self._config.database_config
        )
    
    async def run(self):
        session_pool = await self._session.create()
        async with session_pool() as session:
            for message in self._kafka_reader.listen():
                try:
                    _logger.error(f'Received message: {message}')
                    await self._process_message(session, message)
                except Exception as ex:
                    _logger.error(ex.with_traceback())
                    continue

    async def _process_message(self, session: AsyncSession, message: dict):
        model = message['model']
        method = message['method']
        data = message['data']
        current_user = message['current_user']
        data['current_user'] = current_user
        
        repository = RepositoriesFactory.get_repository(model)
        
        if not (await repository.validate(session, method, current_user, data)):
            raise ValueError(f'Invalid user: {current_user}')

        action_methods = {
            'add': repository.insert,
            'update': repository.update,
            'delete': repository.delete
        }
        
        if method not in action_methods:
            raise ValueError(f"Unknown method: {method}")
        
        result = await action_methods[method](session, data)
        _logger.error(f"Successfully processed {method} for {model}: {result}")
            

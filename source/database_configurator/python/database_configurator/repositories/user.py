from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database_configurator.repositories.repository import Repository
from database_configurator.models import User
from database_configurator.schemas import UserScheme 

class UserRepository(Repository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    def insert(self, object: UserScheme):
        # user = 
        pass
    
from abc import abstractmethod, ABC
from pydantic import BaseModel as BaseScheme

from database_configurator.models import BaseModel

#TODO между нотификатором и конфигуратором + топик кафки
class Repository(ABC):
    @abstractmethod
    def insert(self, object) -> BaseModel:
        pass
    
    @abstractmethod
    def update(self, id: int, object: BaseScheme) -> BaseModel:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

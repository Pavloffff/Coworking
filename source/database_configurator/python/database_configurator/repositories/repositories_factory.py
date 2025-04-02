from typing import Type, Dict

from database_configurator.repositories.base import BaseRepository


class RepositoriesFactory:
    _repositories: Dict[str, Type[BaseRepository]] = {}
    
    @classmethod
    def register(cls, model_name: str, repository: Type[BaseRepository]):
        cls._repositories[model_name] = repository
    
    @classmethod
    def get_repository(cls, model_name: str) -> Type[BaseRepository]:
        if model_name not in cls._repositories:
            raise ValueError(f"No repository registered for model: {model_name}")
        return cls._repositories[model_name]

from .user import UserRepository
from .repositories_factory import RepositoriesFactory

RepositoriesFactory.register("user", UserRepository)

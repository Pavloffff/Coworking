from pydantic import BaseModel

from servers_configurator.schemas.user import User


class Server(BaseModel):
    server_id: int
    name: str
    owner: User

from pydantic import BaseModel

from servers_configurator.schemas.server import Server


class Role(BaseModel):
    role_id: int
    name: str
    server_id: int
    rights: list[str]

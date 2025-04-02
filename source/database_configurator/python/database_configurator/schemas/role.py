from pydantic import BaseModel

from database_configurator.schemas.server import Server


class Role(BaseModel):
    role_id: int
    name: str
    server: Server

from pydantic import BaseModel

from notifications_pusher.schemas.server import Server


class Role(BaseModel):
    role_id: int
    name: str
    server_id: int
    rights: list[str]

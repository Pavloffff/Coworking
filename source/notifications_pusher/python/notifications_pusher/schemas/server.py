from pydantic import BaseModel

from notifications_pusher.schemas.user import User


class Server(BaseModel):
    server_id: int
    name: str
    owner: User

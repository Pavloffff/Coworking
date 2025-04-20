from pydantic import BaseModel


class UserServer(BaseModel):
    user_data: str
    server_id: str

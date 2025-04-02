from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    tag: int
    password_hash: str
    avatar_url: str

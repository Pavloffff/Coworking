from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    password_hash: str
    tag: int
    avatar_url: str
        
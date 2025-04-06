from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    email: str
    tag: int
    password_hash: str
    password_salt: str
    avatar_url: str

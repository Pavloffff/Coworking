from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    email: str
    password_hash: str
    password_salt: str
    tag: int
    avatar_url: str
        
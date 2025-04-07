from pydantic import BaseModel


class AuthResponse(BaseModel):
    email: str
    auth: bool
    access_token: str
    refresh_token: str

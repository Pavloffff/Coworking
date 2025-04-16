from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str

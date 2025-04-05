from pydantic import BaseModel


class UserRole(BaseModel):
    user_role_id: int
    user_id: int
    role_id: int

from pydantic import BaseModel


class UserResponse(BaseModel):
    sub: str
    email: str
    name: str
    is_admin: bool

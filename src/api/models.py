from pydantic import BaseModel


class UserResponse(BaseModel):
    sub: str
    email: str
    name: str


class CourseCreateRequest(BaseModel):
    code: str
    title: str
    description: str
    max_seats: int

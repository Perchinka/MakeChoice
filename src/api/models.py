from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel


class UserResponse(BaseModel):
    sub: str
    email: str
    name: str
    role: str


class CourseCreateRequest(BaseModel):
    code: str
    title: str
    description: str
    max_seats: int


class CourseResponse(BaseModel):
    id: UUID
    code: str
    title: str
    description: Optional[str]
    max_seats: int
    created_at: datetime
    updated_at: datetime


class SkippedCourse(BaseModel):
    input: CourseCreateRequest
    existing: CourseResponse


class ImportCoursesReport(BaseModel):
    imported: List[CourseResponse]
    skipped: List[SkippedCourse]


class ChoiceItem(BaseModel):
    priority: int = Field(..., description="Priority of the choice")
    course_id: UUID = Field(..., description="UUID of the selected course")

    class Config:
        schema_extra = {
            "example": {
                "priority": 1,
                "course_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }

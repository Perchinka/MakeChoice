from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, List
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

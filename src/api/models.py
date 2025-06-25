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


class ElectiveCreateRequest(BaseModel):
    code: str
    title: str
    description: str
    max_seats: int


class ElectiveResponse(BaseModel):
    id: UUID
    code: str
    title: str
    description: Optional[str]
    max_seats: int
    created_at: datetime
    updated_at: datetime


class SkippedElective(BaseModel):
    input: ElectiveCreateRequest
    existing: ElectiveResponse


class ImportElectiveReport(BaseModel):
    imported: List[ElectiveResponse]
    skipped: List[SkippedElective]


class ChoiceItem(BaseModel):
    priority: int = Field(..., description="Priority of the choice")
    elective_id: UUID = Field(..., description="UUID of the selected elective")

    class Config:
        schema_extra = {
            "example": {
                "priority": 1,
                "elective_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }

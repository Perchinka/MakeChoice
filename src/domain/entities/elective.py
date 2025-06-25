from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Field


class Elective(BaseModel):
    """
    An elective elective in the catalog.
    """

    id: UUID
    code: str
    title: str
    description: Optional[str]
    instructor: str
    category: str = Field(..., pattern="^(Tech|Hum)$")
    course_ids: List[UUID] = []
    created_at: datetime
    updated_at: datetime

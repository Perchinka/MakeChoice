from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class Course(BaseModel):
    """
    An elective course in the catalog.
    """

    id: UUID
    code: str
    title: str
    description: Optional[str]
    max_seats: int
    created_at: datetime
    updated_at: datetime

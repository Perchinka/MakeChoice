from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class Elective(BaseModel):
    """
    An elective elective in the catalog.
    """

    id: UUID
    code: str
    title: str
    description: Optional[str]
    max_seats: int
    created_at: datetime
    updated_at: datetime

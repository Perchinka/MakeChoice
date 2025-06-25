from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Choice(BaseModel):
    """
    A student's prioritized selection of a elective.
    """

    id: UUID
    user_id: UUID
    elective_id: UUID
    priority: int
    created_at: datetime
    updated_at: datetime

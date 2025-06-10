from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Choice(BaseModel):
    """
    A student's prioritized selection of a course.
    """

    id: UUID
    user_id: UUID
    course_id: UUID
    priority: int
    created_at: datetime
    updated_at: datetime

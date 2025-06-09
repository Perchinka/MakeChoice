from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Choice:
    """
    A student's prioritized selection of a course.
    """

    id: UUID
    user_id: UUID
    course_id: UUID
    priority: int
    created_at: datetime
    updated_at: datetime

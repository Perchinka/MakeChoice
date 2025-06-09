from pydantic import BaseModel
from uuid import UUID


class SelectionItem(BaseModel):
    priority: int
    course_id: UUID

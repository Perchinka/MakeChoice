from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Course(BaseModel):
    id: UUID
    name: str
    tech_quota: int
    hum_quota: int
    created_at: datetime
    updated_at: datetime

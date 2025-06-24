from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    sso_id: str
    name: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime

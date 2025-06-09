from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    sso_id: str
    name: str
    email: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

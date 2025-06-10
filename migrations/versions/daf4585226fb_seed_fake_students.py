"""seed fake students

Revision ID: daf4585226fb
Revises: 5d90ac5b7342
Create Date: 2025-06-10 01:26:43.891252

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime, timezone
import uuid


# revision identifiers, used by Alembic.
revision: str = "daf4585226fb"
down_revision: Union[str, None] = "5d90ac5b7342"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    now = datetime.now(timezone.utc)

    user_table = table(
        "users",
        column("id"),
        column("sso_id"),
        column("name"),
        column("email"),
        column("is_admin"),
        column("created_at"),
        column("updated_at"),
    )

    op.bulk_insert(
        user_table,
        [
            {
                "id": uuid.uuid4(),
                "sso_id": "student-001",
                "name": "Alice Example",
                "email": "alice@example.com",
                "is_admin": False,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": uuid.uuid4(),
                "sso_id": "student-002",
                "name": "Bob Example",
                "email": "bob@example.com",
                "is_admin": False,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": uuid.uuid4(),
                "sso_id": "student-003",
                "name": "Carol Example",
                "email": "carol@example.com",
                "is_admin": False,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM users WHERE sso_id IN (:s1, :s2, :s3)"),
        {"s1": "student-001", "s2": "student-002", "s3": "student-003"},
    )

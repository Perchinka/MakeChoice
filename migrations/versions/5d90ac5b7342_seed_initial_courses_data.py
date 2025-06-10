"""seed initial courses data

Revision ID: 5d90ac5b7342
Revises: 2475dc0cabff
Create Date: 2025-06-10 01:20:20.002066

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime, timezone
import uuid


# revision identifiers, used by Alembic.
revision: str = "5d90ac5b7342"
down_revision: Union[str, None] = "2475dc0cabff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    now = datetime.now(timezone.utc)

    course_table = table(
        "courses",
        column("id"),
        column("code"),
        column("title"),
        column("description"),
        column("max_seats"),
        column("created_at"),
        column("updated_at"),
    )

    op.bulk_insert(
        course_table,
        [
            {
                "id": uuid.uuid4(),
                "code": "CS101",
                "title": "Introduction to Programming",
                "description": "Fundamentals of programming using Python.",
                "max_seats": 30,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": uuid.uuid4(),
                "code": "MATH201",
                "title": "Linear Algebra",
                "description": "Vector spaces, matrices, and linear transformations.",
                "max_seats": 25,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": uuid.uuid4(),
                "code": "STAT202",
                "title": "Probability and Statistics",
                "description": "Basic probability theory and statistical inference.",
                "max_seats": 40,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": uuid.uuid4(),
                "code": "CS303",
                "title": "Algorithms",
                "description": "Design and analysis of algorithms.",
                "max_seats": 20,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text("DELETE FROM courses WHERE code IN (:c1, :c2, :c3, :c4)"),
        {"c1": "CS101", "c2": "MATH201", "c3": "STAT202", "c4": "CS303"},
    )

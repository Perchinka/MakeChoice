"""seed fake choices

Revision ID: bcacd8abee0d
Revises: daf4585226fb
Create Date: 2025-06-10 01:28:48.335321

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime, timezone
import uuid


# revision identifiers, used by Alembic.
revision: str = "bcacd8abee0d"
down_revision: Union[str, None] = "daf4585226fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = ["5d90ac5b7342", "daf4585226fb"]


def upgrade() -> None:
    conn = op.get_bind()
    now = datetime.now(timezone.utc)

    user_ids = {
        sso: conn.execute(
            sa.text("SELECT id FROM users WHERE sso_id = :sso"),
            {"sso": sso},
        ).scalar_one()
        for sso in ("student-001", "student-002", "student-003")
    }

    course_ids = {
        code: conn.execute(
            sa.text("SELECT id FROM courses WHERE code = :code"),
            {"code": code},
        ).scalar_one()
        for code in ("CS101", "MATH201", "STAT202", "CS303")
    }

    choice_table = table(
        "choices",
        column("id"),
        column("user_id"),
        column("course_id"),
        column("priority"),
        column("created_at"),
        column("updated_at"),
    )

    choices = [
        {
            "id": uuid.uuid4(),
            "user_id": user_ids["student-001"],
            "course_id": course_ids["CS101"],
            "priority": 1,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": uuid.uuid4(),
            "user_id": user_ids["student-001"],
            "course_id": course_ids["MATH201"],
            "priority": 2,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": uuid.uuid4(),
            "user_id": user_ids["student-002"],
            "course_id": course_ids["CS101"],
            "priority": 1,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": uuid.uuid4(),
            "user_id": user_ids["student-002"],
            "course_id": course_ids["STAT202"],
            "priority": 2,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": uuid.uuid4(),
            "user_id": user_ids["student-003"],
            "course_id": course_ids["CS303"],
            "priority": 1,
            "created_at": now,
            "updated_at": now,
        },
    ]

    op.bulk_insert(choice_table, choices)


def downgrade() -> None:
    op.execute(
        sa.text(
            "DELETE FROM choices WHERE user_id IN ("
            " SELECT id FROM users WHERE sso_id IN (:s1, :s2, :s3)"
            ")"
        ),
        {"s1": "student-001", "s2": "student-002", "s3": "student-003"},
    )

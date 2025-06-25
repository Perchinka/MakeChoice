"""extend electives

Revision ID: 2b6c7d9cfbba
Revises: d8497dd06814
Create Date: 2025-06-25 09:43:00.506873

"""

from datetime import datetime, timezone
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b6c7d9cfbba"
down_revision: Union[str, None] = "d8497dd06814"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "electives",
        sa.Column("instructor", sa.Text(), nullable=False, server_default="TBD"),
    )
    op.add_column(
        "electives",
        sa.Column(
            "category",
            sa.Text(),
            nullable=False,
            server_default="Tech",
        ),
    )
    op.create_check_constraint(
        "chk_electives_category",
        "electives",
        "category IN ('Tech','Hum')",
    )
    op.drop_column("electives", "max_seats")

    # New table: courses
    op.create_table(
        "courses",
        sa.Column("id", sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.Text(), nullable=False, unique=True),
        sa.Column("tech_quota", sa.SmallInteger(), nullable=False),
        sa.Column("hum_quota", sa.SmallInteger(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc),
        ),
    )

    # Association electives <-> courses (many-to-many)
    op.create_table(
        "elective_courses",
        sa.Column(
            "elective_id",
            sa.UUID(),
            sa.ForeignKey("electives.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "course_id",
            sa.UUID(),
            sa.ForeignKey("courses.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("elective_courses")
    op.drop_table("courses")
    op.drop_constraint("chk_electives_category", "electives", type_="check")
    op.drop_column("electives", "category")
    op.drop_column("electives", "instructor")

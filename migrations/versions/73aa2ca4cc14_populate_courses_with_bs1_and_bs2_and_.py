"""populate courses with bs1 and bs2 and map on electives

Revision ID: 73aa2ca4cc14
Revises: 2b6c7d9cfbba
Create Date: 2025-06-25 11:55:09.207067

"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = "73aa2ca4cc14"
down_revision: Union[str, None] = "2b6c7d9cfbba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    now = datetime.now(timezone.utc)

    # ─── insert Bs1 & Bs2 ─────────────────────────────────────
    course_tbl = table(
        "courses",
        column("id"),
        column("name"),
        column("tech_quota"),
        column("hum_quota"),
        column("created_at"),
        column("updated_at"),
    )

    bs1_id = uuid.uuid4()
    bs2_id = uuid.uuid4()

    op.bulk_insert(
        course_tbl,
        [
            {
                "id": bs1_id,
                "name": "Bs1",
                "tech_quota": 2,
                "hum_quota": 1,
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": bs2_id,
                "name": "Bs2",
                "tech_quota": 1,
                "hum_quota": 0,
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    # ─── fetch existing elective IDs ──────────────────────────
    codes = ("CS101", "MATH201", "STAT202", "CS303")
    rows = conn.execute(
        sa.text("SELECT id, code FROM electives WHERE code IN :codes"),
        {"codes": tuple(codes)},
    ).all()
    code_to_id = {row.code: row.id for row in rows}  # type: ignore[attr-defined]

    # ─── elective → course mapping (1–2 courses each) ─────────
    mappings: list[tuple[uuid.UUID, uuid.UUID]] = [
        (code_to_id["CS101"], bs1_id),
        (code_to_id["MATH201"], bs1_id),
        (code_to_id["STAT202"], bs2_id),
        (code_to_id["CS303"], bs1_id),
        (code_to_id["CS303"], bs2_id),
    ]

    ec_tbl = table("elective_courses", column("elective_id"), column("course_id"))
    op.bulk_insert(
        ec_tbl,
        [{"elective_id": e, "course_id": c} for e, c in mappings],
    )

    # ─── set instructor names ─────────────────────────────────
    instructor_map = {
        "CS101": "Dr. Ada Smith",
        "MATH201": "Prof. Alan Johnson",
        "STAT202": "Dr. Grace Lee",
        "CS303": "Prof. Donald Brown",
    }
    for code, inst in instructor_map.items():
        conn.execute(
            sa.text(
                "UPDATE electives "
                "SET instructor = :inst, updated_at = :ts "
                "WHERE code = :code"
            ),
            {"inst": inst, "ts": now, "code": code},
        )


def downgrade() -> None:
    conn = op.get_bind()

    # delete course mappings first
    conn.execute(
        sa.text(
            """
            DELETE FROM elective_courses
            WHERE course_id IN (
                SELECT id FROM courses WHERE name IN ('Bs1', 'Bs2')
            )
            """
        )
    )

    # delete Bs1 & Bs2
    conn.execute(sa.text("DELETE FROM courses WHERE name IN ('Bs1','Bs2')"))

    # reset instructors to 'TBD'
    conn.execute(
        sa.text(
            """
            UPDATE electives
            SET instructor = 'TBD'
            WHERE instructor IN (
                'Dr. Ada Smith',
                'Prof. Alan Johnson',
                'Dr. Grace Lee',
                'Prof. Donald Brown'
            )
            """
        )
    )

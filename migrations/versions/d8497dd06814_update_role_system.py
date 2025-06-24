"""update role-system

Revision ID: d8497dd06814
Revises: bcacd8abee0d
Create Date: 2025-06-24 22:43:34.166201

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d8497dd06814"
down_revision: Union[str, None] = "bcacd8abee0d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # drop old boolean flag
    op.drop_column("users", "is_admin")

    # add role column with default 'Student'
    op.add_column(
        "users",
        sa.Column("role", sa.Text(), nullable=False, server_default="Student"),
    )
    # enforce only valid values
    op.create_check_constraint(
        "chk_users_role",
        "users",
        "role IN ('Admin', 'Student', 'Instructor')",
    )


def downgrade():
    # remove role & re-add is_admin
    op.drop_constraint("chk_users_role", "users", type_="check")
    op.drop_column("users", "role")
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="false"),
    )

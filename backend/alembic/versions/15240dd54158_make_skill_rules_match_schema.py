"""make skill rules match schema

Revision ID: 15240dd54158
Revises: 5665d3759eee
Create Date: 2026-11-16 14:12:17.219976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15240dd54158'
down_revision: Union[str, Sequence[str], None] = '5665d3759eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "skillitem",
        "proficiency",
        existing_type=sa.VARCHAR(),
        nullable=False
    )
    op.alter_column(
        "skillitem",
        "description",
        existing_type=sa.VARCHAR(),
        type_=sa.String(length=300),
        existing_nullable=True
    )
    op.create_check_constraint(
        "ck_skillitem_years_experience_non_negative",
        "skillitem",
        "years_experience >= 0"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "ck_skillitem_years_experience_non_negative",
        "skillitem",
        type_="check"
    )
    op.alter_column(
        "skillitem",
        "description",
        existing_type=sa.String(length=300),
        type_=sa.VARCHAR(),
        existing_nullable=True
    )
    op.alter_column(
        "skillitem",
        "proficiency",
        existing_type=sa.VARCHAR(),
        nullable=True
    )

"""add universal_id to articles

Revision ID: 1b5b6c738ae4
Revises: 856a722a63a5
Create Date: 2025-12-31 10:11:00.046287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1b5b6c738ae4'
down_revision: Union[str, Sequence[str], None] = '856a722a63a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    tables = [
        "articles",
        "budgets_union",
        "ce",
        "cgst",
        "cu",
        "dgft",
        "features",
        "sgst",
        "st",
        "vat",
    ]

    for table in tables:
        # 1. Add column as nullable
        op.add_column(
            table,
            sa.Column("universal_id", postgresql.UUID(as_uuid=True), nullable=True))

        # 2. Backfill existing rows
        op.execute(
            f"UPDATE {table} SET universal_id = gen_random_uuid() WHERE universal_id IS NULL")

        # 3. Enforce NOT NULL
        op.alter_column(table, "universal_id", nullable=False)

        # 4. Create UNIQUE index
        op.create_index(
            op.f(f"ix_{table}_universal_id"),
            table,
            ["universal_id"],
            unique=True)


def downgrade() -> None:
    """Downgrade schema."""

    tables = [
        "articles",
        "budgets_union",
        "ce",
        "cgst",
        "cu",
        "dgft",
        "features",
        "sgst",
        "st",
        "vat",
    ]

    for table in tables:
        # Drop index first
        op.drop_index(
            op.f(f"ix_{table}_universal_id"),
            table_name=table)

        # Drop column
        op.drop_column(table, "universal_id")

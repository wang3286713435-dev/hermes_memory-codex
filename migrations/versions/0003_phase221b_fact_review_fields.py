"""phase221b fact review fields

Revision ID: 0003_phase221b_review
Revises: 0002_phase221_facts_schema
Create Date: 2026-04-26
"""

import sqlalchemy as sa
from alembic import op


revision = "0003_phase221b_review"
down_revision = "0002_phase221_facts_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    columns = {column["name"] for column in inspector.get_columns("facts")}
    _add_column_if_missing(columns, "confirmed_at", sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True))
    _add_column_if_missing(columns, "rejected_by", sa.Column("rejected_by", sa.String(length=128), nullable=True))
    _add_column_if_missing(columns, "rejected_at", sa.Column("rejected_at", sa.DateTime(timezone=True), nullable=True))
    _add_column_if_missing(columns, "rejection_reason", sa.Column("rejection_reason", sa.Text(), nullable=True))
    _create_index_if_missing("ix_facts_rejected_by", ["rejected_by"])


def downgrade() -> None:
    _drop_index_if_exists("ix_facts_rejected_by")
    for column in ("rejection_reason", "rejected_at", "rejected_by", "confirmed_at"):
        if column in {item["name"] for item in sa.inspect(op.get_bind()).get_columns("facts")}:
            op.drop_column("facts", column)


def _add_column_if_missing(columns: set[str], name: str, column: sa.Column) -> None:
    if name not in columns:
        op.add_column("facts", column)


def _create_index_if_missing(name: str, columns: list[str]) -> None:
    existing = {index["name"] for index in sa.inspect(op.get_bind()).get_indexes("facts")}
    if name not in existing:
        op.create_index(name, "facts", columns)


def _drop_index_if_exists(name: str) -> None:
    existing = {index["name"] for index in sa.inspect(op.get_bind()).get_indexes("facts")}
    if name in existing:
        op.drop_index(name, table_name="facts")

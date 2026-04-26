"""phase221 facts schema

Revision ID: 0002_phase221_facts_schema
Revises: 0001_phase1_core_schema
Create Date: 2026-04-26
"""

import sqlalchemy as sa
from alembic import op


revision = "0002_phase221_facts_schema"
down_revision = "0001_phase1_core_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("facts"):
        columns = {column["name"] for column in inspector.get_columns("facts")}
        _add_column_if_missing(columns, "fact_type", sa.Column("fact_type", sa.String(length=64), nullable=True))
        _add_column_if_missing(columns, "subject", sa.Column("subject", sa.String(length=256), nullable=True))
        _add_column_if_missing(columns, "source_version_id", sa.Column("source_version_id", sa.String(), nullable=True))
        _add_column_if_missing(columns, "verification_status", sa.Column("verification_status", sa.String(length=32), nullable=True))
        _add_column_if_missing(columns, "created_by", sa.Column("created_by", sa.String(length=128), nullable=True))
        _add_column_if_missing(columns, "confirmed_by", sa.Column("confirmed_by", sa.String(length=128), nullable=True))
        _add_column_if_missing(columns, "audit_event_id", sa.Column("audit_event_id", sa.String(), nullable=True))
        for legacy_column in ("entity_type", "entity_id", "value_type", "verified_status"):
            if legacy_column in columns:
                op.alter_column("facts", legacy_column, nullable=True, existing_type=sa.String())
        _create_missing_indexes()
        return

    op.create_table(
        "facts",
        sa.Column("fact_type", sa.String(length=64), nullable=False),
        sa.Column("subject", sa.String(length=256), nullable=False),
        sa.Column("predicate", sa.String(length=128), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("source_document_id", sa.String(), nullable=False),
        sa.Column("source_version_id", sa.String(), nullable=False),
        sa.Column("source_chunk_id", sa.String(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("verification_status", sa.String(length=32), nullable=False),
        sa.Column("created_by", sa.String(length=128), nullable=True),
        sa.Column("confirmed_by", sa.String(length=128), nullable=True),
        sa.Column("audit_event_id", sa.String(), nullable=True),
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["audit_event_id"], ["audit_logs.id"]),
        sa.ForeignKeyConstraint(["source_chunk_id"], ["chunks.id"]),
        sa.ForeignKeyConstraint(["source_document_id"], ["documents.id"]),
        sa.ForeignKeyConstraint(["source_version_id"], ["document_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_facts_fact_type", "facts", ["fact_type"])
    op.create_index("ix_facts_subject", "facts", ["subject"])
    op.create_index("ix_facts_predicate", "facts", ["predicate"])
    op.create_index("ix_facts_source_document_id", "facts", ["source_document_id"])
    op.create_index("ix_facts_source_version_id", "facts", ["source_version_id"])
    op.create_index("ix_facts_source_chunk_id", "facts", ["source_chunk_id"])
    op.create_index("ix_facts_verification_status", "facts", ["verification_status"])
    op.create_index("ix_facts_created_by", "facts", ["created_by"])
    op.create_index("ix_facts_confirmed_by", "facts", ["confirmed_by"])
    op.create_index("ix_facts_audit_event_id", "facts", ["audit_event_id"])
    op.create_index("ix_facts_subject_predicate", "facts", ["subject", "predicate"])
    op.create_index("ix_facts_source_document_version", "facts", ["source_document_id", "source_version_id"])


def downgrade() -> None:
    op.drop_table("facts")


def _add_column_if_missing(columns: set[str], name: str, column: sa.Column) -> None:
    if name not in columns:
        op.add_column("facts", column)


def _create_missing_indexes() -> None:
    existing = {index["name"] for index in sa.inspect(op.get_bind()).get_indexes("facts")}
    index_specs = {
        "ix_facts_fact_type": ["fact_type"],
        "ix_facts_subject": ["subject"],
        "ix_facts_predicate": ["predicate"],
        "ix_facts_source_document_id": ["source_document_id"],
        "ix_facts_source_version_id": ["source_version_id"],
        "ix_facts_source_chunk_id": ["source_chunk_id"],
        "ix_facts_verification_status": ["verification_status"],
        "ix_facts_created_by": ["created_by"],
        "ix_facts_confirmed_by": ["confirmed_by"],
        "ix_facts_audit_event_id": ["audit_event_id"],
        "ix_facts_subject_predicate": ["subject", "predicate"],
        "ix_facts_source_document_version": ["source_document_id", "source_version_id"],
    }
    for name, columns in index_specs.items():
        if name not in existing:
            op.create_index(name, "facts", columns)

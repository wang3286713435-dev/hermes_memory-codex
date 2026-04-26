from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TimestampMixin


class Fact(IdMixin, TimestampMixin, Base):
    __tablename__ = "facts"
    __table_args__ = (
        Index("ix_facts_subject_predicate", "subject", "predicate"),
        Index("ix_facts_source_document_version", "source_document_id", "source_version_id"),
    )

    fact_type: Mapped[str] = mapped_column(String(64), index=True)
    subject: Mapped[str] = mapped_column(String(256), index=True)
    predicate: Mapped[str] = mapped_column(String(128), index=True)
    value: Mapped[str] = mapped_column(Text)
    source_document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    source_version_id: Mapped[str] = mapped_column(ForeignKey("document_versions.id"), index=True)
    source_chunk_id: Mapped[str] = mapped_column(ForeignKey("chunks.id"), index=True)
    confidence: Mapped[float | None] = mapped_column(Float)
    verification_status: Mapped[str] = mapped_column(String(32), default="unverified", index=True)
    created_by: Mapped[str | None] = mapped_column(String(128), index=True)
    confirmed_by: Mapped[str | None] = mapped_column(String(128), index=True)
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejected_by: Mapped[str | None] = mapped_column(String(128), index=True)
    rejected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(Text)
    audit_event_id: Mapped[str | None] = mapped_column(ForeignKey("audit_logs.id"), index=True)

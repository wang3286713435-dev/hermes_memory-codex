from sqlalchemy import ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TimestampMixin


class CitationRecord(IdMixin, TimestampMixin, Base):
    __tablename__ = "citations"
    __table_args__ = (
        Index("ix_citations_chunk", "chunk_id"),
        Index("ix_citations_document_version", "document_id", "version_id"),
    )

    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    version_id: Mapped[str] = mapped_column(ForeignKey("document_versions.id"), index=True)
    chunk_id: Mapped[str] = mapped_column(ForeignKey("chunks.id"), index=True)
    source_name: Mapped[str] = mapped_column(String(512))
    source_uri: Mapped[str | None] = mapped_column(Text)
    page_start: Mapped[int | None] = mapped_column(Integer)
    page_end: Mapped[int | None] = mapped_column(Integer)
    heading_path: Mapped[list[str] | None] = mapped_column(JSON)
    quote_text: Mapped[str] = mapped_column(Text)


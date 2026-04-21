from sqlalchemy import ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin
from app.models.document import DocumentVersion


class Chunk(IdMixin, TimestampMixin, Base):
    __tablename__ = "chunks"
    __table_args__ = (
        Index("ix_chunks_document_version", "document_id", "version_id"),
        Index("ix_chunks_version_index", "version_id", "chunk_index"),
    )

    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    version_id: Mapped[str] = mapped_column(ForeignKey("document_versions.id"), index=True)
    chunk_index: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(Text)
    heading_path: Mapped[list[str] | None] = mapped_column(JSON)
    title_path: Mapped[list[str] | None] = mapped_column(JSON)
    section_path: Mapped[list[str] | None] = mapped_column(JSON)
    page_start: Mapped[int | None] = mapped_column(Integer)
    page_end: Mapped[int | None] = mapped_column(Integer)
    char_count: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String(128), index=True)
    token_count: Mapped[int | None] = mapped_column(Integer)
    source_type: Mapped[str] = mapped_column(String(64), index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON)
    embedding_id: Mapped[str | None] = mapped_column(String(128), index=True)
    sparse_id: Mapped[str | None] = mapped_column(String(128), index=True)
    permission_tags: Mapped[list[str] | None] = mapped_column(JSON)

    version: Mapped[DocumentVersion] = relationship(back_populates="chunks")

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdMixin, TimestampMixin


class Document(IdMixin, TimestampMixin, Base):
    __tablename__ = "documents"
    __table_args__ = (
        Index("ix_documents_source_type_status", "source_type", "status"),
        Index("ix_documents_project_status", "project_id", "status"),
    )

    title: Mapped[str] = mapped_column(String(512), index=True)
    source_type: Mapped[str] = mapped_column(String(64), index=True)
    source_uri: Mapped[str] = mapped_column(Text)
    storage_uri: Mapped[str | None] = mapped_column(Text)
    document_type: Mapped[str | None] = mapped_column(String(64), index=True)
    owner_id: Mapped[str | None] = mapped_column(String(128), index=True)
    department_id: Mapped[str | None] = mapped_column(String(128), index=True)
    project_id: Mapped[str | None] = mapped_column(String(128), index=True)
    confidentiality_level: Mapped[str] = mapped_column(String(32), default="internal", index=True)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON)

    versions: Mapped[list["DocumentVersion"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentVersion(IdMixin, TimestampMixin, Base):
    __tablename__ = "document_versions"
    __table_args__ = (
        Index("ix_document_versions_document_latest", "document_id", "is_latest"),
    )

    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"), index=True)
    version_name: Mapped[str | None] = mapped_column(String(128))
    version_number: Mapped[str | None] = mapped_column(String(64))
    file_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    content_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    is_latest: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    effective_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expired_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    parse_status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict | None] = mapped_column(JSON)

    document: Mapped[Document] = relationship(back_populates="versions")
    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="version",
        cascade="all, delete-orphan",
    )

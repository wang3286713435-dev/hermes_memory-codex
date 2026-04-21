from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TimestampMixin


class Fact(IdMixin, TimestampMixin, Base):
    __tablename__ = "facts"

    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_id: Mapped[str] = mapped_column(String(128), index=True)
    predicate: Mapped[str] = mapped_column(String(128), index=True)
    value: Mapped[str] = mapped_column(Text)
    value_type: Mapped[str] = mapped_column(String(64), default="string")
    source_document_id: Mapped[str | None] = mapped_column(String(128), index=True)
    source_chunk_id: Mapped[str | None] = mapped_column(String(128), index=True)
    confidence: Mapped[float | None] = mapped_column(Float)
    verified_status: Mapped[str] = mapped_column(String(32), default="unverified", index=True)


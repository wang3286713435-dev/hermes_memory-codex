from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TimestampMixin


class RetrievalLog(IdMixin, TimestampMixin, Base):
    __tablename__ = "retrieval_logs"

    trace_id: Mapped[str] = mapped_column(String(128), index=True)
    user_id: Mapped[str | None] = mapped_column(String(128), index=True)
    query: Mapped[str] = mapped_column(Text)
    top_k: Mapped[int] = mapped_column(Integer)
    filters_json: Mapped[dict | None] = mapped_column(JSON)
    result_count: Mapped[int] = mapped_column(Integer, default=0)
    backend: Mapped[str] = mapped_column(String(64), default="opensearch")
    status: Mapped[str] = mapped_column(String(32), default="success", index=True)


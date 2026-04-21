from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdMixin, TimestampMixin


class Permission(IdMixin, TimestampMixin, Base):
    __tablename__ = "permissions"

    resource_type: Mapped[str] = mapped_column(String(64), index=True)
    resource_id: Mapped[str] = mapped_column(String(128), index=True)
    subject_type: Mapped[str] = mapped_column(String(64), index=True)
    subject_id: Mapped[str] = mapped_column(String(128), index=True)
    action: Mapped[str] = mapped_column(String(64), index=True)
    effect: Mapped[str] = mapped_column(String(16), default="allow", index=True)
    condition_json: Mapped[dict | None] = mapped_column(JSON)


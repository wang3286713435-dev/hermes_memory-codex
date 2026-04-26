from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.chunk import Chunk
from app.models.document import DocumentVersion
from app.models.fact import Fact


class FactValidationError(ValueError):
    pass


@dataclass(frozen=True)
class FactView:
    fact: Fact
    source_version_is_latest: bool

    @property
    def stale_source_version(self) -> bool:
        return not self.source_version_is_latest


class FactService:
    """Minimal evidence-backed facts service.

    Facts are structured records linked to retrieval evidence. They do not
    participate in retrieval or answer generation in Phase 2.21a.
    """

    VALID_STATUSES = {"unverified", "confirmed", "rejected"}

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_fact_from_evidence(
        self,
        *,
        fact_type: str,
        subject: str,
        predicate: str,
        value: str,
        source_chunk_id: str,
        confidence: float | None = None,
        created_by: str | None = None,
        audit_event_id: str | None = None,
        verification_status: str = "unverified",
    ) -> Fact:
        if not source_chunk_id:
            raise FactValidationError("source_chunk_id_required")
        if verification_status != "unverified":
            raise FactValidationError("new_fact_must_start_unverified")
        chunk = self.db.get(Chunk, source_chunk_id)
        if chunk is None:
            raise FactValidationError("source_chunk_not_found")
        version = self.db.get(DocumentVersion, chunk.version_id)
        if version is None:
            raise FactValidationError("source_version_not_found")
        if audit_event_id and self.db.get(AuditLog, audit_event_id) is None:
            raise FactValidationError("audit_event_not_found")

        fact = Fact(
            fact_type=fact_type,
            subject=subject,
            predicate=predicate,
            value=value,
            source_document_id=chunk.document_id,
            source_version_id=chunk.version_id,
            source_chunk_id=chunk.id,
            confidence=confidence,
            verification_status="unverified",
            created_by=created_by,
            confirmed_by=None,
            audit_event_id=audit_event_id,
        )
        self.db.add(fact)
        self.db.flush()
        self._add_audit_event(
            action="fact.create",
            fact=fact,
            actor_id=created_by,
            status="unverified",
        )
        self.db.commit()
        self.db.refresh(fact)
        return fact

    def list_facts_by_document(self, document_id: str) -> list[FactView]:
        rows = (
            self.db.query(Fact, DocumentVersion)
            .join(DocumentVersion, Fact.source_version_id == DocumentVersion.id)
            .filter(Fact.source_document_id == document_id)
            .order_by(Fact.created_at.desc())
            .all()
        )
        return [FactView(fact=fact, source_version_is_latest=version.is_latest) for fact, version in rows]

    def list_facts_by_subject(self, subject: str) -> list[FactView]:
        rows = (
            self.db.query(Fact, DocumentVersion)
            .join(DocumentVersion, Fact.source_version_id == DocumentVersion.id)
            .filter(Fact.subject == subject)
            .order_by(Fact.created_at.desc())
            .all()
        )
        return [FactView(fact=fact, source_version_is_latest=version.is_latest) for fact, version in rows]

    def confirm_fact(self, fact_id: str, *, actor_id: str | None = None) -> Fact:
        return self._set_status(fact_id, "confirmed", actor_id=actor_id)

    def mark_fact_rejected(self, fact_id: str, *, actor_id: str | None = None) -> Fact:
        return self._set_status(fact_id, "rejected", actor_id=actor_id)

    def _set_status(self, fact_id: str, status: str, *, actor_id: str | None = None) -> Fact:
        if status not in self.VALID_STATUSES:
            raise FactValidationError("invalid_verification_status")
        fact = self.db.get(Fact, fact_id)
        if fact is None:
            raise FactValidationError("fact_not_found")
        fact.verification_status = status
        fact.confirmed_by = actor_id if status == "confirmed" else None
        self._add_audit_event(
            action=f"fact.{status}",
            fact=fact,
            actor_id=actor_id,
            status=status,
        )
        self.db.commit()
        self.db.refresh(fact)
        return fact

    def _add_audit_event(self, *, action: str, fact: Fact, actor_id: str | None, status: str) -> None:
        self.db.add(
            AuditLog(
                trace_id=f"fact:{fact.id}",
                user_id=actor_id or "local_dev",
                action=action,
                resource_type="fact",
                resource_id=fact.id,
                request_json={
                    "source_document_id": fact.source_document_id,
                    "source_version_id": fact.source_version_id,
                    "source_chunk_id": fact.source_chunk_id,
                },
                result_json={
                    "fact_type": fact.fact_type,
                    "subject": fact.subject,
                    "predicate": fact.predicate,
                    "verification_status": status,
                    "audit_event_id": fact.audit_event_id,
                },
            )
        )

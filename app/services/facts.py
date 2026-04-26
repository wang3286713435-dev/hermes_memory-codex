from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.chunk import Chunk
from app.models.document import Document
from app.models.document import DocumentVersion
from app.models.fact import Fact

logger = logging.getLogger(__name__)


class FactValidationError(ValueError):
    pass


@dataclass(frozen=True)
class FactView:
    fact: Fact
    source_version_is_latest: bool

    @property
    def stale_source_version(self) -> bool:
        return not self.source_version_is_latest


@dataclass(frozen=True)
class FactQueryIdentity:
    requester_id: str = "local_dev"
    tenant_id: str = "local_dev"
    role: str = "local_dev"


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

    def list_facts_by_document(
        self,
        document_id: str,
        *,
        requester_id: str | None = None,
        tenant_id: str | None = None,
        role: str | None = None,
    ) -> list[FactView]:
        rows = (
            self.db.query(Fact, DocumentVersion)
            .join(DocumentVersion, Fact.source_version_id == DocumentVersion.id)
            .filter(Fact.source_document_id == document_id)
            .order_by(Fact.created_at.desc())
            .all()
        )
        return self._apply_query_policy_and_audit(
            rows,
            query_type="by_document",
            query_filter={"document_id": document_id},
            identity=self._identity(requester_id=requester_id, tenant_id=tenant_id, role=role),
        )

    def list_facts_by_subject(
        self,
        subject: str,
        *,
        requester_id: str | None = None,
        tenant_id: str | None = None,
        role: str | None = None,
    ) -> list[FactView]:
        rows = (
            self.db.query(Fact, DocumentVersion)
            .join(DocumentVersion, Fact.source_version_id == DocumentVersion.id)
            .filter(Fact.subject == subject)
            .order_by(Fact.created_at.desc())
            .all()
        )
        return self._apply_query_policy_and_audit(
            rows,
            query_type="by_subject",
            query_filter={"subject": subject},
            identity=self._identity(requester_id=requester_id, tenant_id=tenant_id, role=role),
        )

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

    def _apply_query_policy_and_audit(
        self,
        rows: list[tuple[Fact, DocumentVersion]],
        *,
        query_type: str,
        query_filter: dict[str, str],
        identity: FactQueryIdentity,
    ) -> list[FactView]:
        document_acl = self._load_document_acl([fact.source_document_id for fact, _ in rows])
        returned: list[FactView] = []
        denied_fact_ids: list[str] = []
        denied_document_ids: list[str] = []
        source_document_ids: list[str] = []
        document_decisions: dict[str, dict[str, Any]] = {}

        for fact, version in rows:
            if fact.source_document_id not in source_document_ids:
                source_document_ids.append(fact.source_document_id)
            decision = document_decisions.get(fact.source_document_id)
            if decision is None:
                decision = self._decide_document_access(document_acl.get(fact.source_document_id), identity)
                document_decisions[fact.source_document_id] = decision
            if decision["decision"] == "deny":
                denied_fact_ids.append(fact.id)
                if fact.source_document_id not in denied_document_ids:
                    denied_document_ids.append(fact.source_document_id)
                continue
            returned.append(FactView(fact=fact, source_version_is_latest=version.is_latest))

        policy_decision = self._aggregate_policy_decision(document_decisions, bool(rows))
        self._add_fact_query_audit(
            identity=identity,
            query_type=query_type,
            query_filter=query_filter,
            returned_fact_ids=[view.fact.id for view in returned],
            denied_fact_ids=denied_fact_ids,
            source_document_ids=source_document_ids,
            denied_document_ids=denied_document_ids,
            policy_decision=policy_decision,
            policy_reason=self._policy_reason(document_decisions, policy_decision),
        )
        return returned

    def _identity(self, *, requester_id: str | None, tenant_id: str | None, role: str | None) -> FactQueryIdentity:
        return FactQueryIdentity(
            requester_id=requester_id or "local_dev",
            tenant_id=tenant_id or "local_dev",
            role=role or "local_dev",
        )

    def _load_document_acl(self, document_ids: list[str]) -> dict[str, dict[str, Any] | None]:
        unique_ids = sorted({document_id for document_id in document_ids if document_id})
        if not unique_ids:
            return {}
        rows = self.db.query(Document).filter(Document.id.in_(unique_ids)).all()
        metadata_by_id = {document.id: document.metadata_json or {} for document in rows}
        return {document_id: metadata_by_id.get(document_id) for document_id in unique_ids}

    def _decide_document_access(
        self,
        metadata: dict[str, Any] | None,
        identity: FactQueryIdentity,
    ) -> dict[str, Any]:
        if metadata is None:
            return {"decision": "allow", "reason": "acl_metadata_missing", "policy_decision": "not_configured_allow"}

        allowed_requester_ids = self._as_list(metadata.get("allowed_requester_ids"))
        allowed_roles = self._as_list(metadata.get("allowed_roles"))
        tenant_id = metadata.get("tenant_id")
        acl_configured = bool(allowed_requester_ids or allowed_roles or tenant_id)

        if not acl_configured:
            return {"decision": "allow", "reason": "acl_not_configured", "policy_decision": "not_configured_allow"}
        if tenant_id and str(tenant_id) != identity.tenant_id:
            return {"decision": "deny", "reason": "tenant_mismatch", "policy_decision": "deny"}
        if allowed_requester_ids and identity.requester_id in allowed_requester_ids:
            return {"decision": "allow", "reason": "requester_id_allowed", "policy_decision": "allow"}
        if allowed_roles and identity.role in allowed_roles:
            return {"decision": "allow", "reason": "role_allowed", "policy_decision": "allow"}
        if allowed_requester_ids or allowed_roles:
            return {"decision": "deny", "reason": "acl_no_match", "policy_decision": "deny"}
        return {"decision": "allow", "reason": "tenant_match", "policy_decision": "allow"}

    def _aggregate_policy_decision(self, document_decisions: dict[str, dict[str, Any]], had_facts: bool) -> str:
        if not had_facts:
            return "not_configured_allow"
        if document_decisions and all(decision["decision"] == "deny" for decision in document_decisions.values()):
            return "deny"
        if any(decision.get("policy_decision") == "allow" for decision in document_decisions.values()):
            return "allow"
        return "not_configured_allow"

    def _policy_reason(self, document_decisions: dict[str, dict[str, Any]], policy_decision: str) -> str:
        reasons = sorted({decision.get("reason", "unknown") for decision in document_decisions.values()})
        if not reasons:
            return "no_facts"
        if policy_decision == "deny":
            return ",".join(reasons)
        if any(reason not in {"acl_not_configured", "acl_metadata_missing"} for reason in reasons):
            return ",".join(reasons)
        return "acl_not_configured"

    def _as_list(self, value: Any) -> list[str]:
        if value in (None, "", [], {}):
            return []
        if isinstance(value, list):
            return [str(item) for item in value if item not in (None, "")]
        if isinstance(value, (tuple, set)):
            return [str(item) for item in value if item not in (None, "")]
        return [str(value)]

    def _add_fact_query_audit(
        self,
        *,
        identity: FactQueryIdentity,
        query_type: str,
        query_filter: dict[str, str],
        returned_fact_ids: list[str],
        denied_fact_ids: list[str],
        source_document_ids: list[str],
        denied_document_ids: list[str],
        policy_decision: str,
        policy_reason: str,
    ) -> None:
        try:
            self.db.add(
                AuditLog(
                    trace_id=f"fact_query:{query_type}:{hash(str(query_filter))}",
                    user_id=identity.requester_id,
                    action="fact.query",
                    resource_type="fact",
                    resource_id=query_filter.get("document_id") or query_filter.get("subject"),
                    request_json={
                        "requester_id": identity.requester_id,
                        "tenant_id": identity.tenant_id,
                        "role": identity.role,
                        "query_type": query_type,
                        "filter": query_filter,
                    },
                    result_json={
                        "returned_fact_ids": returned_fact_ids,
                        "denied_fact_ids": denied_fact_ids,
                        "source_document_ids": source_document_ids,
                        "denied_document_ids": denied_document_ids,
                        "policy_decision": policy_decision,
                        "policy_reason": policy_reason,
                    },
                )
            )
            self.db.commit()
        except Exception:
            logger.warning("fact_query_audit_write_failed", exc_info=True)
            self.db.rollback()

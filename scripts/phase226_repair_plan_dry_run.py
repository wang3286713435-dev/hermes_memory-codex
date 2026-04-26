#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx
from opensearchpy import OpenSearch
from sqlalchemy import func

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import settings  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.models.chunk import Chunk  # noqa: E402
from app.models.document import Document, DocumentVersion  # noqa: E402
from app.models.fact import Fact  # noqa: E402


@dataclass(frozen=True)
class RepairPlanItem:
    item_type: str
    severity: str
    entity_type: str
    entity_id: str
    issue: str
    recommended_action: str
    reason: str
    source_document_id: str | None = None
    source_version_id: str | None = None
    latest_version_id: str | None = None
    executable: bool = False

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["executable"] = False
        return data


def stale_fact_item(
    *,
    fact_id: str,
    source_document_id: str | None,
    source_version_id: str | None,
    latest_version_id: str | None,
) -> RepairPlanItem:
    return RepairPlanItem(
        item_type="stale_fact",
        severity="warning",
        entity_type="fact",
        entity_id=fact_id,
        source_document_id=source_document_id,
        source_version_id=source_version_id,
        latest_version_id=latest_version_id,
        issue="source_version_is_not_latest",
        recommended_action="revalidate_against_latest",
        reason="confirmed fact points to a superseded source version; do not auto-confirm against latest.",
    )


def missing_source_item(
    *,
    fact_id: str,
    source_document_id: str | None,
    source_version_id: str | None,
    source_chunk_id: str | None,
    missing_fields: list[str],
) -> RepairPlanItem:
    return RepairPlanItem(
        item_type="missing_source",
        severity="critical",
        entity_type="fact",
        entity_id=fact_id,
        source_document_id=source_document_id,
        source_version_id=source_version_id,
        issue="source_reference_missing",
        recommended_action="mark_needs_review",
        reason=f"fact source reference is missing or unresolved: {', '.join(missing_fields)}; do not delete automatically.",
    )


def version_inconsistency_item(
    *,
    document_id: str,
    version_id: str | None,
    issue: str,
    reason: str,
) -> RepairPlanItem:
    return RepairPlanItem(
        item_type="version_inconsistency",
        severity="critical",
        entity_type="version" if version_id else "document",
        entity_id=version_id or document_id,
        source_document_id=document_id,
        source_version_id=version_id,
        issue=issue,
        recommended_action="mark_version_needs_review",
        reason=reason,
    )


def index_inconsistency_item(
    *,
    document_id: str,
    version_id: str | None,
    issue: str,
    recommended_action: str,
    reason: str,
    severity: str = "warning",
) -> RepairPlanItem:
    return RepairPlanItem(
        item_type="index_inconsistency",
        severity=severity,
        entity_type="index",
        entity_id=version_id or document_id,
        source_document_id=document_id,
        source_version_id=version_id,
        issue=issue,
        recommended_action=recommended_action,
        reason=reason,
    )


def service_warning_item(*, service: str, issue: str, reason: str, severity: str = "warning") -> RepairPlanItem:
    return RepairPlanItem(
        item_type="service_warning",
        severity=severity,
        entity_type="service",
        entity_id=service,
        issue=issue,
        recommended_action="inspect_service",
        reason=reason,
    )


def build_repair_plan(items: list[RepairPlanItem], *, generated_at: str | None = None) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()
    item_dicts = [item.as_dict() for item in items]
    critical = sum(1 for item in items if item.severity == "critical")
    warnings = sum(1 for item in items if item.severity == "warning")
    summary = {
        "items_total": len(items),
        "critical": critical,
        "warnings": warnings,
        "stale_facts": sum(1 for item in items if item.item_type == "stale_fact"),
        "missing_sources": sum(1 for item in items if item.item_type == "missing_source"),
        "version_inconsistencies": sum(1 for item in items if item.item_type == "version_inconsistency"),
        "index_inconsistencies": sum(1 for item in items if item.item_type == "index_inconsistency"),
        "failures": critical,
    }
    status = "fail" if critical else "warn" if warnings else "pass"
    return {
        "dry_run": True,
        "destructive_actions": [],
        "executable": False,
        "repair_plan_id": f"phase226-{uuid4()}",
        "generated_at": generated_at,
        "status": status,
        "summary": summary,
        "items": item_dicts,
        "next_steps": _next_steps(summary),
    }


def exit_code_for_summary(summary: dict[str, Any], *, fail_on_critical: bool) -> int:
    if fail_on_critical and summary.get("summary", {}).get("critical", 0) > 0:
        return 1
    return 0


class RepairPlanAuditor:
    def __init__(
        self,
        *,
        document_ids: list[str],
        fact_ids: list[str],
        include_index_checks: bool,
        limit_facts: int,
        limit_documents: int,
    ) -> None:
        self.document_ids = document_ids
        self.fact_ids = fact_ids
        self.include_index_checks = include_index_checks
        self.limit_facts = limit_facts
        self.limit_documents = limit_documents
        self._db = None

    def run(self) -> dict[str, Any]:
        items: list[RepairPlanItem] = []
        try:
            db = self._db_session()
            db.execute(func.now().select())
        except Exception as exc:  # noqa: BLE001 - report, do not crash.
            items.append(
                service_warning_item(
                    service="postgres",
                    issue="database_unavailable",
                    severity="critical",
                    reason=repr(exc),
                )
            )
            return build_repair_plan(items)

        items.extend(self._fact_items())
        items.extend(self._version_items())
        if self.include_index_checks:
            items.extend(self._index_items())
        return build_repair_plan(items)

    def close(self) -> None:
        if self._db is not None:
            self._db.close()

    def _db_session(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def _fact_query(self):
        query = self._db_session().query(Fact)
        if self.fact_ids:
            query = query.filter(Fact.id.in_(self.fact_ids))
        return query.order_by(Fact.updated_at.desc()).limit(self.limit_facts)

    def _fact_items(self) -> list[RepairPlanItem]:
        db = self._db_session()
        items: list[RepairPlanItem] = []
        for fact in self._fact_query().all():
            document = db.get(Document, fact.source_document_id) if fact.source_document_id else None
            version = db.get(DocumentVersion, fact.source_version_id) if fact.source_version_id else None
            chunk = db.get(Chunk, fact.source_chunk_id) if fact.source_chunk_id else None
            missing = []
            if document is None:
                missing.append("source_document_id")
            if version is None:
                missing.append("source_version_id")
            if chunk is None:
                missing.append("source_chunk_id")
            if missing:
                items.append(
                    missing_source_item(
                        fact_id=fact.id,
                        source_document_id=fact.source_document_id,
                        source_version_id=fact.source_version_id,
                        source_chunk_id=fact.source_chunk_id,
                        missing_fields=missing,
                    )
                )
                continue

            if fact.verification_status == "confirmed" and not version.is_latest:
                latest = (
                    db.query(DocumentVersion)
                    .filter(DocumentVersion.document_id == fact.source_document_id, DocumentVersion.is_latest.is_(True))
                    .first()
                )
                items.append(
                    stale_fact_item(
                        fact_id=fact.id,
                        source_document_id=fact.source_document_id,
                        source_version_id=fact.source_version_id,
                        latest_version_id=latest.id if latest else None,
                    )
                )
        return items

    def _sample_document_ids(self) -> list[str]:
        if self.document_ids:
            return self.document_ids
        rows = (
            self._db_session()
            .query(Document.id)
            .join(DocumentVersion, DocumentVersion.document_id == Document.id)
            .group_by(Document.id)
            .order_by(Document.updated_at.desc())
            .limit(self.limit_documents)
            .all()
        )
        return [row[0] for row in rows]

    def _version_items(self) -> list[RepairPlanItem]:
        db = self._db_session()
        items: list[RepairPlanItem] = []
        for document_id in self._sample_document_ids():
            versions = db.query(DocumentVersion).filter(DocumentVersion.document_id == document_id).all()
            latest_versions = [version for version in versions if version.is_latest]
            if not latest_versions:
                items.append(
                    version_inconsistency_item(
                        document_id=document_id,
                        version_id=None,
                        issue="zero_latest_version",
                        reason="document has versions but no latest version; inspect before retrieval use.",
                    )
                )
            elif len(latest_versions) > 1:
                items.append(
                    version_inconsistency_item(
                        document_id=document_id,
                        version_id=None,
                        issue="multiple_latest_versions",
                        reason=f"document has {len(latest_versions)} latest versions; default retrieval may be ambiguous.",
                    )
                )
            for version in versions:
                metadata = version.metadata_json or {}
                if metadata.get("superseded_by_version_id") and (
                    version.is_latest or metadata.get("version_status") == "active"
                ):
                    items.append(
                        version_inconsistency_item(
                            document_id=document_id,
                            version_id=version.id,
                            issue="superseded_version_marked_active_or_latest",
                            reason="version has superseded_by_version_id but still appears active/latest.",
                        )
                    )
        return items

    def _index_items(self) -> list[RepairPlanItem]:
        items: list[RepairPlanItem] = []
        items.extend(self._opensearch_items())
        items.extend(self._qdrant_items())
        return items

    def _opensearch_items(self) -> list[RepairPlanItem]:
        items: list[RepairPlanItem] = []
        try:
            client = OpenSearch(settings.opensearch_url, timeout=3)
            index_name = settings.opensearch_index_chunks
            if not client.indices.exists(index=index_name):
                return [
                    service_warning_item(
                        service="opensearch",
                        issue="index_missing",
                        reason=f"OpenSearch index {index_name} does not exist.",
                    )
                ]
            field_document_id = _opensearch_filter_field(client, index_name, "document_id")
            field_version_id = _opensearch_filter_field(client, index_name, "version_id")
            for document_id in self._sample_document_ids():
                db_count = self._db_session().query(Chunk).filter(Chunk.document_id == document_id).count()
                os_count = _opensearch_count(client, index_name, [{"term": {field_document_id: document_id}}])
                if os_count != db_count:
                    items.append(
                        index_inconsistency_item(
                            document_id=document_id,
                            version_id=None,
                            issue="opensearch_db_chunk_count_mismatch",
                            recommended_action="reindex_opensearch_payload",
                            reason=f"DB chunks={db_count}, OpenSearch chunks={os_count}.",
                        )
                    )
                old_versions = (
                    self._db_session()
                    .query(DocumentVersion)
                    .filter(DocumentVersion.document_id == document_id, DocumentVersion.is_latest.is_(False))
                    .all()
                )
                for version in old_versions:
                    leak_count = _opensearch_count(
                        client,
                        index_name,
                        [
                            {"term": {field_document_id: document_id}},
                            {"term": {field_version_id: version.id}},
                            {"term": {"is_latest": True}},
                        ],
                    )
                    if leak_count:
                        items.append(
                            index_inconsistency_item(
                                document_id=document_id,
                                version_id=version.id,
                                issue="opensearch_superseded_version_latest_leak",
                                recommended_action="reindex_opensearch_payload",
                                severity="critical",
                                reason=f"OpenSearch has {leak_count} chunks for superseded version still marked is_latest=true.",
                            )
                        )
        except Exception as exc:  # noqa: BLE001
            items.append(
                service_warning_item(
                    service="opensearch",
                    issue="service_unavailable",
                    reason=repr(exc),
                )
            )
        return items

    def _qdrant_items(self) -> list[RepairPlanItem]:
        items: list[RepairPlanItem] = []
        try:
            response = httpx.get(_qdrant_url(f"/collections/{settings.qdrant_collection}"), headers=_qdrant_headers(), timeout=5)
            response.raise_for_status()
            for document_id in self._sample_document_ids():
                db_count = self._db_session().query(Chunk).filter(Chunk.document_id == document_id).count()
                qdrant_count = _qdrant_count(document_id)
                if qdrant_count <= 0 and db_count > 0:
                    items.append(
                        index_inconsistency_item(
                            document_id=document_id,
                            version_id=None,
                            issue="qdrant_dense_points_missing",
                            recommended_action="rerun_dense_backfill",
                            reason=f"DB chunks={db_count}, Qdrant dense points={qdrant_count}.",
                        )
                    )
                    continue
                payload = _qdrant_sample_payload(document_id)
                missing_fields = [field for field in ("document_id", "version_id", "chunk_id", "is_latest") if field not in payload]
                if missing_fields:
                    items.append(
                        index_inconsistency_item(
                            document_id=document_id,
                            version_id=payload.get("version_id"),
                            issue="qdrant_payload_missing_required_fields",
                            recommended_action="rerun_dense_backfill",
                            reason=f"Qdrant payload missing fields: {', '.join(missing_fields)}.",
                        )
                    )
        except Exception as exc:  # noqa: BLE001
            items.append(
                service_warning_item(
                    service="qdrant",
                    issue="service_unavailable",
                    reason=repr(exc),
                )
            )
        return items


def _opensearch_filter_field(client: OpenSearch, index_name: str, field: str) -> str:
    mapping = client.indices.get_mapping(index=index_name)
    props = ((mapping.get(index_name) or {}).get("mappings") or {}).get("properties") or {}
    field_def = props.get(field) or {}
    if field_def.get("type") == "text" and (field_def.get("fields") or {}).get("keyword"):
        return f"{field}.keyword"
    return field


def _opensearch_count(client: OpenSearch, index_name: str, filters: list[dict[str, Any]]) -> int:
    data = client.count(index=index_name, body={"query": {"bool": {"filter": filters}}})
    return int(data.get("count") or 0)


def _qdrant_headers() -> dict[str, str]:
    headers: dict[str, str] = {}
    if settings.qdrant_api_key:
        headers["api-key"] = settings.qdrant_api_key
    return headers


def _qdrant_url(path: str) -> str:
    return settings.qdrant_url.rstrip("/") + path


def _qdrant_filter(document_id: str) -> dict[str, Any]:
    return {"must": [{"key": "document_id", "match": {"value": document_id}}]}


def _qdrant_count(document_id: str) -> int:
    response = httpx.post(
        _qdrant_url(f"/collections/{settings.qdrant_collection}/points/count"),
        headers=_qdrant_headers(),
        json={"filter": _qdrant_filter(document_id), "exact": True},
        timeout=10,
    )
    response.raise_for_status()
    return int(((response.json() or {}).get("result") or {}).get("count") or 0)


def _qdrant_sample_payload(document_id: str) -> dict[str, Any]:
    response = httpx.post(
        _qdrant_url(f"/collections/{settings.qdrant_collection}/points/scroll"),
        headers=_qdrant_headers(),
        json={
            "filter": _qdrant_filter(document_id),
            "limit": 1,
            "with_payload": True,
            "with_vector": False,
        },
        timeout=10,
    )
    response.raise_for_status()
    points = (((response.json() or {}).get("result") or {}).get("points") or [])
    if not points:
        return {}
    return dict(points[0].get("payload") or {})


def _next_steps(summary: dict[str, int]) -> list[str]:
    steps: list[str] = []
    if summary["stale_facts"]:
        steps.append("Review stale confirmed facts and revalidate against latest source versions before deeper facts usage.")
    if summary["missing_sources"]:
        steps.append("Review facts with missing sources; consider mark_needs_review or reject_if_source_missing after human approval.")
    if summary["version_inconsistencies"]:
        steps.append("Inspect version state manually before any index or retrieval policy changes.")
    if summary["index_inconsistencies"]:
        steps.append("Plan explicit document_id scoped reindex/backfill only after reviewing this dry-run output.")
    if not steps:
        steps.append("No repair plan items detected; keep running readiness and repair plan dry-runs before rollout planning.")
    return steps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Phase 2.26a read-only repair plan dry-run.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--document-id", action="append", default=[], help="Limit index/version checks to a document id. Can be repeated.")
    parser.add_argument("--fact-id", action="append", default=[], help="Limit fact checks to a fact id. Can be repeated.")
    parser.add_argument("--include-index-checks", action="store_true", help="Include read-only OpenSearch/Qdrant consistency checks.")
    parser.add_argument("--fail-on-critical", action="store_true", help="Exit non-zero if critical plan items are present.")
    parser.add_argument("--limit-facts", type=int, default=100, help="Maximum facts to inspect when --fact-id is not provided.")
    parser.add_argument("--limit-documents", type=int, default=50, help="Maximum documents to inspect when --document-id is not provided.")
    args = parser.parse_args(argv)

    auditor = RepairPlanAuditor(
        document_ids=list(dict.fromkeys(args.document_id)),
        fact_ids=list(dict.fromkeys(args.fact_id)),
        include_index_checks=args.include_index_checks,
        limit_facts=args.limit_facts,
        limit_documents=args.limit_documents,
    )
    try:
        summary = auditor.run()
    finally:
        auditor.close()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return exit_code_for_summary(summary, fail_on_critical=args.fail_on_critical)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

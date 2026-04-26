#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import httpx
from opensearchpy import OpenSearch
from sqlalchemy import func, or_, text

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.core.config import settings  # noqa: E402
from app.db.session import SessionLocal  # noqa: E402
from app.models.audit import AuditLog  # noqa: E402
from app.models.chunk import Chunk  # noqa: E402
from app.models.document import Document, DocumentVersion  # noqa: E402
from app.models.fact import Fact  # noqa: E402
from app.services.indexing.opensearch import OpenSearchChunkIndexer  # noqa: E402

EXPECTED_QDRANT_COLLECTION = "hermes_chunks"
AUDIT_ACTIONS = ("retrieval.query", "fact.query", "fact.search", "fact.confirm", "fact.reject")
REQUIRED_QDRANT_PAYLOAD_FIELDS = ("document_id", "version_id", "chunk_id", "is_latest")


def make_check(name: str, status: str, message: str, **details: Any) -> dict[str, Any]:
    return {"name": name, "status": status, "message": message, "details": details}


def qdrant_collection_config_check(collection: str) -> dict[str, Any]:
    if collection != EXPECTED_QDRANT_COLLECTION:
        return make_check(
            "qdrant_collection_config",
            "fail",
            "QDRANT_COLLECTION is not the expected production/eval collection.",
            expected=EXPECTED_QDRANT_COLLECTION,
            actual=collection,
            impact="dense_eval_false_failure_or_wrong_collection",
        )
    return make_check(
        "qdrant_collection_config",
        "pass",
        "QDRANT_COLLECTION points to the expected collection.",
        expected=EXPECTED_QDRANT_COLLECTION,
        actual=collection,
    )


def stale_facts_check(rows: list[dict[str, Any]]) -> dict[str, Any]:
    stale = [
        {
            "fact_id": row.get("fact_id"),
            "source_document_id": row.get("source_document_id"),
            "source_version_id": row.get("source_version_id"),
            "latest_version_id": row.get("latest_version_id"),
        }
        for row in rows
        if row.get("source_version_id") and row.get("latest_version_id") and row.get("source_version_id") != row.get("latest_version_id")
    ]
    if stale:
        return make_check(
            "confirmed_facts_stale_source_version",
            "warn",
            "Some confirmed facts point to superseded source versions.",
            count=len(stale),
            examples=stale[:20],
        )
    return make_check(
        "confirmed_facts_stale_source_version",
        "pass",
        "No confirmed facts with stale source versions were detected.",
        count=0,
    )


def summarize_section(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = sum(1 for check in checks if check["status"] == "fail")
    warnings = sum(1 for check in checks if check["status"] == "warn")
    passed = sum(1 for check in checks if check["status"] == "pass")
    status = "fail" if failed else "warn" if warnings else "pass"
    return {
        "status": status,
        "checks_total": len(checks),
        "passed": passed,
        "warnings": warnings,
        "failed": failed,
        "checks": checks,
    }


def build_audit_summary(sections: dict[str, dict[str, Any]], recommendations: list[str]) -> dict[str, Any]:
    checks_total = sum(section["checks_total"] for section in sections.values())
    passed = sum(section["passed"] for section in sections.values())
    warnings = sum(section["warnings"] for section in sections.values())
    failed = sum(section["failed"] for section in sections.values())
    status = "fail" if failed else "warn" if warnings else "pass"
    return {
        "status": status,
        "checks_total": checks_total,
        "passed": passed,
        "warnings": warnings,
        "failed": failed,
        **sections,
        "recommendations": recommendations,
        "destructive_actions": [],
        "dry_run": True,
    }


class ReadinessAuditor:
    def __init__(
        self,
        *,
        document_ids: list[str],
        skip_service_check: bool = False,
        run_light_eval: bool = False,
    ) -> None:
        self.document_ids = document_ids
        self.skip_service_check = skip_service_check
        self.run_light_eval = run_light_eval
        self.db_available = False
        self.os_available = False
        self.qdrant_available = False
        self._db = None

    def run(self) -> dict[str, Any]:
        sections = {
            "services": self._check_services(),
            "version_governance": self._check_version_governance(),
            "opensearch_consistency": self._check_opensearch_consistency(),
            "qdrant_consistency": self._check_qdrant_consistency(),
            "facts_governance": self._check_facts_governance(),
            "audit_logs": self._check_audit_logs(),
            "eval_readiness": self._check_eval_readiness(),
        }
        recommendations = self._recommendations(sections)
        return build_audit_summary(sections, recommendations)

    def close(self) -> None:
        if self._db is not None:
            self._db.close()

    def _db_session(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def _check_services(self) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        checks.append(qdrant_collection_config_check(settings.qdrant_collection))
        checks.append(
            make_check(
                "environment_config",
                "pass",
                "Core service endpoints resolved from settings.",
                database_url_configured=bool(settings.database_url),
                opensearch_url=settings.opensearch_url,
                qdrant_url=settings.qdrant_url,
                qdrant_collection=settings.qdrant_collection,
                embedding_key_present=bool(settings.aliyun_embedding_api_key),
                rerank_key_present=bool(settings.aliyun_rerank_api_key),
                env_vars_present={
                    "DATABASE_URL": "DATABASE_URL" in os.environ,
                    "OPENSEARCH_URL": "OPENSEARCH_URL" in os.environ,
                    "QDRANT_URL": "QDRANT_URL" in os.environ,
                    "QDRANT_COLLECTION": "QDRANT_COLLECTION" in os.environ,
                },
            )
        )
        if self.skip_service_check:
            checks.append(make_check("service_connectivity", "warn", "Service connectivity checks skipped by flag."))
            return summarize_section(checks)

        try:
            db = self._db_session()
            db.execute(text("SELECT 1"))
            self.db_available = True
            checks.append(make_check("postgres_connectivity", "pass", "Postgres query succeeded."))
        except Exception as exc:  # noqa: BLE001 - readiness audit must report layer.
            checks.append(make_check("postgres_connectivity", "fail", "Postgres query failed.", error=repr(exc)))

        try:
            client = OpenSearch(settings.opensearch_url, timeout=3)
            if not client.ping():
                raise RuntimeError("OpenSearch ping returned false")
            self.os_available = True
            checks.append(make_check("opensearch_connectivity", "pass", "OpenSearch ping succeeded."))
        except Exception as exc:  # noqa: BLE001
            checks.append(make_check("opensearch_connectivity", "fail", "OpenSearch ping failed.", error=repr(exc)))

        try:
            response = httpx.get(
                _qdrant_url(f"/collections/{settings.qdrant_collection}"),
                headers=_qdrant_headers(),
                timeout=5,
            )
            response.raise_for_status()
            self.qdrant_available = True
            checks.append(make_check("qdrant_connectivity", "pass", "Qdrant collection is reachable."))
        except Exception as exc:  # noqa: BLE001
            checks.append(make_check("qdrant_connectivity", "fail", "Qdrant collection check failed.", error=repr(exc)))

        return summarize_section(checks)

    def _check_version_governance(self) -> dict[str, Any]:
        if not self.db_available:
            return summarize_section([make_check("version_governance", "fail", "Skipped because Postgres is unavailable.")])
        db = self._db_session()
        checks: list[dict[str, Any]] = []

        latest_counts = (
            db.query(DocumentVersion.document_id, func.count(DocumentVersion.id))
            .filter(DocumentVersion.is_latest.is_(True))
            .group_by(DocumentVersion.document_id)
            .all()
        )
        multiple_latest = [{"document_id": document_id, "latest_count": count} for document_id, count in latest_counts if count > 1]
        checks.append(
            make_check(
                "multiple_latest_versions",
                "fail" if multiple_latest else "pass",
                "Documents should not have more than one latest version.",
                count=len(multiple_latest),
                examples=multiple_latest[:20],
            )
        )

        version_doc_ids = {row[0] for row in db.query(DocumentVersion.document_id).distinct().all()}
        latest_doc_ids = {row[0] for row in latest_counts}
        zero_latest = sorted(version_doc_ids - latest_doc_ids)
        checks.append(
            make_check(
                "zero_latest_versions",
                "fail" if zero_latest else "pass",
                "Documents with versions should have exactly one latest version.",
                count=len(zero_latest),
                examples=zero_latest[:20],
            )
        )

        bad_superseded = (
            db.query(DocumentVersion)
            .filter(
                or_(
                    DocumentVersion.is_latest.is_(True),
                    DocumentVersion.metadata_json["version_status"].as_string() == "active",
                )
            )
            .filter(DocumentVersion.metadata_json["superseded_by_version_id"].as_string().isnot(None))
            .limit(20)
            .all()
        )
        checks.append(
            make_check(
                "superseded_marked_active_or_latest",
                "fail" if bad_superseded else "pass",
                "Superseded versions should not remain active/latest.",
                count=len(bad_superseded),
                examples=[
                    {
                        "document_id": version.document_id,
                        "version_id": version.id,
                        "is_latest": version.is_latest,
                        "metadata_json": version.metadata_json,
                    }
                    for version in bad_superseded
                ],
            )
        )

        metadata_mismatch: list[dict[str, Any]] = []
        documents = db.query(Document).filter(Document.metadata_json.isnot(None)).limit(200).all()
        for document in documents:
            current_version_id = (document.metadata_json or {}).get("current_version_id")
            if not current_version_id:
                continue
            version = db.get(DocumentVersion, current_version_id)
            if version is None or version.document_id != document.id or not version.is_latest:
                metadata_mismatch.append(
                    {
                        "document_id": document.id,
                        "current_version_id": current_version_id,
                        "reason": "missing_or_not_latest",
                    }
                )
        checks.append(
            make_check(
                "document_current_version_pointer",
                "warn" if metadata_mismatch else "pass",
                "Document current_version_id should point to the latest version when present.",
                count=len(metadata_mismatch),
                examples=metadata_mismatch[:20],
            )
        )
        return summarize_section(checks)

    def _sample_document_ids(self) -> list[str]:
        if self.document_ids:
            return self.document_ids
        if not self.db_available:
            return []
        return [row[0] for row in self._db_session().query(Document.id).filter(Document.status == "active").limit(3).all()]

    def _check_opensearch_consistency(self) -> dict[str, Any]:
        if not self.db_available or not self.os_available:
            return summarize_section([make_check("opensearch_consistency", "fail", "Skipped because DB or OpenSearch is unavailable.")])
        checks: list[dict[str, Any]] = []
        indexer = OpenSearchChunkIndexer()
        document_ids = self._sample_document_ids()
        if not document_ids:
            checks.append(make_check("opensearch_sample_documents", "warn", "No document ids available for OpenSearch sampling."))
            return summarize_section(checks)

        try:
            indexer.ensure_index()
            checks.append(make_check("opensearch_index", "pass", "OpenSearch index exists or mapping check succeeded.", index=indexer.index_name))
        except Exception as exc:  # noqa: BLE001
            checks.append(make_check("opensearch_index", "fail", "OpenSearch index check failed.", error=repr(exc)))
            return summarize_section(checks)

        mismatches: list[dict[str, Any]] = []
        old_latest_leaks: list[dict[str, Any]] = []
        for document_id in document_ids:
            db_chunk_count = self._db_session().query(Chunk).filter(Chunk.document_id == document_id).count()
            os_count = _opensearch_count(indexer, [{"term": {indexer._resolve_filter_field("document_id"): document_id}}])
            if os_count != db_chunk_count:
                mismatches.append({"document_id": document_id, "db_chunks": db_chunk_count, "opensearch_chunks": os_count})
            old_versions = (
                self._db_session()
                .query(DocumentVersion)
                .filter(DocumentVersion.document_id == document_id, DocumentVersion.is_latest.is_(False))
                .all()
            )
            for version in old_versions:
                leak_count = _opensearch_count(
                    indexer,
                    [
                        {"term": {indexer._resolve_filter_field("document_id"): document_id}},
                        {"term": {indexer._resolve_filter_field("version_id"): version.id}},
                        {"term": {"is_latest": True}},
                    ],
                )
                if leak_count:
                    old_latest_leaks.append({"document_id": document_id, "version_id": version.id, "leaked_chunks": leak_count})

        checks.append(
            make_check(
                "opensearch_db_chunk_count_alignment",
                "warn" if mismatches else "pass",
                "OpenSearch sampled chunk counts should roughly match DB chunks.",
                count=len(mismatches),
                examples=mismatches[:20],
            )
        )
        checks.append(
            make_check(
                "opensearch_superseded_latest_leak",
                "fail" if old_latest_leaks else "pass",
                "Superseded versions should not remain is_latest=true in OpenSearch.",
                count=len(old_latest_leaks),
                examples=old_latest_leaks[:20],
            )
        )
        return summarize_section(checks)

    def _check_qdrant_consistency(self) -> dict[str, Any]:
        checks = [qdrant_collection_config_check(settings.qdrant_collection)]
        if not self.qdrant_available:
            checks.append(make_check("qdrant_consistency", "fail", "Skipped because Qdrant is unavailable."))
            return summarize_section(checks)
        document_ids = self._sample_document_ids()
        if not document_ids:
            checks.append(make_check("qdrant_sample_documents", "warn", "No document ids available for Qdrant sampling."))
            return summarize_section(checks)

        missing_points: list[dict[str, Any]] = []
        missing_payload_fields: list[dict[str, Any]] = []
        for document_id in document_ids:
            count = _qdrant_count(document_id)
            if count <= 0:
                missing_points.append({"document_id": document_id, "points": count})
                continue
            payload = _qdrant_sample_payload(document_id)
            absent = [field for field in REQUIRED_QDRANT_PAYLOAD_FIELDS if field not in payload]
            if absent:
                missing_payload_fields.append({"document_id": document_id, "missing_fields": absent, "payload": payload})

        checks.append(
            make_check(
                "qdrant_dense_points_exist",
                "warn" if missing_points else "pass",
                "Sampled documents should have dense points in Qdrant.",
                count=len(missing_points),
                examples=missing_points[:20],
            )
        )
        checks.append(
            make_check(
                "qdrant_payload_fields",
                "fail" if missing_payload_fields else "pass",
                "Qdrant payload should include document/version/chunk/is_latest fields.",
                count=len(missing_payload_fields),
                examples=missing_payload_fields[:20],
            )
        )
        return summarize_section(checks)

    def _check_facts_governance(self) -> dict[str, Any]:
        if not self.db_available:
            return summarize_section([make_check("facts_governance", "fail", "Skipped because Postgres is unavailable.")])
        db = self._db_session()
        checks: list[dict[str, Any]] = []
        status_counts = dict(db.query(Fact.verification_status, func.count(Fact.id)).group_by(Fact.verification_status).all())
        checks.append(
            make_check(
                "facts_status_counts",
                "pass",
                "Fact status counts collected.",
                confirmed=status_counts.get("confirmed", 0),
                unverified=status_counts.get("unverified", 0),
                rejected=status_counts.get("rejected", 0),
            )
        )

        missing_source = (
            db.query(Fact)
            .filter(Fact.verification_status == "confirmed")
            .filter(or_(Fact.source_document_id.is_(None), Fact.source_version_id.is_(None), Fact.source_chunk_id.is_(None)))
            .limit(20)
            .all()
        )
        checks.append(
            make_check(
                "confirmed_facts_source_fields",
                "fail" if missing_source else "pass",
                "Confirmed facts must retain source document/version/chunk.",
                count=len(missing_source),
                examples=[fact.id for fact in missing_source],
            )
        )

        rows = (
            db.query(Fact, DocumentVersion)
            .outerjoin(DocumentVersion, Fact.source_version_id == DocumentVersion.id)
            .filter(Fact.verification_status == "confirmed")
            .limit(500)
            .all()
        )
        stale_rows: list[dict[str, Any]] = []
        for fact, version in rows:
            latest_version_id = None
            if version is not None and not version.is_latest:
                latest = (
                    db.query(DocumentVersion)
                    .filter(DocumentVersion.document_id == fact.source_document_id, DocumentVersion.is_latest.is_(True))
                    .first()
                )
                latest_version_id = latest.id if latest else None
            stale_rows.append(
                {
                    "fact_id": fact.id,
                    "source_document_id": fact.source_document_id,
                    "source_version_id": fact.source_version_id,
                    "latest_version_id": latest_version_id or fact.source_version_id,
                }
            )
        checks.append(stale_facts_check(stale_rows))

        restricted_rows = (
            db.query(Fact.id, Document.id, Document.metadata_json)
            .join(Document, Fact.source_document_id == Document.id)
            .filter(
                or_(
                    Document.metadata_json["tenant_id"].as_string().isnot(None),
                    Document.metadata_json["allowed_requester_ids"].isnot(None),
                    Document.metadata_json["allowed_roles"].isnot(None),
                )
            )
            .limit(20)
            .all()
        )
        checks.append(
            make_check(
                "facts_restricted_source_documents",
                "pass",
                "Restricted source documents referenced by facts are counted for operator awareness.",
                count=len(restricted_rows),
                examples=[
                    {"fact_id": fact_id, "document_id": document_id, "metadata_json": metadata}
                    for fact_id, document_id, metadata in restricted_rows
                ],
                policy="Fact query service should enforce source document soft policy.",
            )
        )
        return summarize_section(checks)

    def _check_audit_logs(self) -> dict[str, Any]:
        if not self.db_available:
            return summarize_section([make_check("audit_logs", "fail", "Skipped because Postgres is unavailable.")])
        db = self._db_session()
        checks: list[dict[str, Any]] = []
        total = db.query(AuditLog).count()
        action_counts = dict(
            db.query(AuditLog.action, func.count(AuditLog.id))
            .filter(AuditLog.action.in_(AUDIT_ACTIONS))
            .group_by(AuditLog.action)
            .all()
        )
        checks.append(
            make_check(
                "audit_log_presence",
                "warn" if total == 0 else "pass",
                "Audit logs should not be completely empty in a used environment.",
                total=total,
            )
        )
        checks.append(
            make_check(
                "audit_action_counts",
                "warn" if not action_counts else "pass",
                "Key retrieval/fact audit action counts collected.",
                action_counts={action: action_counts.get(action, 0) for action in AUDIT_ACTIONS},
            )
        )
        return summarize_section(checks)

    def _check_eval_readiness(self) -> dict[str, Any]:
        checks: list[dict[str, Any]] = []
        try:
            import scripts.phase214_regression_eval as phase214  # noqa: F401

            checks.append(make_check("phase214_eval_import", "pass", "phase214_regression_eval.py imports successfully."))
        except Exception as exc:  # noqa: BLE001
            checks.append(make_check("phase214_eval_import", "fail", "phase214_regression_eval.py import failed.", error=repr(exc)))

        if self.run_light_eval:
            checks.append(
                make_check(
                    "light_eval_execution",
                    "warn",
                    "Light eval execution skipped to preserve Phase 2.25a read-only dry-run semantics.",
                    requested=True,
                    reason="phase214 eval prepares fixtures and may write test rows",
                )
            )
        else:
            checks.append(make_check("light_eval_execution", "pass", "Light eval not requested; expensive/full eval not run by default."))
        return summarize_section(checks)

    def _recommendations(self, sections: dict[str, dict[str, Any]]) -> list[str]:
        recommendations = []
        if sections["services"]["status"] != "pass":
            recommendations.append("Fix service connectivity/configuration before using readiness results for rollout decisions.")
        if sections["qdrant_consistency"]["status"] != "pass":
            recommendations.append("Verify QDRANT_COLLECTION=hermes_chunks and inspect dense payload consistency.")
        if sections["opensearch_consistency"]["status"] != "pass":
            recommendations.append("Inspect OpenSearch chunk counts and superseded version leakage before rollout readiness.")
        if sections["facts_governance"]["status"] != "pass":
            recommendations.append("Review stale or malformed confirmed facts before enabling deeper facts usage.")
        if not recommendations:
            recommendations.append("Readiness dry-run checks did not find blocking failures; continue with targeted smoke/eval before rollout planning.")
        return recommendations


def _opensearch_count(indexer: OpenSearchChunkIndexer, filters: list[dict[str, Any]]) -> int:
    data = indexer.client.count(index=indexer.index_name, body={"query": {"bool": {"filter": filters}}})
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Phase 2.25a read-only readiness audit dry-run.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument("--document-id", action="append", default=[], help="Document id to sample. Can be repeated.")
    parser.add_argument("--skip-service-check", action="store_true", help="Skip service connectivity checks.")
    parser.add_argument("--run-light-eval", action="store_true", help="Request lightweight eval readiness check.")
    parser.add_argument("--fail-on-warn", action="store_true", help="Exit non-zero when warnings are present.")
    args = parser.parse_args(argv)

    auditor = ReadinessAuditor(
        document_ids=list(dict.fromkeys(args.document_id)),
        skip_service_check=args.skip_service_check,
        run_light_eval=args.run_light_eval,
    )
    try:
        summary = auditor.run()
    finally:
        auditor.close()

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["status"] == "fail":
        return 1
    if args.fail_on_warn and summary["status"] == "warn":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

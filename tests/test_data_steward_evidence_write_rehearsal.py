from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from app.services.asset_catalog.evidence_write_dry_run import (
    build_evidence_write_dry_run_report,
)


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase286a_temp_evidence_write_rehearsal.py"
)


def _rehearsal_module():
    try:
        from app.services.asset_catalog.evidence_write_rehearsal import (
            InMemoryEvidenceWriteRehearsalStore,
            build_evidence_write_rehearsal_report,
            write_evidence_write_rehearsal_report,
        )
    except ModuleNotFoundError as error:  # pragma: no cover - RED phase guard
        pytest.fail(f"evidence write rehearsal module is missing: {error}")
    return (
        InMemoryEvidenceWriteRehearsalStore,
        build_evidence_write_rehearsal_report,
        write_evidence_write_rehearsal_report,
    )


def _cli_main():
    assert SCRIPT_PATH.exists(), "phase286a evidence write rehearsal CLI script is missing"
    script_spec = importlib.util.spec_from_file_location(
        "phase286a_temp_evidence_write_rehearsal",
        SCRIPT_PATH,
    )
    assert script_spec and script_spec.loader
    script_module = importlib.util.module_from_spec(script_spec)
    script_spec.loader.exec_module(script_module)
    return script_module.main


def test_ready_write_dry_run_creates_rehearsal_go() -> None:
    _store_cls, build_report, _write_report = _rehearsal_module()

    report = build_report(_ready_write_dry_run(), created_at="2026-05-15T15:00:00Z")

    assert report["rehearsal_version"] == "nas_evidence_write_rehearsal.v0"
    assert report["decision"]["rehearsal_state"] == "rehearsal_go"
    assert report["dry_run"] is True
    assert report["writes_authorized"] is False
    assert report["temp_store"]["backend"] == "in_memory"
    assert report["temp_store"]["real_hermes_db_used"] is False
    assert len(report["rehearsal_documents"]) == 1
    assert len(report["rehearsal_document_versions"]) == 1
    assert len(report["rehearsal_chunks"]) == 1
    assert len(report["rehearsal_citations"]) == 1
    assert report["rehearsal_documents"][0]["simulated_document_ref"].startswith(
        "simdoc_"
    )
    assert report["rehearsal_chunks"][0]["simulated_chunk_ref"].startswith("simchunk_")
    assert report["rollback"]["rollback_scope"] == "temp_rehearsal_only"
    assert report["safety"]["documents_written"] is False
    assert report["safety"]["document_versions_written"] is False
    assert report["safety"]["chunks_written"] is False
    assert report["safety"]["db_writes"] is False
    assert report["safety"]["agent_answer_integration"] is False


def test_non_go_write_dry_run_becomes_not_allowed() -> None:
    _store_cls, build_report, _write_report = _rehearsal_module()
    write_dry_run = _ready_write_dry_run()
    write_dry_run["decision"]["write_dry_run_state"] = "write_dry_run_not_allowed"

    report = build_report(write_dry_run)

    assert report["decision"]["rehearsal_state"] == "rehearsal_not_allowed"
    assert "write_dry_run_not_go" in report["decision"]["reasons"]
    assert report["rehearsal_documents"] == []


def test_forbidden_input_keys_become_no_go() -> None:
    _store_cls, build_report, _write_report = _rehearsal_module()
    write_dry_run = _ready_write_dry_run()
    write_dry_run["simulated_documents"][0]["scratch_path"] = "/tmp/raw.docx"

    report = build_report(write_dry_run)

    assert report["decision"]["rehearsal_state"] == "rehearsal_no_go"
    assert "forbidden_input_key_scratch_path" in report["decision"]["reasons"]
    assert report["rehearsal_chunks"] == []


def test_in_memory_store_detects_duplicate_rehearsal_by_idempotency_key() -> None:
    store_cls, build_report, _write_report = _rehearsal_module()
    store = store_cls()

    first = build_report(_ready_write_dry_run(), store=store)
    second = build_report(_ready_write_dry_run(), store=store)

    assert first["idempotency"]["duplicates_detected"] == 0
    assert second["idempotency"]["duplicates_detected"] == 1
    assert second["idempotency"]["status"] == "duplicate_detected"
    assert second["decision"]["rehearsal_state"] == "rehearsal_go"


def test_idempotency_conflict_becomes_no_go() -> None:
    store_cls, build_report, _write_report = _rehearsal_module()
    store = store_cls()
    first_input = _ready_write_dry_run()
    conflicting_input = _ready_write_dry_run()
    conflicting_input["simulated_chunks"][0]["redacted_citation_anchor"] = (
        "FileAssetView:hash:asset-001:chunk-9999"
    )

    build_report(first_input, store=store)
    conflict = build_report(conflicting_input, store=store)

    assert conflict["decision"]["rehearsal_state"] == "rehearsal_no_go"
    assert "idempotency_conflict" in conflict["decision"]["reasons"]
    assert conflict["idempotency"]["idempotency_conflict"] is True


def test_rollback_dry_run_lists_temp_only_rehearsal_refs() -> None:
    _store_cls, build_report, _write_report = _rehearsal_module()

    report = build_report(_ready_write_dry_run())

    assert report["rollback"]["rollback_scope"] == "temp_rehearsal_only"
    assert report["rollback"]["source_data_mutation"] is False
    assert report["rollback"]["delete_original_nas_file"] is False
    assert report["rollback"]["delete_platform_db_record"] is False
    assert report["rollback"]["repair_backfill_reindex_cleanup"] is False
    assert report["rollback"]["temp_refs_to_remove"] == [
        report["rehearsal_documents"][0]["rehearsal_document_ref"],
        report["rehearsal_document_versions"][0]["rehearsal_document_version_ref"],
        report["rehearsal_chunks"][0]["rehearsal_chunk_ref"],
        report["rehearsal_citations"][0]["rehearsal_citation_ref"],
    ]


def test_cli_writes_ignored_local_report_and_prints_sanitized_summary(
    tmp_path: Path,
    capsys,
) -> None:
    cli_main = _cli_main()
    write_dry_run_path = tmp_path / "write-dry-run.json"
    write_dry_run_path.write_text(
        json.dumps(_ready_write_dry_run()),
        encoding="utf-8",
    )
    output_dir = tmp_path / "rehearsal"
    sqlite_path = tmp_path / "rehearsal.sqlite"

    exit_code = cli_main(
        [
            "--write-dry-run-json",
            str(write_dry_run_path),
            "--output-dir",
            str(output_dir),
            "--sqlite-path",
            str(sqlite_path),
            "--created-at",
            "2026-05-15T15:00:00Z",
        ]
    )

    summary = json.loads(capsys.readouterr().out)
    reports = list(output_dir.glob("*.json"))

    assert exit_code == 0
    assert len(reports) == 1
    assert summary["decision"] == "go"
    assert summary["rehearsal_state"] == "rehearsal_go"
    assert summary["rehearsal_artifact_generated"] is True
    assert summary["temp_store_backend"] == "sqlite"
    assert summary["documents_written"] is False
    assert summary["document_versions_written"] is False
    assert summary["chunks_written"] is False
    assert summary["db_writes"] is False
    assert summary["opensearch_writes"] is False
    assert summary["qdrant_writes"] is False
    assert summary["minio_writes"] is False
    assert summary["agent_answer_integration"] is False
    assert summary["production_rollout"] is False
    assert str(tmp_path) not in json.dumps(summary, ensure_ascii=False)


def _ready_write_dry_run() -> dict[str, object]:
    return build_evidence_write_dry_run_report(
        _ready_preflight(),
        created_at="2026-05-15T14:00:00Z",
    )


def _ready_preflight() -> dict[str, object]:
    return {
        "preflight_version": "nas_evidence_write_preflight.v0",
        "run_id": "redacted-preflight-001",
        "created_at": "2026-05-15T13:00:00Z",
        "payload_ref": {
            "payload_version": "nas_evidence_write_payload.v0",
            "payload_run_id": "redacted-payload-001",
            "source_view": "FileAssetView",
            "asset_ref": "hash:asset-001",
            "platform_contract_version": "delivery_platform.asset_views.v1.1",
        },
        "idempotency": {
            "idempotency_key": "preflight-key-001",
            "dry_run_document_ref": "payload-document-ref-001",
            "dry_run_chunk_refs": ["payload-chunk-ref-001"],
        },
        "citation_coverage": {
            "complete": True,
            "chunk_count": 1,
            "redacted_citation_anchors": ["FileAssetView:hash:asset-001:chunk-0001"],
        },
        "rollback": {
            "rollback_plan_available": True,
            "rollback_scope": "same_run_only",
        },
        "locks": {
            "lock_required": True,
        },
        "safety": {
            "parser_invoked": False,
            "scratch_copy_performed": False,
            "documents_written": False,
            "chunks_written": False,
            "db_writes": False,
            "opensearch_writes": False,
            "qdrant_writes": False,
            "minio_writes": False,
            "agent_answer_integration": False,
            "production_rollout": False,
        },
        "dry_run": True,
        "writes_authorized": False,
        "decision": {
            "preflight_state": "write_preflight_ready_for_dry_run",
            "reasons": ["all_preflight_gates_passed"],
        },
    }

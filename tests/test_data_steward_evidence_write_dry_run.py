from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase285a_evidence_write_dry_run.py"
)


def _dry_run_module():
    try:
        from app.services.asset_catalog.evidence_write_dry_run import (
            InMemoryEvidenceWriteDryRunStore,
            build_evidence_write_dry_run_report,
            write_evidence_write_dry_run_report,
        )
    except ModuleNotFoundError as error:  # pragma: no cover - RED phase guard
        pytest.fail(f"evidence write dry-run module is missing: {error}")
    return (
        InMemoryEvidenceWriteDryRunStore,
        build_evidence_write_dry_run_report,
        write_evidence_write_dry_run_report,
    )


def _cli_main():
    assert SCRIPT_PATH.exists(), "phase285a evidence write dry-run CLI script is missing"
    script_spec = importlib.util.spec_from_file_location(
        "phase285a_evidence_write_dry_run",
        SCRIPT_PATH,
    )
    assert script_spec and script_spec.loader
    script_module = importlib.util.module_from_spec(script_spec)
    script_spec.loader.exec_module(script_module)
    return script_module.main


def test_ready_preflight_creates_write_dry_run_go() -> None:
    _store_cls, build_report, _write_report = _dry_run_module()

    report = build_report(_ready_preflight(), created_at="2026-05-15T14:00:00Z")

    assert report["write_dry_run_version"] == "nas_evidence_write_dry_run.v0"
    assert report["decision"]["write_dry_run_state"] == "write_dry_run_go"
    assert report["dry_run"] is True
    assert report["writes_authorized"] is False
    assert report["simulated_store"]["backend"] == "in_memory"
    assert len(report["simulated_documents"]) == 1
    assert len(report["simulated_chunks"]) == 1
    assert len(report["simulated_citations"]) == 1
    assert report["simulated_documents"][0]["simulated_document_ref"].startswith(
        "simdoc_"
    )
    assert report["simulated_chunks"][0]["simulated_chunk_ref"].startswith("simchunk_")
    assert report["rollback"]["source_data_mutation"] is False
    assert report["safety"]["documents_written"] is False
    assert report["safety"]["agent_answer_integration"] is False


def test_non_ready_preflight_becomes_not_allowed() -> None:
    _store_cls, build_report, _write_report = _dry_run_module()
    preflight = _ready_preflight()
    preflight["decision"]["preflight_state"] = "write_preflight_not_allowed"

    report = build_report(preflight)

    assert report["decision"]["write_dry_run_state"] == "write_dry_run_not_allowed"
    assert "preflight_not_ready_for_write_dry_run" in report["decision"]["reasons"]
    assert report["simulated_documents"] == []


def test_side_effect_flags_true_becomes_no_go() -> None:
    _store_cls, build_report, _write_report = _dry_run_module()
    preflight = _ready_preflight()
    preflight["safety"]["db_writes"] = True

    report = build_report(preflight)

    assert report["decision"]["write_dry_run_state"] == "write_dry_run_no_go"
    assert "db_writes_true" in report["decision"]["reasons"]
    assert report["writes_authorized"] is False


def test_forbidden_input_keys_become_no_go() -> None:
    _store_cls, build_report, _write_report = _dry_run_module()
    preflight = _ready_preflight()
    preflight["payload_ref"]["nas_path"] = "/Volumes/secret/raw.docx"

    report = build_report(preflight)

    assert report["decision"]["write_dry_run_state"] == "write_dry_run_no_go"
    assert "forbidden_input_key_nas_path" in report["decision"]["reasons"]
    assert report["simulated_chunks"] == []


def test_deterministic_refs_are_stable_across_repeated_builds() -> None:
    _store_cls, build_report, _write_report = _dry_run_module()
    first = build_report(_ready_preflight(), created_at="2026-05-15T14:00:00Z")
    second = build_report(_ready_preflight(), created_at="2026-05-15T14:00:00Z")

    assert first["simulated_documents"] == second["simulated_documents"]
    assert first["simulated_chunks"] == second["simulated_chunks"]
    assert first["simulated_citations"] == second["simulated_citations"]


def test_in_memory_store_detects_duplicate_rerun_by_idempotency_key() -> None:
    store_cls, build_report, _write_report = _dry_run_module()
    store = store_cls()

    first = build_report(_ready_preflight(), store=store)
    second = build_report(_ready_preflight(), store=store)

    assert first["idempotency"]["duplicates_detected"] == 0
    assert second["idempotency"]["duplicates_detected"] == 1
    assert second["idempotency"]["status"] == "duplicate_detected"
    assert second["decision"]["write_dry_run_state"] == "write_dry_run_go"


def test_rollback_dry_run_is_same_run_only_and_source_safe() -> None:
    _store_cls, build_report, _write_report = _dry_run_module()

    report = build_report(_ready_preflight())

    assert report["rollback"]["rollback_scope"] == "same_run_only"
    assert report["rollback"]["source_data_mutation"] is False
    assert report["rollback"]["delete_original_nas_file"] is False
    assert report["rollback"]["delete_platform_db_record"] is False
    assert report["rollback"]["repair_backfill_reindex_cleanup"] is False
    assert report["rollback"]["simulated_refs_to_remove"] == [
        report["simulated_documents"][0]["simulated_document_ref"],
        report["simulated_chunks"][0]["simulated_chunk_ref"],
    ]


def test_cli_writes_ignored_local_report_and_prints_sanitized_summary(
    tmp_path: Path,
    capsys,
) -> None:
    cli_main = _cli_main()
    preflight_path = tmp_path / "preflight.json"
    preflight_path.write_text(json.dumps(_ready_preflight()), encoding="utf-8")
    output_dir = tmp_path / "write_dry_run"

    exit_code = cli_main(
        [
            "--preflight-json",
            str(preflight_path),
            "--output-dir",
            str(output_dir),
            "--created-at",
            "2026-05-15T14:00:00Z",
        ]
    )

    summary = json.loads(capsys.readouterr().out)
    reports = list(output_dir.glob("*.json"))

    assert exit_code == 0
    assert len(reports) == 1
    assert summary["decision"] == "go"
    assert summary["write_dry_run_state"] == "write_dry_run_go"
    assert summary["write_dry_run_artifact_generated"] is True
    assert summary["documents_written"] is False
    assert summary["chunks_written"] is False
    assert summary["db_writes"] is False
    assert summary["opensearch_writes"] is False
    assert summary["qdrant_writes"] is False
    assert summary["minio_writes"] is False
    assert summary["agent_answer_integration"] is False
    assert summary["production_rollout"] is False
    assert "/Users/" not in json.dumps(summary, ensure_ascii=False)


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

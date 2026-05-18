from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.chunk import Chunk
from app.models.document import Document

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase291_runtime_evidence_write_smoke.py"
)


def _smoke_module():
    try:
        from app.services.asset_catalog.evidence_write_runtime_smoke import (
            RUNTIME_SMOKE_REPORT_VERSION,
            build_runtime_evidence_writer_smoke_report,
            write_runtime_evidence_writer_smoke_report,
        )
    except ModuleNotFoundError as error:  # pragma: no cover - RED phase guard
        pytest.fail(f"runtime evidence writer smoke module is missing: {error}")
    return (
        RUNTIME_SMOKE_REPORT_VERSION,
        build_runtime_evidence_writer_smoke_report,
        write_runtime_evidence_writer_smoke_report,
    )


def _cli_main():
    assert SCRIPT_PATH.exists(), "phase291 runtime evidence writer smoke CLI is missing"
    script_spec = importlib.util.spec_from_file_location(
        "phase291_runtime_evidence_write_smoke",
        SCRIPT_PATH,
    )
    assert script_spec and script_spec.loader
    script_module = importlib.util.module_from_spec(script_spec)
    script_spec.loader.exec_module(script_module)
    return script_module.main


def test_gate_only_success_returns_ready_without_invoking_writer() -> None:
    version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    approval = _ready_approval(payload)

    report = build_report(
        approval=approval,
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
        worktree_status_text="",
    )

    assert version == "hermes_runtime_evidence_writer_smoke.v0"
    assert report["report_version"] == version
    assert report["decision"] == "writer_smoke_ready_for_operator_stop"
    assert report["would_invoke_writer"] is False
    assert report["writer_invoked"] is False
    assert report["db_writes"] is False
    assert report["created_counts"] == _empty_counts()
    assert report["sanitized"] is True
    assert report["pause_reasons"] == []
    assert report["no_go_reasons"] == []
    assert report["forbidden_actions"]["opensearch_written"] is False
    assert report["preflight_state"] == "preflight_ready_for_operator_stop"


def test_non_ready_preflight_returns_no_go() -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()

    report = build_report(
        approval=_ready_approval(payload),
        preflight_report=_ready_preflight_report("preflight_pause"),
        payload=payload,
        expected_git_commit="3ee37e3",
    )

    assert report["decision"] == "writer_smoke_no_go"
    assert "preflight_not_ready" in report["no_go_reasons"]
    assert report["writer_invoked"] is False


def test_payload_with_forbidden_raw_fields_returns_no_go() -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    payload["chunks"][0]["raw_text"] = "forbidden raw business content"

    report = build_report(
        approval=_ready_approval(payload),
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
    )

    assert report["decision"] == "writer_smoke_no_go"
    assert "forbidden_payload_key_raw_text" in report["no_go_reasons"]
    assert report["writer_invoked"] is False


def test_scope_larger_than_one_document_one_version_or_twenty_chunks_is_no_go() -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    payload["chunks"] = [
        {
            **payload["chunks"][0],
            "chunk_index": index,
            "chunk_ref": f"chunk-{index}",
            "sanitized_text": f"sanitized test chunk {index}",
            "sanitized_quote": f"sanitized quote {index}",
        }
        for index in range(21)
    ]

    report = build_report(
        approval=_ready_approval(payload),
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
    )

    assert report["decision"] == "writer_smoke_no_go"
    assert "chunk_scope_exceeds_20" in report["no_go_reasons"]
    assert report["writer_invoked"] is False


@pytest.mark.parametrize(
    "flag",
    [
        "PLATFORM_ASSET_PARSER_ENABLED",
        "PLATFORM_ASSET_INDEX_WRITE_ENABLED",
        "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED",
        "PLATFORM_ASSET_ROLLOUT_ENABLED",
    ],
)
def test_forbidden_parser_index_agent_or_rollout_flag_is_no_go(flag: str) -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    payload["feature_flags"][flag] = True
    approval = _ready_approval(payload)
    approval["feature_flags_expected"][flag] = True

    report = build_report(
        approval=approval,
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
    )

    assert report["decision"] == "writer_smoke_no_go"
    assert f"forbidden_feature_flag_true_{flag}" in report["no_go_reasons"]
    assert report["forbidden_actions"]["parser_executed"] is False


def test_temp_sqlite_execution_invokes_writer_and_reports_created_counts() -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    db = _db_session()

    report = build_report(
        approval=_ready_approval(payload),
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
        execute_writer=True,
        db=db,
    )

    assert report["decision"] == "writer_smoke_executed"
    assert report["would_invoke_writer"] is True
    assert report["writer_invoked"] is True
    assert report["db_writes"] is True
    assert report["created_counts"] == {
        "documents": 1,
        "document_versions": 1,
        "chunks": 2,
        "citations": 2,
    }
    assert report["idempotency_status"] == "created"
    assert len(report["rollback_dry_run_before"]["rows_by_model"]["Document"]) == 0
    assert len(report["rollback_dry_run_after"]["rows_by_model"]["Chunk"]) == 2
    assert db.query(Document).count() == 1
    assert db.query(Chunk).count() == 2


def test_idempotency_duplicate_creates_zero_new_rows() -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    approval = _ready_approval(payload)
    db = _db_session()

    first = build_report(
        approval=approval,
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
        execute_writer=True,
        db=db,
    )
    second = build_report(
        approval=approval,
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
        execute_writer=True,
        db=db,
    )

    assert first["decision"] == "writer_smoke_executed"
    assert second["decision"] == "writer_smoke_executed"
    assert second["created_counts"] == _empty_counts()
    assert second["idempotency_status"] == "duplicate_detected"
    assert db.query(Document).count() == 1


def test_rollback_dry_run_after_execution_is_scoped_to_write_run_id() -> None:
    _version, build_report, _write_report = _smoke_module()
    payload = _ready_payload()
    db = _db_session()

    report = build_report(
        approval=_ready_approval(payload),
        preflight_report=_ready_preflight_report(),
        payload=payload,
        expected_git_commit="3ee37e3",
        execute_writer=True,
        db=db,
    )

    rows = report["rollback_dry_run_after"]["rows_by_model"]
    assert report["rollback_dry_run_after"]["write_run_id"] == "runtime-write-run-001"
    assert rows.keys() == {"Document", "DocumentVersion", "Chunk", "CitationRecord"}
    assert len(rows["Document"]) == 1
    assert len(rows["DocumentVersion"]) == 1
    assert len(rows["Chunk"]) == 2
    assert len(rows["CitationRecord"]) == 2
    assert report["rollback_dry_run_after"]["delete_rows"] is False
    assert report["rollback_dry_run_after"]["executable"] is False


def test_cli_writes_sanitized_gate_only_report(tmp_path: Path, capsys) -> None:
    cli_main = _cli_main()
    payload = _ready_payload()
    approval_path = tmp_path / "approval.json"
    preflight_path = tmp_path / "preflight.json"
    payload_path = tmp_path / "payload.json"
    worktree_path = tmp_path / "worktree.txt"
    output_path = tmp_path / "phase291-runtime-smoke.json"
    approval_path.write_text(json.dumps(_ready_approval(payload)), encoding="utf-8")
    preflight_path.write_text(json.dumps(_ready_preflight_report()), encoding="utf-8")
    payload_path.write_text(json.dumps(payload), encoding="utf-8")
    worktree_path.write_text("", encoding="utf-8")

    exit_code = cli_main(
        [
            "--approval-json",
            str(approval_path),
            "--preflight-report",
            str(preflight_path),
            "--payload-json",
            str(payload_path),
            "--output",
            str(output_path),
            "--expected-git-commit",
            "3ee37e3",
            "--worktree-status-file",
            str(worktree_path),
        ]
    )

    summary_text = capsys.readouterr().out
    report_text = output_path.read_text(encoding="utf-8")
    summary = json.loads(summary_text)
    report = json.loads(report_text)

    assert exit_code == 0
    assert summary["decision"] == "writer_smoke_ready_for_operator_stop"
    assert summary["writer_invoked"] is False
    assert summary["db_writes"] is False
    assert summary["smoke_report_filename"] == output_path.name
    assert report["writer_invoked"] is False
    assert "sanitized evidence chunk one" not in report_text
    assert "true_nas_path" not in report_text
    assert str(tmp_path) not in summary_text


def _db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _ready_payload() -> dict:
    return {
        "payload_version": "hermes_evidence_only_payload.v0",
        "payload_fingerprint": "payload-fingerprint-001",
        "target_environment": "test_machine_only",
        "feature_flags": {
            "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED": True,
            "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED": True,
            "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED": False,
            "PLATFORM_ASSET_INDEX_WRITE_ENABLED": False,
            "PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED": False,
            "PLATFORM_ASSET_PARSER_ENABLED": False,
            "PLATFORM_ASSET_ROLLOUT_ENABLED": False,
        },
        "operator_approval": {
            "approval_id": "approval-001",
            "writes_authorized": True,
            "target_environment": "test_machine_only",
            "target_git_commit": "3ee37e3",
            "write_run_id": "runtime-write-run-001",
            "source_asset_ref": "asset-ref-001",
            "project_scope": "project-scope-001",
            "permission_proof_ref": "permission-proof-001",
            "rollback_dry_run_ref": "rollback-ref-001",
            "max_documents": 1,
            "max_document_versions": 1,
            "max_chunks": 20,
        },
        "write_run_id": "runtime-write-run-001",
        "source_system": "platform_asset_catalog",
        "source_asset_ref": "asset-ref-001",
        "project_scope": "project-scope-001",
        "permission_proof_ref": "permission-proof-001",
        "rollback_dry_run_ref": "rollback-ref-001",
        "idempotency": {"idempotency_key": "runtime-idempotency-001"},
        "document": {
            "title": "redacted evidence document",
            "source_type": "platform_asset",
            "source_uri": "asset-ref:asset-ref-001",
            "document_type": "sanitized_test_evidence",
            "confidentiality_level": "internal",
            "status": "active",
        },
        "document_version": {
            "version_name": "test-smoke-v1",
            "version_number": "v1",
            "file_hash": "redacted-file-hash",
            "content_hash": "redacted-content-hash",
            "parse_status": "parsed",
        },
        "chunks": [
            {
                "chunk_ref": "chunk-1",
                "chunk_index": 0,
                "sanitized_text": "sanitized evidence chunk one",
                "sanitized_quote": "sanitized quote one",
                "heading_path": ["redacted heading"],
                "page_start": 1,
                "page_end": 1,
                "content_hash": "chunk-hash-1",
                "source_type": "platform_asset",
                "permission_tags": ["project:project-scope-001"],
            },
            {
                "chunk_ref": "chunk-2",
                "chunk_index": 1,
                "sanitized_text": "sanitized evidence chunk two",
                "sanitized_quote": "sanitized quote two",
                "heading_path": ["redacted heading"],
                "page_start": 2,
                "page_end": 2,
                "content_hash": "chunk-hash-2",
                "source_type": "platform_asset",
                "permission_tags": ["project:project-scope-001"],
            },
        ],
    }


def _ready_approval(payload: dict) -> dict:
    return {
        "approval_version": "hermes_evidence_write_operator_approval.v1",
        "approval_id": "approval-001",
        "approved_by": "operator-a",
        "approved_at": "2026-05-18T00:00:00Z",
        "expires_at": "2099-01-01T00:00:00Z",
        "target_environment": "test_machine_only",
        "target_git_commit": "3ee37e3",
        "source_system": "platform_asset_catalog",
        "source_asset_ref": payload["source_asset_ref"],
        "project_scope": payload["project_scope"],
        "permission_proof_ref": payload["permission_proof_ref"],
        "sanitized_manifest_ref": "sanitized-manifest-ref-001",
        "eligibility_report_ref": "eligibility-report-ref-001",
        "payload_plan_ref": "payload-plan-ref-001",
        "preflight_report_ref": "preflight-report-ref-001",
        "dry_run_ref": "dry-run-ref-001",
        "rehearsal_ref": "rehearsal-ref-001",
        "rollback_dry_run_ref": payload["rollback_dry_run_ref"],
        "write_run_id": payload["write_run_id"],
        "evidence_write_idempotency_key": payload["idempotency"]["idempotency_key"],
        "expected_payload_fingerprint": payload["payload_fingerprint"],
        "max_documents": 1,
        "max_document_versions": 1,
        "max_chunks": 20,
        "allowed_write_action": "first_real_hermes_evidence_write_smoke",
        "feature_flags_expected": dict(payload["feature_flags"]),
        "writes_authorized": True,
    }


def _ready_preflight_report(state: str = "preflight_ready_for_operator_stop") -> dict:
    return {
        "runtime_preflight_version": "runtime_evidence_write_preflight.v0",
        "decision": {
            "runtime_preflight_state": state,
            "reasons": ["all_runtime_preflight_gates_passed"],
        },
        "git": {
            "expected_git_commit": "3ee37e3",
            "target_git_commit_matches": True,
            "worktree_clean": True,
        },
        "safety": {
            "writer_invoked": False,
            "db_writes": False,
            "parser_invoked": False,
            "file_copied": False,
            "nas_scanned": False,
            "opensearch_writes": False,
            "qdrant_writes": False,
            "minio_writes": False,
            "agent_answer_integration": False,
            "production_rollout": False,
        },
        "would_invoke_writer": False,
        "writes_authorized": False,
        "dry_run": True,
        "report_refs": [
            {
                "field": "permission_proof_ref",
                "exists": True,
                "appears_sanitized": True,
            }
        ],
    }


def _empty_counts() -> dict[str, int]:
    return {
        "documents": 0,
        "document_versions": 0,
        "chunks": 0,
        "citations": 0,
    }

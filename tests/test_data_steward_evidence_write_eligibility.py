from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from app.services.asset_catalog.evidence_eligibility import (
    build_evidence_write_eligibility_report,
    write_evidence_write_eligibility_report,
)

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase282a_evidence_write_eligibility.py"
)
SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "phase282a_evidence_write_eligibility",
    SCRIPT_PATH,
)
assert SCRIPT_SPEC and SCRIPT_SPEC.loader
SCRIPT_MODULE = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(SCRIPT_MODULE)
cli_main = SCRIPT_MODULE.main


def test_report_marks_manifest_eligible_only_with_human_review_approval() -> None:
    report = build_evidence_write_eligibility_report(
        _ready_manifest(),
        human_review_decision="approve_for_evidence_write_planning",
        created_at="2026-05-15T10:00:00Z",
    )

    assert report["report_version"] == "nas_evidence_write_eligibility.v0"
    assert report["run_id"] == "redacted-run-001"
    assert report["eligibility_state"] == "eligible_for_evidence_write_planning"
    assert report["human_review_decision"] == "approve_for_evidence_write_planning"
    assert report["writes_authorized"] is False
    assert report["agent_answer_integration"] is False
    assert report["gates"]["manifest_ready_for_review"] is True
    assert report["gates"]["human_review_approved_for_planning"] is True
    assert report["reasons"] == ["all_planning_gates_passed"]


def test_report_without_human_approval_stays_eligible_for_review_only() -> None:
    report = build_evidence_write_eligibility_report(
        _ready_manifest(),
        human_review_decision="needs_more_metadata",
    )

    assert report["eligibility_state"] == "eligible_for_human_review"
    assert report["writes_authorized"] is False
    assert "human_review_not_approved_for_planning" in report["reasons"]


def test_report_fails_closed_when_permission_proof_is_missing() -> None:
    manifest = _ready_manifest()
    manifest["source"]["project_scope_proven"] = False
    manifest["source"]["permission_proof_status"] = "missing"

    report = build_evidence_write_eligibility_report(
        manifest,
        human_review_decision="approve_for_evidence_write_planning",
    )

    assert report["eligibility_state"] == "not_eligible"
    assert report["permission_default"] == "DENIED"
    assert "project_scope_not_proven" in report["reasons"]
    assert "permission_proof_not_valid" in report["reasons"]
    assert report["writes_authorized"] is False


def test_report_marks_no_go_when_manifest_contains_write_or_answer_side_effects() -> None:
    manifest = _ready_manifest()
    manifest["decision"]["manifest_status"] = "no_go"
    manifest["safety"]["documents_written"] = True
    manifest["safety"]["agent_answer_integration"] = True

    report = build_evidence_write_eligibility_report(
        manifest,
        human_review_decision="approve_for_evidence_write_planning",
    )

    assert report["eligibility_state"] == "no_go"
    assert "manifest_no_go" in report["reasons"]
    assert "documents_written_true" in report["reasons"]
    assert "agent_answer_integration_true" in report["reasons"]
    assert report["writes_authorized"] is False


def test_write_report_is_sanitized_and_ignored_artifact_friendly(tmp_path: Path) -> None:
    report = build_evidence_write_eligibility_report(
        _ready_manifest(),
        human_review_decision="approve_for_evidence_write_planning",
    )

    output_path = write_evidence_write_eligibility_report(tmp_path, report)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    output_text = output_path.read_text(encoding="utf-8")

    assert output_path.name == "redacted-run-001-eligibility.json"
    assert payload["eligibility_state"] == "eligible_for_evidence_write_planning"
    assert "/Users/" not in output_text
    assert "secret.pdf" not in output_text
    assert "真实正文" not in output_text


def test_cli_writes_report_and_prints_sanitized_summary(
    tmp_path: Path,
    capsys,
) -> None:
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_ready_manifest()), encoding="utf-8")
    output_dir = tmp_path / "eligibility"

    exit_code = cli_main(
        [
            "--manifest-json",
            str(manifest_path),
            "--output-dir",
            str(output_dir),
            "--human-review-decision",
            "approve_for_evidence_write_planning",
            "--created-at",
            "2026-05-15T10:00:00Z",
        ]
    )

    summary = json.loads(capsys.readouterr().out)
    report_path = output_dir / "redacted-run-001-eligibility.json"

    assert exit_code == 0
    assert report_path.exists()
    assert summary["decision"] == "go"
    assert summary["eligibility_state"] == "eligible_for_evidence_write_planning"
    assert summary["eligibility_report_generated"] is True
    assert summary["writes_authorized"] is False
    assert summary["agent_answer_integration"] is False
    assert "/Users/" not in json.dumps(summary, ensure_ascii=False)


def _ready_manifest() -> dict[str, object]:
    return {
        "manifest_version": "nas_evidence_manifest.v0",
        "run_id": "redacted-run-001",
        "created_at": "2026-05-15T09:00:00Z",
        "source": {
            "asset_ref": "hash:asset-001",
            "source_view": "FileAssetView",
            "project_scope_proven": True,
            "permission_proof_status": "valid",
            "storage_locator_present": True,
        },
        "sample": {
            "file_type": "pdf",
            "size_bucket": "lt_1mb",
            "confidentiality_status": "known",
            "lifecycle_status": "active",
            "index_eligibility_status": "eligible_for_preview",
        },
        "parser_preview": {
            "parser_status": "parsed",
            "parser_type": "pdf-sanitized-preview",
            "text_length_bucket": "small",
            "structure_summary": {
                "page_count_bucket": "two_to_five",
                "sheet_count_bucket": "none",
                "slide_count_bucket": "none",
                "row_count_bucket": "none",
            },
            "warnings": [],
        },
        "safety": {
            "raw_text_output": False,
            "true_filename_output": False,
            "true_nas_path_output": False,
            "raw_row_output": False,
            "secret_printed": False,
            "true_business_data_output": False,
            "documents_written": False,
            "chunks_written": False,
            "db_writes": False,
            "opensearch_writes": False,
            "qdrant_writes": False,
            "minio_writes": False,
            "agent_answer_integration": False,
        },
        "cleanup": {
            "scratch_cleanup_status": "all_deleted",
            "preview_cleanup_status": "all_deleted",
        },
        "decision": {
            "manifest_status": "ready_for_review",
            "next_allowed_phase": "review_only",
            "reasons": ["sanitized_preview_ready"],
        },
    }

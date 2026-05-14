from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from app.services.asset_catalog.evidence_payload import (
    build_evidence_write_payload_plan,
    write_evidence_write_payload_plan,
)

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase283a_evidence_write_payload.py"
)
SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "phase283a_evidence_write_payload",
    SCRIPT_PATH,
)
assert SCRIPT_SPEC and SCRIPT_SPEC.loader
SCRIPT_MODULE = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(SCRIPT_MODULE)
cli_main = SCRIPT_MODULE.main


def test_payload_plan_is_ready_for_write_dry_run_from_eligible_report() -> None:
    payload = build_evidence_write_payload_plan(
        _eligible_report(),
        human_review_decision="approve_for_payload_dry_run_planning",
        created_at="2026-05-15T12:00:00Z",
    )

    assert payload["payload_version"] == "nas_evidence_write_payload.v0"
    assert payload["run_id"] == "redacted-run-001"
    assert payload["decision"]["payload_state"] == "payload_ready_for_write_dry_run"
    assert payload["decision"]["reasons"] == ["all_payload_planning_gates_passed"]
    assert payload["dry_run"] is True
    assert payload["writes_authorized"] is False
    assert payload["candidate_document"]["external_source_type"] == "platform_asset_catalog"
    assert payload["candidate_document"]["document_write_mode"] == "dry_run_only"
    assert payload["candidate_chunks"][0]["chunk_write_mode"] == "dry_run_only"
    assert payload["candidate_chunks"][0]["raw_text_present"] is False
    assert payload["citation_contract"]["cite_scratch_path"] is False
    assert payload["safety"]["documents_written"] is False
    assert payload["safety"]["agent_answer_integration"] is False


def test_payload_plan_requires_eligible_report_state() -> None:
    report = _eligible_report()
    report["eligibility_state"] = "eligible_for_human_review"

    payload = build_evidence_write_payload_plan(
        report,
        human_review_decision="approve_for_payload_dry_run_planning",
    )

    assert payload["decision"]["payload_state"] == "payload_not_allowed"
    assert "eligibility_not_ready_for_payload_planning" in payload["decision"]["reasons"]
    assert payload["writes_authorized"] is False


def test_payload_plan_no_go_when_safety_side_effects_are_present() -> None:
    report = _eligible_report()
    report["documents_written"] = True
    report["agent_answer_integration"] = True

    payload = build_evidence_write_payload_plan(
        report,
        human_review_decision="approve_for_payload_dry_run_planning",
    )

    assert payload["decision"]["payload_state"] == "payload_no_go"
    assert "documents_written_true" in payload["decision"]["reasons"]
    assert "agent_answer_integration_true" in payload["decision"]["reasons"]
    assert payload["writes_authorized"] is False


def test_payload_plan_rejects_forbidden_raw_fields() -> None:
    report = _eligible_report()
    report["source"]["true_filename"] = "secret.pdf"
    report["raw_text"] = "真实正文"

    payload = build_evidence_write_payload_plan(
        report,
        human_review_decision="approve_for_payload_dry_run_planning",
    )

    assert payload["decision"]["payload_state"] == "payload_no_go"
    assert "forbidden_report_key_raw_text" in payload["decision"]["reasons"]
    assert "forbidden_report_key_true_filename" in payload["decision"]["reasons"]
    assert payload["candidate_chunks"] == []


def test_write_payload_plan_is_sanitized_and_ignored_artifact_friendly(tmp_path: Path) -> None:
    payload = build_evidence_write_payload_plan(
        _eligible_report(),
        human_review_decision="approve_for_payload_dry_run_planning",
    )

    output_path = write_evidence_write_payload_plan(tmp_path, payload)
    output_text = output_path.read_text(encoding="utf-8")
    saved = json.loads(output_text)

    assert output_path.name == "redacted-run-001-payload.json"
    assert saved["decision"]["payload_state"] == "payload_ready_for_write_dry_run"
    assert "/Users/" not in output_text
    assert "secret.pdf" not in output_text
    assert "真实正文" not in output_text


def test_cli_writes_payload_plan_and_prints_sanitized_summary(
    tmp_path: Path,
    capsys,
) -> None:
    report_path = tmp_path / "eligibility.json"
    report_path.write_text(json.dumps(_eligible_report()), encoding="utf-8")
    output_dir = tmp_path / "payloads"

    exit_code = cli_main(
        [
            "--eligibility-json",
            str(report_path),
            "--output-dir",
            str(output_dir),
            "--human-review-decision",
            "approve_for_payload_dry_run_planning",
            "--created-at",
            "2026-05-15T12:00:00Z",
        ]
    )

    summary = json.loads(capsys.readouterr().out)
    payload_path = output_dir / "redacted-run-001-payload.json"

    assert exit_code == 0
    assert payload_path.exists()
    assert summary["decision"] == "go"
    assert summary["payload_state"] == "payload_ready_for_write_dry_run"
    assert summary["payload_artifact_generated"] is True
    assert summary["writes_authorized"] is False
    assert summary["documents_written"] is False
    assert summary["agent_answer_integration"] is False
    assert "/Users/" not in json.dumps(summary, ensure_ascii=False)


def _eligible_report() -> dict[str, object]:
    return {
        "report_version": "nas_evidence_write_eligibility.v0",
        "run_id": "redacted-run-001",
        "created_at": "2026-05-15T10:00:00Z",
        "source": {
            "asset_ref": "hash:asset-001",
            "source_view": "FileAssetView",
            "project_scope_proven": True,
            "permission_proof_status": "valid",
            "storage_locator_present": True,
        },
        "sample": {
            "file_type": "pdf",
            "confidentiality_status": "known",
            "lifecycle_status": "active",
            "index_eligibility_status": "eligible_for_preview",
        },
        "human_review_decision": "approve_for_evidence_write_planning",
        "eligibility_state": "eligible_for_evidence_write_planning",
        "permission_default": "DENIED",
        "gates": {
            "manifest_version_supported": True,
            "manifest_ready_for_review": True,
            "project_scope_proven": True,
            "permission_proof_valid": True,
            "storage_locator_present": True,
            "parser_parsed": True,
            "text_length_present": True,
            "cleanup_all_deleted": True,
            "safety_flags_clear": True,
            "no_forbidden_manifest_keys": True,
            "index_eligibility_preview": True,
            "confidentiality_known": True,
            "lifecycle_active": True,
            "file_type_supported": True,
            "human_review_approved_for_planning": True,
        },
        "reasons": ["all_planning_gates_passed"],
        "writes_authorized": False,
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
    }

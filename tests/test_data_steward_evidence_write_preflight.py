from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase284a_evidence_write_preflight.py"
)


def _preflight_module():
    try:
        from app.services.asset_catalog.evidence_preflight import (
            build_evidence_write_preflight_report,
            write_evidence_write_preflight_report,
        )
    except ModuleNotFoundError as error:  # pragma: no cover - RED phase guard
        pytest.fail(f"preflight module is missing: {error}")
    return build_evidence_write_preflight_report, write_evidence_write_preflight_report


def _cli_main():
    assert SCRIPT_PATH.exists(), "phase284a preflight CLI script is missing"
    script_spec = importlib.util.spec_from_file_location(
        "phase284a_evidence_write_preflight",
        SCRIPT_PATH,
    )
    assert script_spec and script_spec.loader
    script_module = importlib.util.module_from_spec(script_spec)
    script_spec.loader.exec_module(script_module)
    return script_module.main


def test_preflight_is_ready_for_dry_run_from_ready_payload_and_approval() -> None:
    build_preflight, _ = _preflight_module()

    preflight = build_preflight(
        _ready_payload(),
        operator_approval=_operator_approval(),
        created_at="2026-05-15T13:00:00Z",
    )

    assert preflight["preflight_version"] == "nas_evidence_write_preflight.v0"
    assert preflight["payload_ref"]["payload_run_id"] == "redacted-run-001"
    assert preflight["operator_approval"]["approved"] is True
    assert preflight["write_scope"]["document_count"] == 1
    assert preflight["write_scope"]["chunk_count"] == 1
    assert preflight["idempotency"]["idempotency_key"].startswith("preflight-")
    assert preflight["idempotency"]["duplicate_write_allowed"] is False
    assert preflight["rollback"]["rollback_plan_available"] is True
    assert preflight["rollback"]["source_data_mutation"] is False
    assert preflight["citation_coverage"]["complete"] is True
    assert preflight["locks"]["lock_required"] is True
    assert preflight["locks"]["lock_created"] is False
    assert preflight["dry_run"] is True
    assert preflight["writes_authorized"] is False
    assert preflight["safety"]["documents_written"] is False
    assert preflight["safety"]["agent_answer_integration"] is False
    assert preflight["decision"]["preflight_state"] == "write_preflight_ready_for_dry_run"
    assert preflight["decision"]["reasons"] == ["all_preflight_gates_passed"]


def test_preflight_requires_payload_ready_state() -> None:
    build_preflight, _ = _preflight_module()
    payload = _ready_payload()
    payload["decision"]["payload_state"] = "payload_ready_for_human_review"

    preflight = build_preflight(
        payload,
        operator_approval=_operator_approval(),
    )

    assert preflight["decision"]["preflight_state"] == "write_preflight_not_allowed"
    assert "payload_not_ready_for_write_preflight" in preflight["decision"]["reasons"]
    assert preflight["writes_authorized"] is False


def test_preflight_no_go_when_payload_has_side_effects() -> None:
    build_preflight, _ = _preflight_module()
    payload = _ready_payload()
    payload["writes_authorized"] = True
    payload["safety"]["documents_written"] = True

    preflight = build_preflight(
        payload,
        operator_approval=_operator_approval(),
    )

    assert preflight["decision"]["preflight_state"] == "write_preflight_no_go"
    assert "writes_authorized_true" in preflight["decision"]["reasons"]
    assert "documents_written_true" in preflight["decision"]["reasons"]
    assert preflight["writes_authorized"] is False


def test_preflight_fails_closed_without_matching_operator_approval() -> None:
    build_preflight, _ = _preflight_module()
    approval = _operator_approval()
    approval["payload_run_id"] = "different-run"

    preflight = build_preflight(
        _ready_payload(),
        operator_approval=approval,
    )

    assert preflight["decision"]["preflight_state"] == "write_preflight_not_allowed"
    assert "operator_approval_payload_run_id_mismatch" in preflight["decision"]["reasons"]
    assert preflight["operator_approval"]["permission_default"] == "DENIED"


def test_preflight_rejects_scope_exceeding_approval_caps() -> None:
    build_preflight, _ = _preflight_module()
    approval = _operator_approval()
    approval["max_chunk_count"] = 0

    preflight = build_preflight(
        _ready_payload(),
        operator_approval=approval,
    )

    assert preflight["decision"]["preflight_state"] == "write_preflight_not_allowed"
    assert "chunk_count_exceeds_approval" in preflight["decision"]["reasons"]
    assert preflight["write_scope"]["chunk_count"] == 1


def test_write_preflight_report_is_sanitized_and_ignored_artifact_friendly(
    tmp_path: Path,
) -> None:
    build_preflight, write_preflight = _preflight_module()
    preflight = build_preflight(
        _ready_payload(),
        operator_approval=_operator_approval(),
    )

    output_path = write_preflight(tmp_path, preflight)
    output_text = output_path.read_text(encoding="utf-8")
    saved = json.loads(output_text)

    assert output_path.name == "redacted-run-001-preflight.json"
    assert saved["decision"]["preflight_state"] == "write_preflight_ready_for_dry_run"
    assert "/Users/" not in output_text
    assert "secret.pdf" not in output_text
    assert "真实正文" not in output_text


def test_cli_writes_preflight_report_and_prints_sanitized_summary(
    tmp_path: Path,
    capsys,
) -> None:
    cli_main = _cli_main()
    payload_path = tmp_path / "payload.json"
    approval_path = tmp_path / "approval.json"
    payload_path.write_text(json.dumps(_ready_payload()), encoding="utf-8")
    approval_path.write_text(json.dumps(_operator_approval()), encoding="utf-8")
    output_dir = tmp_path / "preflight"

    exit_code = cli_main(
        [
            "--payload-json",
            str(payload_path),
            "--operator-approval-json",
            str(approval_path),
            "--output-dir",
            str(output_dir),
            "--created-at",
            "2026-05-15T13:00:00Z",
        ]
    )

    summary = json.loads(capsys.readouterr().out)
    report_path = output_dir / "redacted-run-001-preflight.json"

    assert exit_code == 0
    assert report_path.exists()
    assert summary["decision"] == "go"
    assert summary["preflight_state"] == "write_preflight_ready_for_dry_run"
    assert summary["preflight_artifact_generated"] is True
    assert summary["writes_authorized"] is False
    assert summary["documents_written"] is False
    assert summary["chunks_written"] is False
    assert summary["agent_answer_integration"] is False
    assert "/Users/" not in json.dumps(summary, ensure_ascii=False)


def _operator_approval() -> dict[str, object]:
    return {
        "approved": True,
        "payload_run_id": "redacted-run-001",
        "approved_project_scope": "SPECIFIC_PROJECTS",
        "max_document_count": 1,
        "max_chunk_count": 20,
        "max_total_text_bucket": "small",
        "reason": "controlled small batch preflight",
        "approved_at": "2026-05-15T12:30:00Z",
        "expires_at": "2099-01-01T00:00:00Z",
    }


def _ready_payload() -> dict[str, object]:
    return {
        "payload_version": "nas_evidence_write_payload.v0",
        "run_id": "redacted-run-001",
        "created_at": "2026-05-15T12:00:00Z",
        "source": {
            "asset_ref": "hash:asset-001",
            "source_view": "FileAssetView",
            "platform_contract_version": "delivery_platform.asset_views.v1.1",
            "eligibility_report_version": "nas_evidence_write_eligibility.v0",
            "eligibility_report_run_id": "redacted-eligibility-001",
            "hash_or_checksum_present": True,
            "cleanup_status": "all_deleted",
        },
        "eligibility": {
            "state": "eligible_for_evidence_write_planning",
            "human_review_decision": "approve_for_payload_dry_run_planning",
            "permission_default": "DENIED",
        },
        "candidate_document": {
            "external_source_type": "platform_asset_catalog",
            "external_asset_ref": "hash:asset-001",
            "sanitized_title": "redacted_asset_document",
            "source_view": "FileAssetView",
            "file_type": "pdf",
            "parser_type": "sanitized_parser_preview",
            "permission_proof_status": "valid",
            "confidentiality_status": "known",
            "lifecycle_status": "active",
            "index_eligibility_status": "eligible_for_preview",
            "document_write_mode": "dry_run_only",
            "raw_text_present": False,
            "true_source_path_present": False,
        },
        "candidate_chunks": [
            {
                "dry_run_chunk_ref": "redacted-run-001-chunk-0001",
                "chunk_write_mode": "dry_run_only",
                "chunk_order": 1,
                "text_length_bucket": "derived_from_manifest",
                "structure_bucket": "sanitized_structure_summary",
                "parser_section_label": "sanitized_section",
                "redacted_citation_anchor": "FileAssetView:hash:asset-001:chunk-0001",
                "file_type": "pdf",
                "raw_text_present": False,
                "scratch_path_present": False,
                "true_filename_present": False,
            }
        ],
        "citation_contract": {
            "cite_db_asset_ref": True,
            "cite_scratch_path": False,
            "source_view_required": True,
            "platform_contract_version_required": True,
            "parser_type_required": True,
            "permission_proof_status_required": True,
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
            "production_rollout": False,
        },
        "dry_run": True,
        "writes_authorized": False,
        "decision": {
            "payload_state": "payload_ready_for_write_dry_run",
            "reasons": ["all_payload_planning_gates_passed"],
        },
    }

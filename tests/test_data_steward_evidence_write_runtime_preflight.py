from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase288_runtime_evidence_write_preflight.py"
)


def _runtime_preflight_module():
    try:
        from app.services.asset_catalog.evidence_write_runtime_preflight import (
            RUNTIME_PREFLIGHT_VERSION,
            build_runtime_evidence_write_preflight_report,
            write_runtime_evidence_write_preflight_report,
        )
    except ModuleNotFoundError as error:  # pragma: no cover - RED phase guard
        pytest.fail(f"runtime evidence write preflight module is missing: {error}")
    return (
        RUNTIME_PREFLIGHT_VERSION,
        build_runtime_evidence_write_preflight_report,
        write_runtime_evidence_write_preflight_report,
    )


def _cli_main():
    assert SCRIPT_PATH.exists(), "phase288 runtime evidence write preflight CLI is missing"
    script_spec = importlib.util.spec_from_file_location(
        "phase288_runtime_evidence_write_preflight",
        SCRIPT_PATH,
    )
    assert script_spec and script_spec.loader
    script_module = importlib.util.module_from_spec(script_spec)
    script_spec.loader.exec_module(script_module)
    return script_module.main


def test_valid_approval_and_safe_refs_are_ready_for_operator_stop(tmp_path: Path) -> None:
    version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)

    report = build_report(
        approval,
        expected_git_commit="3b01b0f",
        created_at="2026-05-15T17:00:00Z",
    )

    assert version == "runtime_evidence_write_preflight.v0"
    assert report["runtime_preflight_version"] == version
    assert report["decision"]["runtime_preflight_state"] == (
        "preflight_ready_for_operator_stop"
    )
    assert report["decision"]["reasons"] == ["all_runtime_preflight_gates_passed"]
    assert report["dry_run"] is True
    assert report["writes_authorized"] is False
    assert report["would_invoke_writer"] is False
    assert report["safety"]["writer_invoked"] is False
    assert report["safety"]["db_writes"] is False
    assert report["approval_summary"]["approval_id"] == "approval-001"
    assert report["write_scope"] == {
        "max_documents": 1,
        "max_document_versions": 1,
        "max_chunks": 20,
        "one_run_boundary": True,
    }
    assert all(item["exists"] is True for item in report["report_refs"])
    assert all(item["appears_sanitized"] is True for item in report["report_refs"])


def test_missing_required_approval_field_pauses(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval.pop("approved_by")

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_pause"
    assert "missing_approval_field_approved_by" in report["decision"]["reasons"]
    assert report["would_invoke_writer"] is False


def test_expired_approval_pauses(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval["expires_at"] = "2026-01-01T00:00:00Z"

    report = build_report(
        approval,
        expected_git_commit="3b01b0f",
        created_at="2026-05-15T17:00:00Z",
    )

    assert report["decision"]["runtime_preflight_state"] == "preflight_pause"
    assert "operator_approval_expired" in report["decision"]["reasons"]


def test_wrong_target_environment_is_no_go(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval["target_environment"] = "production"

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_no_go"
    assert "target_environment_not_test_machine_only" in report["decision"]["reasons"]


def test_scope_over_tiny_limits_is_no_go(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval["max_chunks"] = 21

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_no_go"
    assert "max_chunks_exceeds_20" in report["decision"]["reasons"]


def test_agent_answer_or_index_flag_true_is_no_go(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval["feature_flags_expected"]["PLATFORM_ASSET_INDEX_WRITE_ENABLED"] = True

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_no_go"
    assert (
        "forbidden_feature_flag_true_PLATFORM_ASSET_INDEX_WRITE_ENABLED"
        in report["decision"]["reasons"]
    )


def test_missing_prerequisite_report_ref_pauses(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval["dry_run_ref"] = str(tmp_path / "missing-dry-run.json")

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_pause"
    assert "missing_report_ref_dry_run_ref" in report["decision"]["reasons"]


def test_unsafe_report_marker_or_raw_path_marker_is_no_go(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    Path(approval["payload_plan_ref"]).write_text(
        json.dumps({"sanitized": True, "nas_path": "/Users/example/raw.docx"}),
        encoding="utf-8",
    )

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_no_go"
    assert "unsafe_report_ref_payload_plan_ref" in report["decision"]["reasons"]


def test_missing_idempotency_key_or_write_run_id_is_no_go(tmp_path: Path) -> None:
    _version, build_report, _write_report = _runtime_preflight_module()
    approval = _ready_approval(tmp_path)
    approval["evidence_write_idempotency_key"] = ""

    report = build_report(approval, expected_git_commit="3b01b0f")

    assert report["decision"]["runtime_preflight_state"] == "preflight_no_go"
    assert "idempotency_key_missing" in report["decision"]["reasons"]


def test_cli_writes_sanitized_report_and_summary(tmp_path: Path, capsys) -> None:
    cli_main = _cli_main()
    approval_path = tmp_path / "approval.json"
    output_path = tmp_path / "runtime-preflight.json"
    approval_path.write_text(
        json.dumps(_ready_approval(tmp_path), ensure_ascii=False),
        encoding="utf-8",
    )

    exit_code = cli_main(
        [
            "--approval-json",
            str(approval_path),
            "--output",
            str(output_path),
            "--expected-git-commit",
            "3b01b0f",
            "--created-at",
            "2026-05-15T17:00:00Z",
        ]
    )

    summary_text = capsys.readouterr().out
    summary = json.loads(summary_text)
    report_text = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert output_path.exists()
    assert summary["runtime_preflight_state"] == "preflight_ready_for_operator_stop"
    assert summary["preflight_artifact_generated"] is True
    assert summary["would_invoke_writer"] is False
    assert summary["db_writes"] is False
    assert summary["agent_answer_integration"] is False
    assert "secret" not in summary_text
    assert "真实正文" not in report_text
    assert "/Users/example/raw.docx" not in report_text
    assert "reports_ready" in report_text


def _ready_approval(tmp_path: Path) -> dict[str, object]:
    refs = _safe_report_refs(tmp_path)
    return {
        "approval_version": "hermes_evidence_write_operator_approval.v1",
        "approval_id": "approval-001",
        "approved_by": "operator-a",
        "approved_at": "2026-05-15T16:00:00Z",
        "expires_at": "2099-01-01T00:00:00Z",
        "target_environment": "test_machine_only",
        "target_git_commit": "3b01b0f",
        "source_system": "db_v1_1_catalog",
        "source_asset_ref": "hash:asset-001",
        "project_scope": "SPECIFIC_PROJECTS",
        "permission_proof_ref": refs["permission_proof_ref"],
        "sanitized_manifest_ref": refs["sanitized_manifest_ref"],
        "eligibility_report_ref": refs["eligibility_report_ref"],
        "payload_plan_ref": refs["payload_plan_ref"],
        "preflight_report_ref": refs["preflight_report_ref"],
        "dry_run_ref": refs["dry_run_ref"],
        "rehearsal_ref": refs["rehearsal_ref"],
        "rollback_dry_run_ref": refs["rollback_dry_run_ref"],
        "write_run_id": "runtime-write-run-001",
        "evidence_write_idempotency_key": "runtime-idempotency-001",
        "expected_payload_fingerprint": "payload-fingerprint-001",
        "max_documents": 1,
        "max_document_versions": 1,
        "max_chunks": 20,
        "allowed_write_action": "first_real_hermes_evidence_write_smoke",
        "feature_flags_expected": {
            "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED": True,
            "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED": True,
            "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED": False,
            "PLATFORM_ASSET_INDEX_WRITE_ENABLED": False,
            "PLATFORM_ASSET_API_CLI_RUNTIME_ENABLED": False,
        },
        "writes_authorized": True,
        "operator_notes": "controlled smoke approval without sensitive details",
    }


def _safe_report_refs(tmp_path: Path) -> dict[str, str]:
    names = [
        "permission_proof_ref",
        "sanitized_manifest_ref",
        "eligibility_report_ref",
        "payload_plan_ref",
        "preflight_report_ref",
        "dry_run_ref",
        "rehearsal_ref",
        "rollback_dry_run_ref",
    ]
    refs: dict[str, str] = {}
    for name in names:
        path = tmp_path / f"{name}.json"
        path.write_text(
            json.dumps(
                {
                    "report_version": name,
                    "sanitized": True,
                    "status": "reports_ready",
                    "raw_text_present": False,
                    "true_source_path_present": False,
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        refs[name] = str(path)
    return refs

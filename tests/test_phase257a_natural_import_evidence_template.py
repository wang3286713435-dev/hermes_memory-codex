from __future__ import annotations

import json
import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase257a_natural_import_evidence_template.py"
SPEC = importlib.util.spec_from_file_location("phase257a_natural_import_evidence_template", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

build_evidence_template = MODULE.build_evidence_template
build_review_summary = MODULE.build_review_summary
main = MODULE.main
write_evidence_template = MODULE.write_evidence_template


def test_existing_file_generates_ready_for_authorized_smoke(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")

    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )

    assert payload["dry_run"] is True
    assert payload["real_upload_called"] is False
    assert payload["plain_upload_bypass_used"] is False
    assert payload["source_path_exists"] is True
    assert payload["source_file_size_bytes"] == source.stat().st_size
    assert payload["source_file_type"] == ".docx"
    assert payload["alias"] == "测试文件"
    assert payload["session_id"] == "session-1"
    assert payload["operator"] == "operator-a"
    assert payload["go_pause_no_go"] == "ReadyForAuthorizedSmoke"
    assert payload["missing_required_fields"] == []
    assert "explicit user authorization" in " ".join(payload["required_next_steps"])


def test_missing_file_generates_pause(tmp_path):
    payload = build_evidence_template(
        source_path=tmp_path / "missing.docx",
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )

    assert payload["go_pause_no_go"] == "Pause"
    assert "source_path_exists" in payload["missing_required_fields"]
    assert payload["source_file_size_bytes"] is None


def test_empty_alias_or_session_generates_pause(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")

    missing_alias = build_evidence_template(
        source_path=source,
        alias="",
        session_id="session-1",
        operator="operator-a",
    )
    missing_session = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="",
        operator="operator-a",
    )

    assert missing_alias["go_pause_no_go"] == "Pause"
    assert "alias" in missing_alias["missing_required_fields"]
    assert missing_session["go_pause_no_go"] == "Pause"
    assert "session_id" in missing_session["missing_required_fields"]


def test_output_allowed_under_reports_internal_mvp_runs(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    output = tmp_path / "reports" / "internal_mvp_runs" / "evidence.json"
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )

    write_evidence_template(payload, output=output, reports_root=tmp_path / "reports")

    assert json.loads(output.read_text(encoding="utf-8"))["alias"] == "测试文件"


def test_output_outside_reports_internal_mvp_runs_fails_closed(tmp_path):
    payload = build_evidence_template(
        source_path=tmp_path / "demo.docx",
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )

    with pytest.raises(ValueError, match="reports/internal_mvp_runs"):
        write_evidence_template(payload, output=tmp_path / "outside.json", reports_root=tmp_path / "reports")


def test_payload_does_not_authorize_upload_or_repair(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")

    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )

    assert payload["real_upload_called"] is False
    assert payload["real_file_uploaded"] is False
    assert payload["cleanup_authorized"] is False
    assert payload["repair_authorized"] is False
    assert payload["backfill_authorized"] is False
    assert payload["reindex_authorized"] is False
    assert payload["rollout_authorized"] is False
    assert "document_id" not in payload
    assert "version_id" not in payload


def test_cli_writes_stdout_json_without_uploading(tmp_path, capsys):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")

    exit_code = main(
        [
            "--source-path",
            str(source),
            "--alias",
            "测试文件",
            "--session-id",
            "session-1",
            "--operator",
            "operator-a",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["go_pause_no_go"] == "ReadyForAuthorizedSmoke"
    assert payload["real_upload_called"] is False


def test_review_ready_dry_run_template_allows_operator_authorization(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )

    summary = build_review_summary(payload)

    assert summary["review_status"] == "ready_for_operator_authorization"
    assert summary["go_pause_no_go"] == "ReadyForAuthorizedSmoke"
    assert summary["blocking_reasons"] == []
    assert summary["safe_to_request_real_smoke_authorization"] is True
    assert summary["real_upload_called"] is False


def test_review_missing_required_fields_pauses():
    payload = {
        "dry_run": True,
        "real_upload_called": False,
        "go_pause_no_go": "ReadyForAuthorizedSmoke",
        "source_path_exists": True,
        "alias": "",
        "session_id": "session-1",
        "operator": "operator-a",
        "cleanup_authorized": False,
        "repair_authorized": False,
        "backfill_authorized": False,
        "reindex_authorized": False,
        "rollout_authorized": False,
    }

    summary = build_review_summary(payload)

    assert summary["review_status"] == "pause"
    assert "alias_missing" in summary["blocking_reasons"]
    assert summary["safe_to_request_real_smoke_authorization"] is False


def test_review_dangerous_authorization_is_no_go(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )
    payload["repair_authorized"] = True

    summary = build_review_summary(payload)

    assert summary["review_status"] == "no_go"
    assert "repair_authorized" in summary["blocking_reasons"]
    assert summary["safe_to_request_real_smoke_authorization"] is False


def test_review_real_upload_called_pauses_for_dry_run_review(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )
    payload["real_upload_called"] = True

    summary = build_review_summary(payload)

    assert summary["review_status"] == "pause"
    assert "real_upload_called" in summary["blocking_reasons"]
    assert summary["safe_to_request_real_smoke_authorization"] is False


def test_review_plain_upload_bypass_pauses_for_dry_run_review(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )
    payload["plain_upload_bypass_used"] = True

    summary = build_review_summary(payload)

    assert summary["review_status"] == "pause"
    assert "plain_upload_bypass_used" in summary["blocking_reasons"]
    assert summary["safe_to_request_real_smoke_authorization"] is False


def test_review_real_file_uploaded_pauses_for_dry_run_review(tmp_path):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )
    payload["real_file_uploaded"] = True

    summary = build_review_summary(payload)

    assert summary["review_status"] == "pause"
    assert "real_file_uploaded" in summary["blocking_reasons"]
    assert summary["safe_to_request_real_smoke_authorization"] is False


def test_cli_review_json_outputs_summary(tmp_path, capsys):
    source = tmp_path / "demo.docx"
    source.write_text("metadata-only", encoding="utf-8")
    payload = build_evidence_template(
        source_path=source,
        alias="测试文件",
        session_id="session-1",
        operator="operator-a",
    )
    review_json = tmp_path / "evidence.json"
    review_json.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = main(["--review-json", str(review_json)])

    assert exit_code == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["review_status"] == "ready_for_operator_authorization"
    assert summary["safe_to_request_real_smoke_authorization"] is True

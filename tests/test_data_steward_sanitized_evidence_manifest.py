from __future__ import annotations

import json
import importlib.util
from pathlib import Path

import pytest

from app.services.asset_catalog.evidence_manifest import (
    UnsafeParserPreviewError,
    build_sanitized_evidence_manifest,
    write_sanitized_evidence_manifest,
)

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "phase281a_sanitized_evidence_manifest.py"
)
SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "phase281a_sanitized_evidence_manifest",
    SCRIPT_PATH,
)
assert SCRIPT_SPEC and SCRIPT_SPEC.loader
SCRIPT_MODULE = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(SCRIPT_MODULE)
cli_main = SCRIPT_MODULE.main


def test_manifest_is_ready_for_review_from_sanitized_preview() -> None:
    manifest = build_sanitized_evidence_manifest(
        _sanitized_preview(),
        created_at="2026-05-14T10:00:00Z",
    )

    assert manifest["manifest_version"] == "nas_evidence_manifest.v0"
    assert manifest["run_id"] == "redacted-run-001"
    assert manifest["source"]["asset_ref"] == "hash:asset-001"
    assert manifest["source"]["project_scope_proven"] is True
    assert manifest["parser_preview"]["parser_status"] == "parsed"
    assert manifest["parser_preview"]["text_length_bucket"] == "small"
    assert manifest["safety"]["raw_text_output"] is False
    assert manifest["safety"]["documents_written"] is False
    assert manifest["safety"]["agent_answer_integration"] is False
    assert manifest["cleanup"]["scratch_cleanup_status"] == "all_deleted"
    assert manifest["decision"]["manifest_status"] == "ready_for_review"
    assert manifest["decision"]["next_allowed_phase"] == "review_only"


def test_manifest_marks_no_go_when_write_or_answer_flags_are_true() -> None:
    preview = _sanitized_preview(
        safety={
            "raw_text_output": False,
            "documents_written": True,
            "chunks_written": False,
            "db_writes": False,
            "opensearch_writes": False,
            "qdrant_writes": False,
            "minio_writes": False,
            "agent_answer_integration": True,
        }
    )

    manifest = build_sanitized_evidence_manifest(preview)

    assert manifest["decision"]["manifest_status"] == "no_go"
    assert manifest["decision"]["next_allowed_phase"] == "none"
    assert "documents_written_true" in manifest["decision"]["reasons"]
    assert "agent_answer_integration_true" in manifest["decision"]["reasons"]


def test_manifest_rejects_raw_text_filename_and_paths() -> None:
    preview = _sanitized_preview(raw_text="真实正文", true_filename="secret.pdf")

    with pytest.raises(UnsafeParserPreviewError) as error:
        build_sanitized_evidence_manifest(preview)

    assert "raw_text" in str(error.value)
    assert "true_filename" in str(error.value)


def test_write_manifest_uses_sanitized_filename_and_no_raw_values(tmp_path: Path) -> None:
    manifest = build_sanitized_evidence_manifest(_sanitized_preview())

    output_path = write_sanitized_evidence_manifest(tmp_path, manifest)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    output_text = output_path.read_text(encoding="utf-8")

    assert output_path.name == "redacted-run-001.json"
    assert payload["run_id"] == "redacted-run-001"
    assert "/Users/" not in output_text
    assert "secret.pdf" not in output_text
    assert "真实正文" not in output_text


def test_cli_writes_manifest_and_prints_sanitized_summary(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    preview_path = tmp_path / "preview.json"
    preview_path.write_text(json.dumps(_sanitized_preview()), encoding="utf-8")
    output_dir = tmp_path / "manifests"

    exit_code = cli_main(
        [
            "--input-json",
            str(preview_path),
            "--output-dir",
            str(output_dir),
            "--created-at",
            "2026-05-14T10:00:00Z",
        ]
    )

    summary = json.loads(capsys.readouterr().out)
    manifest_path = output_dir / "redacted-run-001.json"

    assert exit_code == 0
    assert manifest_path.exists()
    assert summary["decision"] == "go"
    assert summary["manifest_status"] == "ready_for_review"
    assert summary["manifest_artifact_generated"] is True
    assert summary["documents_written"] is False
    assert summary["agent_answer_integration"] is False
    assert "/Users/" not in json.dumps(summary, ensure_ascii=False)


def _sanitized_preview(**overrides: object) -> dict[str, object]:
    preview: dict[str, object] = {
        "run_id": "redacted-run-001",
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
            "warnings": ["pdf_structure_repaired"],
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
    }
    preview.update(overrides)
    return preview

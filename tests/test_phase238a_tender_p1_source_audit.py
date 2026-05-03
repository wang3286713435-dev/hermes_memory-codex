from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase238a_tender_p1_source_audit.py"
SPEC = importlib.util.spec_from_file_location("phase238a_tender_p1_source_audit", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def _chunk(chunk_id: str, text: str, **overrides):
    return audit.ChunkView.from_mapping(
        {
            "chunk_id": chunk_id,
            "text": text,
            "chunk_index": overrides.get("chunk_index", 1),
            "section_path": overrides.get("section_path", ["投标人须知前附表"]),
            "page_start": overrides.get("page_start", 1),
        }
    )


def _field_result(field: str, chunks):
    return audit.audit_chunks(chunks, [field])[0]


def test_concrete_price_amount_detection():
    result = _field_result(
        "price_ceiling",
        [_chunk("price", "投标人须知前附表\n最高投标限价：人民币200万元。投标报价不得超过招标控制价。")],
    )

    assert result["status"] == "concrete_source_found"
    assert result["candidate_chunk_ids"] == ["price"]
    assert "最高投标限价" in result["matched_terms"]


def test_anchor_only_price_detection():
    result = _field_result("price_ceiling", [_chunk("price-anchor", "最高投标限价详见附件，投标报价按招标控制价执行。")])

    assert result["status"] == "anchor_only"
    assert result["candidate_chunk_ids"] == ["price-anchor"]


def test_qualification_grade_and_category_concrete_detection():
    result = _field_result(
        "qualification_grade_category",
        [_chunk("qualification", "资格审查\n投标人资格要求：具备建筑工程施工总承包一级及以上资质。")],
    )

    assert result["status"] == "concrete_source_found"
    assert result["candidate_chunk_ids"] == ["qualification"]


def test_e_certificate_format_is_not_project_manager_level():
    result = _field_result(
        "project_manager_level",
        [_chunk("ecert", "一级注册建造师电子证书格式要求：签名图像应完整。")],
    )

    assert result["status"] == "anchor_only"
    assert result["candidate_chunks"][0]["diagnostic"] == "e_certificate_format_not_project_manager_level"


def test_explicit_project_manager_level_is_concrete():
    result = _field_result(
        "project_manager_level",
        [_chunk("pm", "项目经理须具备一级注册建造师资格和安全生产考核B证。")],
    )

    assert result["status"] == "concrete_source_found"


def test_performance_and_personnel_ambiguous_status():
    performance = _field_result("performance_requirement", [_chunk("perf", "投标人须提供类似工程业绩证明材料。")])
    personnel = _field_result("personnel_requirement", [_chunk("personnel", "项目管理机构人员配备详见投标文件格式。")])

    assert performance["status"] == "ambiguous"
    assert personnel["status"] == "ambiguous"


def test_not_found_status():
    result = _field_result("price_ceiling", [_chunk("other", "本章节仅描述施工组织设计要求。")])

    assert result["status"] == "not_found"
    assert result["candidate_chunk_ids"] == []


def test_skip_live_marks_fields_skipped(capsys):
    exit_code = audit.main(
        [
            "--document-id",
            "doc",
            "--version-id",
            "ver",
            "--skip-live",
            "--dry-run-preview",
            "--field",
            "price_ceiling",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["field_audits"][0]["status"] == "skipped_live_unavailable"
    assert payload["dry_run"] is True
    assert payload["writes_db"] is False
    assert payload["mutates_index"] is False
    assert payload["destructive_actions"] == []
    assert payload["output_file"] is None


def test_dry_run_preview_does_not_write_file(tmp_path, capsys):
    output_dir = tmp_path / "reports"

    exit_code = audit.main(
        [
            "--document-id",
            "doc",
            "--version-id",
            "ver",
            "--skip-live",
            "--dry-run-preview",
            "--output-dir",
            str(output_dir),
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["output_file"] is None
    assert not output_dir.exists()


def test_reports_tender_p1_audit_ignore_policy_exists():
    ignore_path = Path(__file__).resolve().parents[1] / "reports" / "tender_p1_audit" / ".gitignore"
    content = ignore_path.read_text(encoding="utf-8")

    assert "*.json" in content
    assert "*.md" in content
    assert "!README.md" in content

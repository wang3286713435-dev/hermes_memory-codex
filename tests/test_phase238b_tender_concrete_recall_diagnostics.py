from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "phase238b_tender_concrete_recall_diagnostics.py"
SPEC = importlib.util.spec_from_file_location("phase238b_tender_concrete_recall_diagnostics", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
diagnostics = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = diagnostics
SPEC.loader.exec_module(diagnostics)


def test_price_ceiling_remains_missing_evidence_policy():
    result = diagnostics.fixed_policy_diagnostic("price_ceiling")

    assert result["policy"] == "preserve_missing_evidence"
    assert result["status"] == "field_should_remain_missing_evidence"
    assert result["candidate_chunk_ids"] == []


def test_project_manager_level_requires_human_review_policy():
    result = diagnostics.fixed_policy_diagnostic("project_manager_level")

    assert result["policy"] == "human_review_required"
    assert result["status"] == "field_requires_human_review"
    assert "human review" in result["recommended_next_action"].lower()


def test_candidate_chunks_in_top_k_status():
    result = diagnostics.diagnose_candidate_visibility(
        field="qualification_grade_category",
        candidate_chunk_ids=["c1", "c2"],
        retrieved_chunk_ids=["x", "c1", "c2", "y"],
        retrieval_query="资质等级要求是什么？",
        top_k=5,
    )

    assert result["status"] == "candidate_in_top_k"
    assert [hit["chunk_id"] for hit in result["candidate_hits"]] == ["c1", "c2"]
    assert all(hit["in_top_k"] for hit in result["candidate_hits"])


def test_candidate_present_but_low_rank_status():
    result = diagnostics.diagnose_candidate_visibility(
        field="performance_requirement",
        candidate_chunk_ids=["perf"],
        retrieved_chunk_ids=["a", "b", "c", "perf"],
        retrieval_query="类似业绩要求是什么？",
        top_k=3,
    )

    assert result["status"] == "candidate_present_but_low_rank"
    assert result["candidate_hits"] == [{"chunk_id": "perf", "rank": 4, "in_top_k": False}]


def test_candidate_absent_from_retrieval_status():
    result = diagnostics.diagnose_candidate_visibility(
        field="personnel_requirement",
        candidate_chunk_ids=["personnel"],
        retrieved_chunk_ids=["a", "b", "c"],
        retrieval_query="人员要求是什么？",
        top_k=10,
    )

    assert result["status"] == "candidate_absent_from_retrieval"
    assert result["candidate_hits"] == []


def test_skip_live_marks_concrete_fields_skipped(capsys):
    exit_code = diagnostics.main(
        [
            "--document-id",
            "doc",
            "--version-id",
            "ver",
            "--field",
            "qualification_grade_category",
            "--skip-live",
            "--dry-run-preview",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["field_diagnostics"][0]["status"] == "skipped_live_unavailable"
    assert payload["dry_run"] is True
    assert payload["read_only"] is True
    assert payload["writes_db"] is False
    assert payload["mutates_index"] is False
    assert payload["repairs_issue"] is False
    assert payload["destructive_actions"] == []
    assert payload["output_file"] is None


def test_summary_keeps_safety_flags_constant():
    result = diagnostics.build_summary(
        document_id="doc",
        version_id="ver",
        fields=["price_ceiling", "qualification_grade_category"],
        concrete_diagnostics=[
            diagnostics.diagnose_candidate_visibility(
                field="qualification_grade_category",
                candidate_chunk_ids=["candidate"],
                retrieved_chunk_ids=["candidate"],
                retrieval_query="资质等级要求是什么？",
                top_k=10,
            )
        ],
    )

    assert result["dry_run"] is True
    assert result["read_only"] is True
    assert result["destructive_actions"] == []
    assert result["writes_db"] is False
    assert result["mutates_index"] is False
    assert result["repairs_issue"] is False
    assert result["rollout_approved"] is False


def test_dry_run_preview_does_not_write_file(tmp_path, capsys):
    output_dir = tmp_path / "reports"

    exit_code = diagnostics.main(
        [
            "--document-id",
            "doc",
            "--version-id",
            "ver",
            "--field",
            "all",
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


def test_reports_tender_recall_diagnostics_ignore_policy_exists():
    ignore_path = Path(__file__).resolve().parents[1] / "reports" / "tender_recall_diagnostics" / ".gitignore"
    content = ignore_path.read_text(encoding="utf-8")

    assert "*.json" in content
    assert "*.md" in content
    assert "!README.md" in content

from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.phase245c_health_check_dry_run import (  # noqa: E402
    build_summary,
    env_checks,
    latest_json_ignore_check,
    make_check,
    mount_path_check,
    parse_check_url,
    url_check,
)


def test_summary_keeps_dry_run_invariants() -> None:
    summary = build_summary(
        [
            make_check(
                check_id="sample",
                category="unit",
                status="pass",
                message="ok",
            )
        ]
    )

    assert summary["dry_run"] is True
    assert summary["writes_db"] is False
    assert summary["repairs"] is False
    assert summary["rollout_approved"] is False
    assert summary["status"] == "pass"


def test_env_checks_report_key_names_without_secret_values(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "DATABASE_URL=postgresql://user:super-secret-password@localhost/db",
                "OPENSEARCH_URL=http://localhost:9200",
                "QDRANT_URL=http://localhost:6333",
                "QDRANT_COLLECTION=hermes_chunks",
            ]
        ),
        encoding="utf-8",
    )

    checks = env_checks(env_file=env_file, expected_qdrant_collection="hermes_chunks")
    payload = json.dumps(build_summary(checks), ensure_ascii=False)

    assert "DATABASE_URL" not in payload
    assert "super-secret-password" not in payload
    assert "Required env key names are present" in payload
    assert "QDRANT_COLLECTION matches expected value" in payload


def test_missing_env_file_warns_without_crashing(tmp_path: Path) -> None:
    checks = env_checks(
        env_file=tmp_path / "missing.env",
        expected_qdrant_collection="hermes_chunks",
    )
    summary = build_summary(checks)

    assert summary["status"] == "warn"
    assert summary["warnings"] == 1
    assert checks[0]["id"] == "env_file"
    assert checks[0]["human_action_required"] is True


def test_qdrant_collection_mismatch_requires_stop(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "DATABASE_URL=postgresql://localhost/db",
                "OPENSEARCH_URL=http://localhost:9200",
                "QDRANT_URL=http://localhost:6333",
                "QDRANT_COLLECTION=hermes_gate_chunks",
            ]
        ),
        encoding="utf-8",
    )

    summary = build_summary(
        env_checks(env_file=env_file, expected_qdrant_collection="hermes_chunks")
    )

    assert summary["status"] == "fail"
    assert summary["failures"] == 1
    assert summary["stop_required"] is True
    assert "qdrant_collection" in summary["human_action_required"]


def test_mount_path_missing_warns(tmp_path: Path) -> None:
    check = mount_path_check(tmp_path / "not-mounted")

    assert check["status"] == "warn"
    assert check["human_action_required"] is True


def test_check_url_success_uses_mocked_head() -> None:
    requests: list[urllib.request.Request] = []

    class Response:
        status = 200

    def fake_urlopen(request: urllib.request.Request, *, timeout: float) -> Response:
        requests.append(request)
        assert timeout == 2.0
        return Response()

    check = url_check("api=http://127.0.0.1:8000/health", urlopen=fake_urlopen)

    assert check["status"] == "pass"
    assert check["message"] == "api is reachable with HEAD."
    assert requests[0].get_method() == "HEAD"


def test_check_url_head_405_falls_back_to_mocked_get() -> None:
    requests: list[str] = []

    class Response:
        status = 200

    def fake_urlopen(request: urllib.request.Request, *, timeout: float) -> Response:
        requests.append(request.get_method())
        if request.get_method() == "HEAD":
            raise urllib.error.HTTPError(
                request.full_url,
                405,
                "method not allowed",
                hdrs=None,
                fp=None,
            )
        return Response()

    check = url_check("api=http://127.0.0.1:8000/health", urlopen=fake_urlopen)

    assert check["status"] == "pass"
    assert check["message"] == "api is reachable with GET."
    assert requests == ["HEAD", "GET"]


def test_check_url_rejects_non_http_urls() -> None:
    try:
        parse_check_url("local=file:///tmp/report.json")
    except ValueError as exc:
        assert "http:// or https://" in str(exc)
    else:  # pragma: no cover - assertion clarity
        raise AssertionError("Expected non-http URL to be rejected")


def test_latest_json_ignore_check_can_use_fake_runner(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def fake_runner(
        args: list[str],
        *,
        cwd: Path,
        check: bool,
        capture_output: bool,
        text: bool,
    ) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        return subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr="")

    check = latest_json_ignore_check(cwd=tmp_path, runner=fake_runner)

    assert check["status"] == "pass"
    assert calls == [["git", "check-ignore", "-q", "reports/agent_runs/latest.json"]]

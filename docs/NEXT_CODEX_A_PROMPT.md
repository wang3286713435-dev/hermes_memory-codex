# NEXT_CODEX_A_PROMPT

## Phase 2.91 Runtime Evidence Writer Smoke Gate Baseline

Codex B review passed. Create a selective Git baseline for Phase 2.91 Runtime Evidence Writer Smoke Gate and the newly adopted Data Steward risk boundary docs.

Do not enter real writer smoke, Phase 2.92, Agent answer integration, Data Steward runtime expansion, or production rollout.

Previous baseline:

- commit: `3ee37e3`
- tag: `phase-2.90-test-machine-preflight-readiness-baseline`
- pushed: true

## Review Summary

Codex B reviewed:

1. `app/services/asset_catalog/evidence_write_runtime_smoke.py`
2. `scripts/phase291_runtime_evidence_write_smoke.py`
3. `tests/test_data_steward_evidence_write_runtime_smoke.py`
4. `docs/PHASE291_RUNTIME_EVIDENCE_WRITE_SMOKE_GATE.md`
5. `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
6. `docs/DB_TEAM_HERMES_FRONTEND_GATEWAY_INTEGRATION_V3.md`

Review result:

1. Phase 2.91 default path is gate-only and does not invoke writer.
2. CLI `--execute-writer` has no DB session and pauses safely.
3. `EvidenceOnlyWriter.write()` is reachable only via injected test-local SQLAlchemy session in tests.
4. Reports stay sanitized and exclude raw file content, true NAS path, raw row, secret, absolute scratch path, and business values.
5. Data Steward risk boundary is documentation-only and reinforces Hermes naming plus catalog-only safety.

## Required Validation

Run:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_evidence_write_runtime_smoke.py -q
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile app/services/asset_catalog/evidence_write_runtime_smoke.py scripts/phase291_runtime_evidence_write_smoke.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_data_steward_evidence_writer.py tests/test_data_steward_evidence_write_runtime_preflight.py tests/test_data_steward_evidence_write_runtime_smoke.py -q
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git check-ignore reports/evidence_write_runtime_smoke/test.json
git status --short
```

Expected:

1. target Phase 2.91 tests pass: `12 passed`
2. py_compile passes
3. writer + preflight + smoke regression passes: `29 passed`
4. diff check passes
5. latest JSON parses
6. ignored report paths are ignored

## Allowed Files For Baseline

Stage only:

1. `app/services/asset_catalog/evidence_write_runtime_smoke.py`
2. `scripts/phase291_runtime_evidence_write_smoke.py`
3. `tests/test_data_steward_evidence_write_runtime_smoke.py`
4. `docs/PHASE291_RUNTIME_EVIDENCE_WRITE_SMOKE_GATE.md`
5. `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`
6. `docs/DB_TEAM_HERMES_FRONTEND_GATEWAY_INTEGRATION_V3.md`
7. `docs/NEXT_CODEX_A_PROMPT.md`
8. `docs/ACTIVE_PHASE.md`
9. `docs/PHASE_BACKLOG.md`
10. `docs/HANDOFF_LOG.md`
11. `docs/TODO.md`
12. `docs/DEV_LOG.md`

Do not stage:

1. ignored `reports/agent_runs/latest.json`
2. ignored evidence write runtime smoke reports
3. any `.env`, secret, local approval JSON, DB output, NAS output, raw sample, or unrelated file

If any non-allowed tracked or untracked file appears, stop and report.

Before committing, run:

```bash
git diff --cached --check
git diff --cached --name-only
```

The cached file list must match the allowed baseline files only.

## Commit / Tag / Push

Commit message:

```text
chore: add phase 2.91 runtime writer smoke gate
```

Tag:

```text
phase-2.91-runtime-evidence-writer-smoke-gate-baseline
```

Push `origin/main` and the tag.

## Hard Boundaries

Still forbidden:

1. running the smoke against a real developer DB or Mac mini DB
2. calling `EvidenceOnlyWriter.write()` outside tests / injected temp DB session
3. enabling real-write feature flags in `.env`
4. executing parser
5. performing scratch copy
6. reading raw file content
7. scanning NAS
8. writing OpenSearch / Qdrant / MinIO
9. writing platform DB
10. integrating Agent answer
11. Agent DB / NAS CRUD
12. repair / cleanup / backfill / reindex / delete / migration
13. production rollout
14. entering Phase 2.92 automatically

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation writer / DB / parser / scratch / NAS / index / object-store / Agent answer actions remain blocked
7. final `git status --short`

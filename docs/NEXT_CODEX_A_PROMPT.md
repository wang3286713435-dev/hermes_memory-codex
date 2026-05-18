# NEXT_CODEX_A_PROMPT

## Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack Baseline

Codex B review passed. Create a selective Git baseline for Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack.

Do not run frontend / Gateway smoke. Do not enter Phase 2.94b automatically.

Previous baseline:

- commit: `b41bf9b`
- tag: `phase-2.94-frontend-gateway-smoke-plan-baseline`
- pushed: true

## Review Summary

Codex B reviewed:

```text
docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md
docs/PHASE294_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PLAN.md
docs/DB_TEAM_HERMES_FRONTEND_GATEWAY_INTEGRATION_V3.md
docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md
```

Review result:

1. The handoff prompt remains read-only, sanitized, and fail-closed.
2. It clearly requires separate operator authorization before any runtime smoke.
3. Endpoint matrix covers capabilities, health, chat, catalog search, compatibility route, permission-denied, and catalog-only DWG / RVT / BIM content question.
4. Forbidden-field scan covers storage path / URI variants, NAS URI, raw row, SQL, token, secret, bearer, raw content, true NAS path, and executable write / repair / ingestion actions.
5. Permission-denied behavior is fail-closed.
6. Catalog-only content questions must return Missing Evidence / `asset_catalog_only`.
7. Go / Pause / No-Go criteria do not authorize runtime writes, Agent DB CRUD, NAS scan, parser, writer, index/object-store writes, Agent answer integration, or rollout.

## Required Validation

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

Expected:

1. `git diff --check` passes.
2. latest JSON parses.
3. `reports/agent_runs/latest.json` is ignored.
4. `git status --short` contains only Phase 2.94a docs / handoff files.

No pytest is required because no code changed.

## Allowed Files For Baseline

Stage only:

1. `docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage:

1. ignored `reports/agent_runs/latest.json`
2. any DB output, NAS output, platform Gateway output, approval JSON, `.env`, secret, raw sample, screenshot, or unrelated file
3. code, tests, scripts, migrations, parser files, Gateway implementation files, frontend files, or backend platform files

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
docs: add phase 2.94a gateway smoke handoff
```

Tag:

```text
phase-2.94a-gateway-smoke-handoff-baseline
```

Push `origin/main` and the tag.

## Hard Boundaries

Still forbidden:

1. running frontend / Gateway smoke
2. implementing Gateway code in this repository
3. connecting to real DB / platform API / Hermes API
4. Agent DB CRUD
5. Agent-generated SQL
6. NAS scan
7. parser invocation
8. scratch copy
9. writer smoke against real DB
10. writing `documents`, `document_versions`, `chunks`, `citations`
11. writing OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory
12. reading DWG / RVT / NWD / IFC content
13. exposing true `storage_path`, raw row, NAS path, raw content, secret, token, bearer, or credential material
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout
16. entering Phase 2.94b automatically

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation that Gateway smoke, DB/NAS access, writer, parser, index/object-store writes, Agent answer integration, and rollout remain blocked
7. final `git status --short`

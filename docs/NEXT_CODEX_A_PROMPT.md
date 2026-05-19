# NEXT_CODEX_A_PROMPT

## Phase 2.97 Frontend Gateway Read-only Trial Runbook Baseline

You are Codex A. Execute only this bounded Git baseline task.

Do not run frontend / Gateway smoke. Do not connect to DB / NAS / platform API / Hermes API. Do not enter Phase 2.98 automatically.

## Codex B Review Result

Codex B review passed for Phase 2.97.

Confirmed:

1. `docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md` correctly defines a limited internal frontend trial only.
2. It clearly states this is not production rollout and not a smoke execution report.
3. It includes allowed users / roles, environment labels, reviewed refs, auth path, allowed endpoints, allowed query types, response checks, forbidden-field scan, side-effect checklist, operator checklist, per-query recording template, Go / Pause / No-Go, feedback capture, escalation rules, and final summary template.
4. It keeps `project_scope` server-side and does not trust frontend-provided scope.
5. It requires Missing Evidence / `asset_catalog_only` for content-level DWG / RVT / BIM questions.
6. It treats forbidden-field leak, denied-request data exposure, catalog metadata as content evidence, and any write side effect as No-Go.
7. It does not authorize production rollout, Agent DB CRUD, Agent-generated SQL, NAS scan/copy, parser/writer/index writes, DWG/RVT content understanding, raw `storage_path` exposure, repair, migration, or rollout.

## Baseline Scope

Stage only:

1. `docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored local state:

1. `reports/agent_runs/latest.json`

Do not stage any other file.

## Validation

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
git diff --cached --check
git diff --cached --name-only
```

Expected:

1. `git diff --check` passes.
2. latest JSON parses.
3. `reports/agent_runs/latest.json` is ignored.
4. Before staging, `git status --short` shows only the Phase 2.97 docs / handoff files.
5. After staging, `git diff --cached --name-only` includes only the whitelist files above.
6. After commit, final `git status --short` is clean.

## Git Baseline

Commit message:

```text
docs: add frontend gateway readonly trial runbook
```

Tag:

```text
phase-2.97-frontend-gateway-readonly-trial-runbook-baseline
```

Push:

1. `origin/main`
2. tag `phase-2.97-frontend-gateway-readonly-trial-runbook-baseline`

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
16. entering Phase 2.98 automatically

## Completion Report

Report:

1. changed files staged / committed
2. validation command results
3. commit hash
4. tag
5. push result
6. final `git status --short`
7. confirmation that `reports/agent_runs/latest.json` was not staged
8. confirmation that Phase 2.98 was not started

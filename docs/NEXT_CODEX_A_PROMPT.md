# NEXT_CODEX_A_PROMPT

## Phase 2.96 Gateway Controlled Smoke Result Review Baseline

You are Codex A. Execute only this bounded Git baseline task.

Do not run frontend / Gateway smoke. Do not connect to DB / NAS / platform API / Hermes API. Do not enter Phase 2.97 automatically.

## Codex B Review Result

Codex B review passed for Phase 2.96.

Confirmed:

1. `docs/PHASE296_GATEWAY_CONTROLLED_SMOKE_RESULT_REVIEW.md` correctly accepts the latest Gateway controlled smoke result as `Go` for read-only controlled smoke only.
2. The reviewed smoke used normal platform login, project switch, and project-scoped bearer token.
3. Capabilities, health, chat, catalog search, compatibility route, permission-denied, and catalog-only content question passed.
4. Forbidden-field scan found no true secret / token / password / bearer / credential value, NAS path, raw row, SQL, storage path, or raw file content leak.
5. Side-effect flags are all no: DB write, NAS scan/copy, parser, writer, OpenSearch/Qdrant/MinIO write, rollout.
6. Permission-denied fail-closed and catalog-only Missing Evidence / `asset_catalog_only` are the key passed product gates.
7. This `Go` does not authorize production rollout, Agent DB CRUD, Agent-generated SQL, NAS scan/copy, parser/writer/index writes, DWG/RVT content understanding, true `storage_path` exposure, repair, migration, or rollout.

## Baseline Scope

Stage only:

1. `docs/PHASE296_GATEWAY_CONTROLLED_SMOKE_RESULT_REVIEW.md`
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
```

Expected:

1. `git diff --check` passes.
2. latest JSON parses.
3. `reports/agent_runs/latest.json` is ignored.
4. `git status --short` shows only the Phase 2.96 docs / handoff files before staging.
5. After commit, final `git status --short` is clean.

## Git Baseline

Commit message:

```text
docs: review gateway controlled smoke result
```

Tag:

```text
phase-2.96-gateway-controlled-smoke-result-review-baseline
```

Push:

1. `origin/main`
2. tag `phase-2.96-gateway-controlled-smoke-result-review-baseline`

## Hard Boundaries

Still forbidden:

1. running frontend / Gateway smoke again
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
16. entering Phase 2.97 automatically

## Completion Report

Report:

1. changed files staged / committed
2. validation command results
3. commit hash
4. tag
5. push result
6. final `git status --short`
7. confirmation that `reports/agent_runs/latest.json` was not staged
8. confirmation that Phase 2.97 was not started

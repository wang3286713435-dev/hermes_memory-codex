# NEXT_CODEX_A_PROMPT

## Phase 2.95 Shared Contract Alignment Baseline

Codex B review passed. Create a selective Git baseline for Phase 2.95 Shared Contract Alignment.

Do not enter Phase 2.96 automatically. Do not run frontend / Gateway smoke.

Previous baseline:

- commit: `712cd83`
- tag: `phase-2.94a-gateway-smoke-handoff-baseline`
- pushed: true

## Review Summary

Codex B reviewed:

```text
docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md
docs/PHASE_BACKLOG.md
docs/TODO.md
docs/DEV_LOG.md
```

Review result:

1. Shared files read list is complete for the required Phase 2.95 scope.
2. Hermes-owned / reviewed shared files match `ops/document_ownership.md`.
3. `asset_catalog_search` boundary is read-only / fail-closed / catalog-only.
4. Missing Evidence policy is aligned.
5. Memory / `related_file_ids` boundary is safe.
6. Gateway permission and path redaction boundary is aligned.
7. Official name is Hermes; Jarvis is legacy / not official.
8. No required shared contract mismatch was found.

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
4. `git status --short` contains only Phase 2.95 docs / handoff files.

No pytest is required because no code changed.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage:

1. ignored `reports/agent_runs/latest.json`
2. any shared-folder file under `DigitalDeliveryProject`
3. any DB output, NAS output, platform Gateway output, approval JSON, `.env`, secret, raw sample, screenshot, or unrelated file
4. code, tests, scripts, migrations, parser files, Gateway implementation files, frontend files, or backend platform files

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
docs: align shared digital delivery contracts
```

Tag:

```text
phase-2.95-shared-contract-alignment-baseline
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
16. entering Phase 2.96 automatically

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation no shared-folder files were staged
7. confirmation that runtime smoke, DB/NAS access, writer, parser, index/object-store writes, Agent answer integration, and rollout remain blocked
8. final `git status --short`

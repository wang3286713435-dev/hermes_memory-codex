# NEXT_CODEX_A_PROMPT

## Phase 2.87a Exact Write Target Discovery Baseline

Phase 2.87a docs-only / read-only discovery has been completed.
Codex B review has passed.

The discovery document is:

1. `docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md`

## Goal

Baseline the Phase 2.87a discovery document and handoff docs.

This prompt does not authorize Phase 2.87b.

Do not implement a writer.
Do not execute a real write.
Do not run parser / copy / DB / index / object-store / Agent answer smoke.

## Review Result

Codex B verified:

1. Candidate DB evidence targets are identified: `documents`, `document_versions`, `chunks`, `citations`, optional `ingestion_jobs`.
2. Existing `DocumentIngestionService.ingest_uploaded_file()` is marked No-Go for direct reuse because it invokes file bytes, parser/chunker, OpenSearch, and Qdrant side effects.
3. Future Phase 2.87b needs a dedicated evidence-only writer service.
4. Future Phase 2.87b needs explicit idempotency metadata location.
5. Future Phase 2.87b needs run-scoped rollback / invalidation dry-run before runtime smoke.
6. Direct real write remains `Pause`.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage ignored `reports/agent_runs/latest.json`.

If any other tracked or untracked file is dirty, stop and report.

## Validation

Run before baseline:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

## Commit / Tag

Commit message:

```text
docs: add phase 2.87a write target discovery
```

Tag:

```text
phase-2.87a-write-target-discovery-baseline
```

Push `origin/main` and the tag after commit.

## Hard Boundaries

Forbidden:

1. real evidence write
2. writer implementation
3. parser execution
4. file copy
5. raw file content read
6. NAS scan
7. platform DB write
8. Hermes DB write
9. `documents` / `chunks` / `document_versions` write
10. audit table write
11. OpenSearch / Qdrant / MinIO write
12. Agent answer integration
13. Agent DB / NAS CRUD
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout
16. entering Phase 2.87b without a separate explicit prompt and operator approval planning

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation that Phase 2.87a remains docs-only / read-only discovery
7. confirmation that Phase 2.87b remains blocked pending separate authorization
8. confirmation that no real write / parser / copy / DB / index / object-store / Agent answer action occurred

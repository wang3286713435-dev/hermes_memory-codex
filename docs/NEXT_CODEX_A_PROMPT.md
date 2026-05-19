# NEXT_CODEX_A_PROMPT

## Phase 2.98 Digital Delivery Standard Agent Boundary Review Baseline

You are Codex A. Execute only this bounded Git baseline task.

Codex B review result: passed.

Do not modify runtime code. Do not modify shared standard files. Do not connect to DB / NAS / platform API / Hermes API. Do not run frontend / Gateway smoke. Do not enter Phase 2.99.

## Background

Phase 2.98 reviewed the shared Digital Delivery Standard v0.1 as a Hermes Agent answer-boundary source.

Previous baseline:

1. commit: `05e7275`
2. tag: `phase-2.97-frontend-gateway-readonly-trial-runbook-baseline`
3. pushed: true

Codex B reviewed:

1. `docs/PHASE298_STANDARD_AGENT_BOUNDARY_REVIEW.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. ignored `reports/agent_runs/latest.json`

## Baseline Confirmation Checklist

Before staging, confirm:

1. `docs/PHASE298_STANDARD_AGENT_BOUNDARY_REVIEW.md` records the shared standard files reviewed with absolute shared-folder paths.
2. Standard v0.1 is framed as a catalog-only Hermes Agent answer-boundary source, not runtime capability proof.
3. Rule matrix count is recorded as `R001-R043`.
4. `R001-R021` and `R041` are restricted catalog-level answer candidates.
5. `R022-R026` and `R042-R043` are backlog / Missing Evidence leaning.
6. `R027-R040` remain Missing Evidence / future-only.
7. DWG questions require `dwg_parse_evidence`.
8. RVT questions require `rvt_parse_evidence`.
9. BIM component questions require `component_evidence` or `manual_evidence`.
10. Permission/path/conflict safety is recorded.
11. `Hermes / Jarvis` naming overclaim risk is recorded.
12. Standardized answer templates are present.
13. Phase 2.98 did not modify code, shared docs, DB, NAS, platform API, Hermes API, Gateway behavior, parser, writer, index, repair, or rollout.

## Stage Only

Stage only:

1. `docs/PHASE298_STANDARD_AGENT_BOUNDARY_REVIEW.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage:

1. `reports/agent_runs/latest.json`
2. any real reports JSON
3. any runtime code
4. any shared standard files

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

No pytest is required because Phase 2.98 is docs-only.

## Commit / Tag / Push

Commit message:

```text
docs: review digital delivery standard agent boundary
```

Tag:

```text
phase-2.98-standard-agent-boundary-review-baseline
```

Push:

1. `origin/main`
2. `phase-2.98-standard-agent-boundary-review-baseline`

## Completion Report

Report:

1. staged / committed files
2. validation results
3. commit hash
4. tag
5. push result
6. final `git status --short`
7. confirmation that `reports/agent_runs/latest.json` remains ignored and unstaged
8. confirmation that Phase 2.99 was not entered

## Hard Boundaries

Still forbidden:

1. modifying Hermes runtime code
2. modifying shared docs directly unless separately authorized
3. connecting to real DB / platform API / Hermes API
4. running frontend / Gateway smoke
5. Agent DB CRUD
6. Agent-generated SQL
7. NAS scan/copy
8. parser invocation
9. scratch copy
10. writer smoke against real DB
11. writing `documents`, `document_versions`, `chunks`, `citations`
12. writing OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory
13. reading DWG / RVT / NWD / IFC content
14. exposing true `storage_path`, raw row, NAS path, raw content, secret, token, bearer, or credential material
15. repair / cleanup / backfill / reindex / delete / migration
16. production rollout

## Stop Condition

Stop after selective baseline.

Do not enter Phase 2.99 automatically.

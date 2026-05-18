# NEXT_CODEX_A_PROMPT

## Phase 2.93 Read-only Gateway Implementation Review Baseline

Codex B review passed. Create a selective Git baseline for Phase 2.93 Read-only Gateway Implementation Review.

Do not enter Phase 2.94 automatically. Do not run platform Gateway smoke.

Previous baseline:

- commit: `36de5a7`
- tag: `phase-2.92-readonly-gateway-acceptance-plan-baseline`
- pushed: true

## Review Summary

Codex B reviewed:

```text
docs/PHASE293_READONLY_GATEWAY_IMPLEMENTATION_REVIEW.md
```

Review result:

1. The database team's read-only Gateway implementation report satisfies Phase 2.92 P0 gates at report level.
2. Decision is `go` for `read_only_gateway_review_passed`.
3. This is not production readiness.
4. This does not authorize Agent DB CRUD, Agent-generated SQL, NAS scan, content ingestion, writer/parser/index writes, Agent answer integration, or rollout.
5. P1 follow-up remains for sanitized response schema samples, trace identifiers, safe catalog identifiers, and permission-denied copy.
6. Next candidate is Phase 2.94 frontend controlled smoke planning, but this baseline must stop before 2.94.

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
4. `git status --short` contains only Phase 2.93 docs / handoff files.

No pytest is required because no code changed.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE293_READONLY_GATEWAY_IMPLEMENTATION_REVIEW.md`
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
docs: review phase 2.93 readonly gateway implementation
```

Tag:

```text
phase-2.93-readonly-gateway-implementation-review-baseline
```

Push `origin/main` and the tag.

## Hard Boundaries

Still forbidden:

1. implementing Gateway code in this repository
2. running platform Gateway smoke
3. connecting to real DB
4. Agent DB CRUD
5. Agent-generated SQL
6. NAS scan
7. parser invocation
8. scratch copy
9. writer smoke against real DB
10. writing `documents`, `document_versions`, `chunks`, `citations`
11. writing OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory
12. reading DWG / RVT / NWD / IFC content
13. exposing true `storage_path`, raw row, NAS path, raw content, secret, or credential material
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout
16. entering Phase 2.94 automatically

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation that Gateway implementation, DB/NAS access, writer, parser, index/object-store writes, Agent answer integration, and rollout remain blocked
7. final `git status --short`

# NEXT_CODEX_A_PROMPT

## Phase 2.92 Read-only Gateway Acceptance Plan Baseline

Codex B has completed Phase 2.92 docs-only planning. Create a selective Git baseline for the read-only Gateway acceptance plan.

Do not implement Gateway code, do not run DB / NAS / API / CLI smoke, and do not enter Phase 2.93 automatically.

Previous baseline:

- commit: `cf89e1e`
- tag: `phase-2.91-runtime-evidence-writer-smoke-gate-baseline`
- pushed: true

## Review Summary

Codex B reviewed the database team's sanitized `hermes-readonly-frontend-gateway-access-review.md` and converted it into Hermes-side acceptance gates.

Database team has now returned an initial implementation report. It is provisionally positive and should be formally reviewed in Phase 2.93 after this Phase 2.92 baseline.

Phase 2.92 conclusion:

1. Read-only frontend Gateway integration is allowed as a platform-side implementation track.
2. The product / Agent name must be **Hermes** or **Hermes 数据管家**, not Jarvis / 贾维斯.
3. Frontend must call the platform backend Gateway, not raw Hermes internals.
4. `project_scope` / permission proof must be generated server-side by platform backend.
5. Catalog metadata is not document evidence and cannot answer DWG / RVT / NAS content questions.
6. Gateway responses must not expose true `storage_path`, `storage_uri`, raw rows, raw NAS paths, raw file content, secrets, or credential material.
7. Agent DB CRUD, Agent-generated SQL, NAS scan, parser, scratch copy, writer smoke, index writes, Agent answer integration, and production rollout remain forbidden.

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
4. `git status --short` contains only Phase 2.92 docs / handoff files.

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE292_READONLY_GATEWAY_ACCEPTANCE_PLAN.md`
2. `docs/NEXT_CODEX_A_PROMPT.md`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

Do not stage:

1. ignored `reports/agent_runs/latest.json`
2. any DB output, NAS output, approval JSON, `.env`, secret, raw sample, screenshot, or unrelated file
3. code, tests, scripts, migrations, platform DB files, parser files, Gateway implementation files, or frontend files

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
docs: plan phase 2.92 readonly gateway acceptance
```

Tag:

```text
phase-2.92-readonly-gateway-acceptance-plan-baseline
```

Push `origin/main` and the tag.

## Hard Boundaries

Still forbidden:

1. implementing platform Gateway code in this repository
2. running DB / API / CLI / Mac mini Gateway smoke
3. running writer smoke against any real DB
4. enabling DB / NAS / writer / parser / Agent answer feature flags
5. Agent DB CRUD or Agent-generated SQL
6. trusting frontend-supplied `project_scope`
7. returning true `storage_path`, raw row, NAS path, or raw content
8. reading DWG / RVT / NWD / IFC content
9. scanning NAS
10. parser invocation
11. scratch copy
12. writing `documents`, `document_versions`, `chunks`, `citations`
13. writing OpenSearch / Qdrant / MinIO / platform DB / Hermes long-term memory
14. repair / cleanup / backfill / reindex / delete / migration
15. production rollout
16. entering Phase 2.93 automatically

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation that Gateway implementation, DB/NAS access, writer, parser, index/object-store writes, Agent answer integration, and rollout remain blocked
7. final `git status --short`

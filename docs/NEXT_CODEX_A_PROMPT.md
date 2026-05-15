# NEXT_CODEX_A_PROMPT

## Phase 2.87 First Real Hermes Evidence Write Smoke Plan Baseline

Phase 2.87 docs-only planning has been completed.
Codex B review has passed.

The planning document is:

1. `docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md`

## Goal

Baseline the Phase 2.87 planning document and handoff docs.

This prompt does not authorize Phase 2.87a.

Do not implement the writer.
Do not execute a real write.
Do not run parser / copy / DB / index / object-store / Agent answer smoke.

## Review Result

Codex B verified that the Phase 2.87 plan includes:

1. tiny test-machine scope: at most 1 source asset, 1 document version, 20 chunks
2. later explicit operator approval before Phase 2.87a
3. exact write target gate and `Pause` condition if targets cannot be named
4. prerequisite chain from dry-run through rehearsal, permission proof, manifest, eligibility, payload, preflight, rollback
5. operator approval JSON schema
6. feature flags default off
7. no index / object-store / platform DB / audit write in the first smoke
8. rollback limited to records created by one smoke run
9. sanitized ignored report boundary
10. Go / Pause / No-Go decision rules
11. DB platform handoff wording
12. follow-up split for 2.87a / 2.88 / 2.89

## Allowed Files For Baseline

Stage only:

1. `docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md`
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
docs: add phase 2.87 evidence write smoke plan
```

Tag:

```text
phase-2.87-first-real-evidence-write-smoke-plan-baseline
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
16. entering Phase 2.87a without a separate explicit prompt and operator approval

## Completion Report

Report:

1. changed files
2. validation results
3. commit hash
4. tag
5. push result
6. confirmation that Phase 2.87 remains docs-only
7. confirmation that Phase 2.87a remains blocked pending separate authorization
8. confirmation that no real write / parser / copy / DB / index / object-store / Agent answer action occurred

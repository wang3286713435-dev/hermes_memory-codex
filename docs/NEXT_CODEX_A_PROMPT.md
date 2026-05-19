# NEXT_CODEX_A_PROMPT

## Phase 2.103a Codex B Review Fix: Remove Ambiguous Memory Evidence Wording

You are Codex A. Execute only this bounded docs fix, then stop for Codex B review.

## Background

Phase 2.103 handoff pack is complete, but Codex B found one wording blocker in `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`.

Problem sentence:

```text
Hermes answers from safe catalog metadata and existing memory evidence only.
```

Why this is risky:

1. It can make the database / platform team think current catalog-only Gateway integration can already answer from Hermes memory evidence.
2. It blurs the current boundary between catalog metadata, low-sensitive memory references, and governed content evidence.
3. It may imply NAS / DB contents are already in Hermes long-term memory, which violates the shared red lines.

## Required Fix

Modify only:

1. `docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`
2. `docs/PHASE2103_TEST_MACHINE_UPDATE_AND_CAPABILITY_HANDOFF.md` if needed for consistency
3. `docs/NEXT_CODEX_A_PROMPT.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`
9. ignored `reports/agent_runs/latest.json`

Do not touch or stage unrelated `docs/digital-delivery-standards/`.

## Required Wording

Replace ambiguous memory-evidence wording with this meaning:

```text
Hermes answers from safe catalog metadata for catalog questions, and may use only low-sensitive memory references such as related_file_ids / query_id / user feedback labels for continuity. Content-level answers require separately governed retrieval evidence; catalog metadata and low-sensitive memory references must not be treated as file正文 evidence.
```

Ensure both handoff docs state:

1. low-sensitive memory references are not content evidence;
2. `related_file_ids` do not mean Hermes has read or remembered file contents;
3. content answers require governed retrieval / full_text / parser / component evidence;
4. current platform integration remains catalog-only unless a later phase explicitly enables evidence retrieval.

## Validation

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not run API / CLI / Gateway / DB / NAS smoke.
4. Do not connect to DB / NAS / Gateway.
5. Do not read or output raw rows, NAS paths, storage paths, secrets, tokens, or `.env` values.
6. Do not claim DWG/RVT/BIM content understanding.
7. Do not claim PRD 100+ / Roadmap 300+ target satisfaction.
8. Do not enter Phase 3 or production rollout.
9. Do not stage unrelated `docs/digital-delivery-standards/`.

## Completion Report

Report changed files, validation results, and whether Phase 2.103a is ready for Codex B re-review. Stop after the report. Do not baseline.

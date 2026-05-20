# NEXT_CODEX_A_PROMPT

## Stable Hermes Platform Baseline: Test Machine Checkout Gate

You are the test-machine Codex operator. Do not implement runtime features.

The stable Hermes platform integration baseline tag is:

```text
phase-2-stable-hermes-platform-integration-baseline
```

## Goal

Checkout the stable Hermes platform baseline on the test machine and verify docs / JSON / env key names only.

## Required Steps

1. Enter the Hermes_memory repo on the test machine.
2. Confirm current branch and `git status --short`.
3. Fetch tags.
4. Checkout:

```bash
git checkout phase-2-stable-hermes-platform-integration-baseline
```

5. Confirm:

```bash
git rev-parse --short HEAD
git describe --tags --exact-match
git status --short
```

6. Verify required docs exist:

```text
docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md
docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md
docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md
docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md
eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json
eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json
docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md
docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md
docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md
```

7. Validate JSON only:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json >/dev/null
```

8. Verify environment key names only. Do not print values.

## Hard Boundaries

1. Do not run API / CLI / Gateway / DB / NAS smoke unless separately authorized.
2. Do not connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
3. Do not execute SQL.
4. Do not print secret values.
5. Do not run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
6. Do not modify runtime code.
7. Do not modify platform repo files.
8. Do not modify shared `DigitalDeliveryProject` files.

## Go / Pause / No-Go

Go only if checkout succeeds, exact tag matches, worktree is clean, required docs exist, JSON parses, and env key names are checked without printing values.

Pause if tag is missing, worktree is dirty, docs are missing, JSON parse fails, or env names cannot be checked safely.

No-Go if any step would require DB / NAS / Gateway / API connection, print secrets, write data, or run repair/backfill/reindex.

Stop after the report. Do not enter production rollout or Phase 3.

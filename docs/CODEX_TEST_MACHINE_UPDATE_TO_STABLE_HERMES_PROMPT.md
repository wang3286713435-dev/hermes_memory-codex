# Codex Test Machine Prompt: Update To Stable Hermes Baseline

## Goal

Update the test machine to the stable Hermes platform-integration baseline.

This stable tag is a safe platform integration target. It is not a statement that Hermes is only a platform catalog chatbot. Later Hermes releases may unlock native session, Evidence Layer, Memory Layer, and NAS governance while keeping this tag available as the conservative platform baseline.

Stable baseline tag:

```text
phase-2-stable-hermes-platform-integration-baseline
```

## Hard Boundaries

1. Do not run API / CLI / Gateway / DB / NAS smoke unless separately authorized.
2. Do not connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
3. Do not execute SQL.
4. Do not print secret values.
5. Do not run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
6. Do not modify runtime code.
7. Do not modify platform repo files.
8. Do not modify shared `DigitalDeliveryProject` files.

## Required Steps

1. Enter the Hermes_memory repo.
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
docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md
docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md
eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json
docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md
docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md
docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md
```

7. Validate JSON only:

```bash
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json >/dev/null
```

8. Verify environment key names only. Do not print values.

Allowed report shape:

```text
DATABASE_URL key present: yes/no
OPENSEARCH_URL key present: yes/no
QDRANT_URL key present: yes/no
QDRANT_COLLECTION key present: yes/no
ALIYUN_API_KEY key present: yes/no
ALIYUN_RERANK_API_KEY key present: yes/no
```

Do not echo actual values.

## Go / Pause / No-Go

### Go

Report Go only if:

1. checkout succeeded;
2. tag matches `phase-2-stable-hermes-platform-integration-baseline`;
3. worktree is clean;
4. required docs exist;
5. checklist JSON parses;
6. env key names check completed without printing values.

### Pause

Report Pause if:

1. tag is missing;
2. worktree is dirty before checkout;
3. required docs are missing;
4. JSON parse fails;
5. env key names cannot be checked safely.

### No-Go

Report No-Go if:

1. any command would require DB / NAS / Gateway / API connection;
2. any step would print secrets;
3. any step would write data or run repair/backfill/reindex;
4. the test machine cannot checkout the stable tag safely.

## Final Report Template

```text
Test machine update result: Go / Pause / No-Go
Tag requested:
HEAD:
Exact tag:
Worktree status:
Required docs:
Checklist JSON parse:
Env key names checked:
Secrets printed: no
Runtime smoke run: no
DB/NAS/API/Gateway connected: no
Side effects: none
Notes:
```

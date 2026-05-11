# Phase 2.64b Data Steward Selective Integration

## Goal

Phase 2.64b selectively integrates the Data Steward DB branch's readonly asset catalog interface into the current mainline.

This phase intentionally avoids a raw merge from `a272081` because the DB branch predates recent mainline MVP work and would delete or roll back Phase 2.57-2.63 files.

## Source Branch

- Source worktree: `/Users/Weishengsu/Hermes_memory_db0`
- Source branch: `codex/data-steward-db0-contract`
- Source commit: `a272081`
- Source tag: `phase-db-branch-closeout-merge-readiness-baseline`
- Source branch status before intake: pushed to origin

## Integrated Scope

Integrated by explicit whitelist:

1. `app/services/asset_catalog/**`
2. `tests/test_data_steward_*.py`
3. Data Steward / DB contract and smoke docs:
   - `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
   - `docs/DB*.md`
4. Minimal `app/core/config.py` additions for Data Steward feature flags.

## Excluded Scope

Explicitly excluded:

1. Raw `git merge a272081`.
2. `.claude/**`.
3. DB branch handoff files that would overwrite mainline phase state.
4. DB branch untracked QA probe files.
5. Any deletion or rollback of Phase 2.57-2.63 mainline MVP scripts, tests, or docs.
6. Real DB secrets, raw rows, stderr, passwords, NAS scan output, or real sample output.
7. `package.json`, because current mainline already uses `pyproject.toml` / `uv` for the required pytest and ruff commands.

## Feature Flag State

The following Data Steward flags are now present in `app/core/config.py` and default to disabled:

- `platform_asset_catalog_enabled=false`
- `platform_asset_sync_write_enabled=false`
- `platform_asset_mcp_enabled=false`
- `platform_asset_semantic_index_enabled=false`
- `platform_asset_readonly_db_enabled=false`
- `platform_asset_readonly_live_smoke_enabled=false`
- `platform_asset_readonly_mainline_agent_updated=false`
- `platform_asset_readonly_allow_real_sample_data=false`
- `platform_asset_readonly_same_machine_local_dev_authorized=false`

Readonly DB credentials default to `None`.

## Validation

Executed in `/Users/Weishengsu/Hermes_memory`:

```bash
uv run --extra dev pytest \
  tests/test_data_steward_fake_adapter.py \
  tests/test_data_steward_asset_catalog_mirror.py \
  tests/test_data_steward_asset_catalog_temp_db.py \
  tests/test_data_steward_asset_catalog_retrieval_guard.py \
  tests/test_data_steward_asset_catalog_temp_db_retrieval_guard.py \
  tests/test_data_steward_asset_catalog_missing_evidence_response.py \
  tests/test_data_steward_asset_catalog_temp_db_missing_evidence_response.py \
  tests/test_data_steward_asset_catalog_readonly_preflight.py \
  tests/test_data_steward_asset_catalog_readonly_connector.py \
  tests/test_data_steward_asset_catalog_readonly_live_smoke.py \
  tests/test_data_steward_asset_catalog_readonly_local_live_smoke.py -q
```

Result: `71 passed`.

```bash
uv run --extra dev ruff check \
  app/services/asset_catalog \
  tests/test_data_steward_fake_adapter.py \
  tests/test_data_steward_asset_catalog_mirror.py \
  tests/test_data_steward_asset_catalog_temp_db.py \
  tests/test_data_steward_asset_catalog_retrieval_guard.py \
  tests/test_data_steward_asset_catalog_temp_db_retrieval_guard.py \
  tests/test_data_steward_asset_catalog_missing_evidence_response.py \
  tests/test_data_steward_asset_catalog_temp_db_missing_evidence_response.py \
  tests/test_data_steward_asset_catalog_readonly_preflight.py \
  tests/test_data_steward_asset_catalog_readonly_connector.py \
  tests/test_data_steward_asset_catalog_readonly_live_smoke.py \
  tests/test_data_steward_asset_catalog_readonly_local_live_smoke.py \
  app/core/config.py
```

Result: `All checks passed!`

```bash
uv run pytest \
  tests/test_phase263_mvp_operator_daily_summary.py \
  tests/test_phase262_mvp_issue_triage_summary.py \
  tests/test_phase261a_mvp_issue_intake.py -q
```

Result: `28 passed`.

## Non-goals

This phase does not:

- connect to a real DB
- scan NAS
- read `/Volumes/zyzn/卓羽智能项目`
- write migrations
- write `documents` / `chunks`
- write OpenSearch / Qdrant / MinIO
- run real retrieval / indexing
- implement DB-5 selective indexing
- implement DB-6 operation plan / approval
- create a PR
- commit / tag / push
- enter production rollout

## Current Conclusion

Selective integration is implemented and target validation passes. The next step is Codex B review before any baseline, PR, real DB smoke, or merge planning.

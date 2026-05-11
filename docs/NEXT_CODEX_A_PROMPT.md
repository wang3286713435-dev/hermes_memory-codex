# NEXT_CODEX_A_PROMPT

## Phase 2.64b Selective Data Steward DB Integration Git Baseline

你是 Hermes_memory 主线开发 agent。本轮只执行 Phase 2.64b selective Git baseline。

不要继续开发新功能，不连接真实 DB，不扫描 NAS，不创建 PR，不 merge 到 `main`。

## Codex B Review 结论

Codex B 已完成 Phase 2.64b review，结论：通过，可以 baseline。

Review 结果：

1. 本轮没有 raw merge `a272081`。
2. 已选择性合入：
   - `app/services/asset_catalog/**`
   - `tests/test_data_steward_*.py`
   - DB contract / planning / smoke docs
   - `app/core/config.py` 的 Data Steward feature flags，默认全部 off
3. 已排除：
   - `.claude/**`
   - `package.json`
   - DB 支线交接文件覆盖
   - QA probe 文件
   - 会删除 / 回退主线 Phase 2.57-2.63 MVP 文件的变更
4. feature flags 默认关闭。
5. 未连接真实 DB，未扫描 NAS，未写 migration / `documents` / `chunks` / OpenSearch / Qdrant。

Codex B 已复跑：

```bash
uv run --extra dev pytest tests/test_data_steward_fake_adapter.py tests/test_data_steward_asset_catalog_mirror.py tests/test_data_steward_asset_catalog_temp_db.py tests/test_data_steward_asset_catalog_retrieval_guard.py tests/test_data_steward_asset_catalog_temp_db_retrieval_guard.py tests/test_data_steward_asset_catalog_missing_evidence_response.py tests/test_data_steward_asset_catalog_temp_db_missing_evidence_response.py tests/test_data_steward_asset_catalog_readonly_preflight.py tests/test_data_steward_asset_catalog_readonly_connector.py tests/test_data_steward_asset_catalog_readonly_live_smoke.py tests/test_data_steward_asset_catalog_readonly_local_live_smoke.py -q
uv run --extra dev ruff check app/services/asset_catalog tests/test_data_steward_*.py app/core/config.py
uv run pytest tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
python3 -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase264b_review_check.json
```

结果：

- Data Steward tests：`71 passed`
- Data Steward ruff：`All checks passed!`
- MVP runner regression：`28 passed`
- `git diff --check`：passed
- latest JSON check：passed

## 本轮目标

只做 Git baseline。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
uv run --extra dev pytest tests/test_data_steward_fake_adapter.py tests/test_data_steward_asset_catalog_mirror.py tests/test_data_steward_asset_catalog_temp_db.py tests/test_data_steward_asset_catalog_retrieval_guard.py tests/test_data_steward_asset_catalog_temp_db_retrieval_guard.py tests/test_data_steward_asset_catalog_missing_evidence_response.py tests/test_data_steward_asset_catalog_temp_db_missing_evidence_response.py tests/test_data_steward_asset_catalog_readonly_preflight.py tests/test_data_steward_asset_catalog_readonly_connector.py tests/test_data_steward_asset_catalog_readonly_live_smoke.py tests/test_data_steward_asset_catalog_readonly_local_live_smoke.py -q
uv run --extra dev ruff check app/services/asset_catalog tests/test_data_steward_*.py app/core/config.py
uv run pytest tests/test_phase263_mvp_operator_daily_summary.py tests/test_phase262_mvp_issue_triage_summary.py tests/test_phase261a_mvp_issue_intake.py -q
git diff --check
python3 -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase264b_baseline_check.json
```

## Baseline 白名单

只允许 stage 以下文件：

1. `app/core/config.py`
2. `app/services/asset_catalog/**`
3. `tests/test_data_steward_*.py`
4. `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
5. `docs/DB*.md`
6. `docs/PHASE264_DATA_STEWARD_DB_BRANCH_INTAKE_PLAN.md`
7. `docs/PHASE264B_DATA_STEWARD_SELECTIVE_INTEGRATION_PLAN.md`
8. `docs/ACTIVE_PHASE.md`
9. `docs/PHASE_BACKLOG.md`
10. `docs/HANDOFF_LOG.md`
11. `docs/NIGHTLY_SPRINT_QUEUE.md`
12. `docs/NEXT_CODEX_A_PROMPT.md`
13. `docs/TODO.md`
14. `docs/DEV_LOG.md`

## 必须排除

不得 stage 以下文件：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `reports/agent_runs/latest.json`
3. `.claude/**`
4. `package.json`
5. `tests/*probe*.py`
6. `tests/__pycache__/**`
7. 任何真实 DB secrets / NAS scan output / raw rows / stderr / password。
8. 任何真实 issue records / run records。

## Commit / Tag

Commit message：

```text
chore: integrate data steward asset catalog shell
```

Tag：

```text
phase-2.64b-data-steward-selective-integration-baseline
```

Push：

```bash
git push origin HEAD
git push origin phase-2.64b-data-steward-selective-integration-baseline
```

## 硬边界

1. 不连接真实 MySQL / PostgreSQL / platform DB。
2. 不扫描 NAS。
3. 不读取 `/Volumes/zyzn/卓羽智能项目`。
4. 不写 migration。
5. 不写 `documents` / `chunks`。
6. 不写 OpenSearch / Qdrant / MinIO。
7. 不进入 DB-5 selective indexing。
8. 不进入 DB-6 operation plan / approval。
9. 不运行 API / CLI runtime smoke。
10. 不创建 PR。
11. 不 merge 到 `main`。
12. 不进入 production rollout。

## 完成后必须停止

baseline 完成后更新 ignored `reports/agent_runs/latest.json`，记录 commit、tag、push result 和 final status，然后停止。

下一步建议：Phase 2.65 Mac mini MVP landing acceleration / local server update plan，继续优先推进真实可用 MVP；真实 DB smoke 仍等待测试机 Hermes Memory 与用户单独授权。

# Codex Test-machine v1.1 Adapter Smoke Prompt

你是 Hermes Memory 测试机 Codex。本任务用于复验 Hermes 主线已接入 `delivery_platform.asset_views.v1.1` readonly adapter contract。

## 0. 总原则

本任务不是 production rollout，不是 Data Steward runtime 启用，不是 Agent CRUD，不是 mirror / indexing。

只允许执行 reviewed-ref 检查、只读结构 smoke，以及在本 prompt 明确授权下执行 `LIMIT 30` 脱敏聚合统计 smoke。

## 1. 必读文件

在测试机 Hermes_memory 仓库中读取：

1. `docs/PHASE273_HERMES_V11_READONLY_ADAPTER_UPDATE.md`
2. `docs/PHASE274_TEST_MACHINE_V11_ADAPTER_SMOKE_PLAN.md`
3. `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`
4. `docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md`
5. `docs/DB_TEAM_DIRECT_HANDOFF_PROTOCOL.md`

如果任一文件不存在，返回 `Pause`。

## 2. 前置检查

只报告 sanitized 状态：

1. 当前机器用户 / 架构 / macOS 版本。
2. Hermes_memory path、HEAD、nearest tag、dirty 状态。
3. 是否包含 Phase 2.73 v1.1 adapter 更新文件：
   - `app/services/asset_catalog/readonly_preflight.py`
   - `app/services/asset_catalog/contracts.py`
   - `app/services/asset_catalog/retrieval_guard.py`
4. env key 名称是否存在，不输出值。
5. `PLATFORM_ASSET_READONLY_DB_CONTRACT_VERSION` 是否为 `delivery_platform.asset_views.v1.1`，只输出是否匹配。
6. Data Steward runtime / mirror / semantic flags 是否仍默认 off。

如果代码 ref 不含 Phase 2.73，返回 `Pause`，不要继续 DB smoke。

## 3. 允许执行的 structure-only smoke

执行 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md` 中允许的 SQL 形状：

```sql
SELECT 1;
SELECT DATABASE();
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SHOW COLUMNS FROM ProjectAssetView;
SHOW COLUMNS FROM FileAssetView;
SHOW COLUMNS FROM ModelAssetView;
SHOW COLUMNS FROM AuditEventView;
SELECT * FROM ProjectAssetView WHERE 1 = 0;
SELECT * FROM FileAssetView WHERE 1 = 0;
SELECT * FROM ModelAssetView WHERE 1 = 0;
SELECT * FROM AuditEventView WHERE 1 = 0;
```

禁止任何真实行读取。

## 4. 授权执行的 LIMIT 30 脱敏统计 smoke

本 prompt 授权执行一次 `LIMIT 30` 脱敏统计 smoke，条件是：

1. structure-only smoke 已返回 `Go`。
2. 工具链可保证不会输出 raw row。
3. 输出仅为聚合统计。

遵守 `docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md` 的全部禁止项。

如不能保证脱敏，返回 `Pause`，不要执行 `LIMIT 30`。

## 5. 额外 Hermes v1.1 adapter 检查

在不连接真实 DB 的前提下，可运行本地目标测试（如环境具备）：

```bash
uv run python -m py_compile app/services/asset_catalog/*.py app/core/config.py
uv run pytest tests/test_data_steward_asset_catalog_*.py tests/test_data_steward_fake_adapter.py -q
```

如果测试环境缺依赖，报告 `not_run`，不要安装新工具。

## 6. 绝对禁止

不得：

1. 输出 secret / token / password / `.env` 真值。
2. 输出真实项目名、文件名、NAS 路径、raw row。
3. 输出 `asset_uid`、`source_id`、ID 原值、`permission_tags` 原值。
4. 写平台 DB / Hermes DB。
5. 写 OpenSearch / Qdrant / MinIO。
6. 扫描 NAS。
7. 执行 mirror migration。
8. 启用 Data Steward runtime features。
9. 执行 Agent DB CRUD。
10. 执行 repair / cleanup / backfill / reindex / delete / migration。
11. 进入 production rollout。
12. git pull / merge / commit / tag / push，除非另有明确 reviewed-ref 更新任务。

## 7. 输出格式

只返回 sanitized YAML / Markdown 报告：

```yaml
status: go | pause | no_go
machine:
  user: string_without_secret
  arch: string
  macos: string
hermes_memory:
  path_checked: true | false
  head: short_hash_or_null
  tag: tag_or_null
  dirty: true | false
  phase_273_files_present: true | false
env:
  contract_version_expected: delivery_platform.asset_views.v1.1
  contract_version_matches: true | false
  key_names_present: []
  key_names_missing: []
feature_flags:
  runtime_enabled: false
  sync_write_enabled: false
  semantic_index_enabled: false
structure_only_smoke:
  status: go | pause | no_go | not_run
  views_found: []
  views_missing: []
  v1_1_fields_missing_by_view: {}
limit_30_redacted_smoke:
  status: go | pause | no_go | not_run
  raw_rows_output: false
  secret_printed: false
  true_business_data_output: false
  writes_performed: false
  summary: {}
adapter_tests:
  py_compile: passed | failed | not_run
  target_pytest: passed | failed | not_run
permission_fail_closed:
  permission_tags_are_final_auth: false
  rest_project_scope_required: true
  hermes_default_without_rest_scope: DENIED
safety:
  real_rows_read: false
  writes_performed: false
  nas_scanned: false
  runtime_enabled: false
  production_rollout: false
go_pause_no_go_reason: string
```

## 8. Go / Pause / No-Go 判断

Go：

1. Phase 2.73 文件存在。
2. contract version v1.1 匹配。
3. feature flags 仍 off。
4. structure-only smoke Go。
5. `LIMIT 30` 脱敏统计 smoke Go，或因工具不足未执行但 structure-only Go 且无风险。
6. 没有 secret / raw row / 真实业务数据输出。
7. 没有任何写操作。

Pause：

1. 测试机 ref 不含 Phase 2.73。
2. contract version 不匹配。
3. env key 缺失。
4. 工具链不能保证脱敏。
5. 测试依赖缺失但未发生违规。

No-Go：

1. 输出 secret / raw row / 真实业务数据。
2. 发生写操作、NAS scan、mirror、indexing、Agent CRUD 或 rollout。
3. Data Steward runtime 被启用。

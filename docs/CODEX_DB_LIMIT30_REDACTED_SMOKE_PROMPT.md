# CODEX DB LIMIT 30 Redacted Statistics Smoke Prompt

用途：在 `delivery_platform.asset_views.v1.1` structure-only smoke 已通过后，交给测试机 Codex 执行最多 30 行的脱敏统计 smoke。

## 1. 前置条件

只有全部满足才可执行：

1. `delivery_platform.asset_views.v1.1` structure-only smoke 已返回 `Go`。
2. 当前 operator / 用户明确授权执行本 prompt。
3. 测试机只读 DB env key 已通过安全渠道注入。
4. 当前任务只允许读取最多 30 行用于聚合统计，不允许输出 raw row。
5. 测试机工具链能保证 SQL / stdout / stderr 不打印真实行值。

若任一条件不满足，返回 `Pause`。

## 2. 允许目标

本轮只验证 v1.1 字段的值形态和统计质量：

1. 每个 View 最多观察 30 行。
2. 输出 row count。
3. 输出 null / non-null 统计。
4. 输出安全枚举字段分布。
5. 输出 timestamp coverage。
6. 输出 size bucket。
7. 输出 `permission_tags` 前缀覆盖情况，不输出 tag 原值。
8. 输出 `confidentiality_level` / `lifecycle_status` / `index_eligibility` 是否符合约定。

## 3. 严格禁止输出

不得输出：

1. raw row。
2. 真实项目名。
3. 真实文件名。
4. NAS 路径。
5. `project_code` 原值。
6. `project_id` / `file_id` / `model_id` / `event_id` 原值。
7. `target_id` / `operator_id` 原值。
8. `asset_uid` / `source_id`。
9. `checksum` 原值。
10. `permission_tags` 原值。
11. `summary` JSON 原文。
12. secret / token / password / API key / `.env` 真值。
13. 任何可反推出真实业务内容的明细值。

## 4. 严格禁止动作

不得：

1. 写平台 DB。
2. 写 Hermes Memory DB。
3. 写 OpenSearch / Qdrant / MinIO。
4. 扫描 NAS。
5. 执行 migration / repair / backfill / reindex / cleanup / delete。
6. 启用 Data Steward runtime features。
7. 执行 Hermes mirror / indexing。
8. 实现或调用 Agent CRUD。
9. 进入 production rollout。

## 5. 安全执行方式

优先使用 Hermes readonly tooling 或测试机已有的安全脚本，把 raw query output 捕获在进程内，只输出聚合统计。

如果只能使用 `mysql` CLI：

1. 不得执行会把 raw rows 打到终端的 `SELECT * ... LIMIT 30`。
2. 只能执行 aggregate SQL。
3. 不得打印 SQL stderr 中包含的连接串、账号或原始值。
4. 如果无法保证 stdout / stderr 脱敏，返回 `Pause`。

## 6. 建议统计范围

### ProjectAssetView

允许输出：

1. `row_count_observed`
2. `null_count_by_field`
3. `non_null_count_by_field`
4. `confidentiality_level_distribution`
5. `lifecycle_status_distribution`
6. `index_eligibility_distribution`
7. `permission_tags_prefix_coverage`
8. `model_file_count_bucket_distribution`
9. `total_size_bytes_bucket_distribution`
10. `last_asset_updated_at_coverage`
11. `last_seen_at_coverage`

禁止输出：

1. `project_id` 原值
2. `project_code`
3. `project_name`
4. `manager_name`
5. `owner_org_name`
6. `permission_tags` 原值

### FileAssetView

允许输出：

1. `row_count_observed`
2. `file_kind_distribution`
3. `file_ext_distribution`
4. `source_type_distribution`
5. `process_status_distribution`
6. `storage_provider_distribution`
7. `confidentiality_level_distribution`
8. `lifecycle_status_distribution`
9. `index_eligibility_distribution`
10. `permission_tags_prefix_coverage`
11. `size_bytes_bucket_distribution`
12. `created_at_coverage`
13. `updated_at_coverage`
14. `last_seen_at_coverage`

禁止输出：

1. `file_id` 原值
2. `project_id` 原值
3. `project_code`
4. `project_name`
5. `file_name`
6. `checksum`
7. `storage_path`
8. `logical_path`
9. `permission_tags` 原值

### ModelAssetView

允许输出：

1. `row_count_observed`
2. `project_id_presence_count`
3. `model_format_distribution`
4. `discipline_distribution`
5. `preview_available_distribution`
6. `lightweight_status_distribution`
7. `component_index_status_distribution`
8. `confidentiality_level_distribution`
9. `lifecycle_status_distribution`
10. `index_eligibility_distribution`
11. `permission_tags_prefix_coverage`
12. `updated_at_coverage`
13. `last_seen_at_coverage`

禁止输出：

1. `model_id` 原值
2. `file_id` 原值
3. `project_id` 原值
4. `project_code`
5. `model_name`
6. `storage_path`
7. `permission_tags` 原值

### AuditEventView

允许输出：

1. `row_count_observed`
2. `event_id_presence_count`
3. `event_id_monotonic_check_result`
4. `module_code_distribution`
5. `action_code_distribution`
6. `target_type_distribution`
7. `created_at_coverage`

禁止输出：

1. `event_id` 原值
2. `project_id` 原值
3. `target_id`
4. `operator_id`
5. `summary` JSON 原文

## 7. 输出格式

只返回 sanitized YAML：

```yaml
status: go | pause | no_go
db_connection_mode_used: string_without_secret
contract_version_expected: delivery_platform.asset_views.v1.1
limit_30_authorized_for_this_run: true
raw_rows_output: false
secret_printed: false
true_business_data_output: false
writes_performed: false
nas_scanned: false
views_sampled:
  ProjectAssetView:
    row_count_observed: 0
    stats: {}
    forbidden_values_output: false
  FileAssetView:
    row_count_observed: 0
    stats: {}
    forbidden_values_output: false
  ModelAssetView:
    row_count_observed: 0
    stats: {}
    forbidden_values_output: false
  AuditEventView:
    row_count_observed: 0
    stats: {}
    forbidden_values_output: false
permission_fail_closed_assessment:
  permission_tags_missing_count: 0
  project_scope_static_view_expected: false
  rest_project_scope_required: true
  hermes_default_without_rest_scope: DENIED
go_pause_no_go_reason: string
```

## 8. Go / Pause / No-Go

Go：

1. 每个 View 最多观察 30 行。
2. 只输出聚合统计。
3. 没有 raw row / secret / 真实业务标识输出。
4. 没有任何写操作。
5. 能判断字段值形态是否基本可用于后续 readonly adapter planning。

Pause：

1. 工具链无法保证 raw output 不泄露。
2. DB 连接或只读权限不可用。
3. 统计无法生成。
4. 字段缺失导致统计无意义。

No-Go：

1. 输出 raw row。
2. 输出真实项目名 / 文件名 / NAS 路径 / ID 原值 / `permission_tags` 原值。
3. 输出 secret。
4. 发生写操作、NAS scan、migration、mirror、indexing、Agent CRUD 或 rollout。

## 9. 重要边界

本 prompt 不授权 Hermes 使用这些行作为 retrieval evidence。

本 prompt 不授权写入 Hermes mirror。

本 prompt 不授权 Data Steward runtime feature 默认开启。

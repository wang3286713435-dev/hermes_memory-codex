# CODEX DB v1.1 Structure-only Smoke Prompt

用途：在数据库团队完成 `delivery_platform.asset_views.v1.1` 后，交给测试机 Codex 执行结构级复验。

## 前置条件

只有满足以下条件才可执行：

1. 数据库团队已确认 `asset_views.v1.1` 完成。
2. 测试机 Hermes_memory 已安装并处于 reviewed ref。
3. 只读 DB env key 已通过安全渠道注入测试机本地环境。
4. 当前授权范围仍是 `structure_only`。

若任一条件不满足，返回 `Pause`。

## 禁止事项

不得：

1. 打印 secret / token / password / API key / `.env` 真值。
2. 打印真实项目名、文件名、NAS 路径、raw row。
3. 执行 `LIMIT 1` / `LIMIT 30` / `COUNT(*)` over business rows。
4. 读取真实业务行。
5. 写平台 DB / Hermes DB / OpenSearch / Qdrant / MinIO。
6. 扫描 NAS。
7. 执行 migration / repair / backfill / reindex / cleanup / delete。
8. 启用 Data Steward runtime features。
9. 实现或调用 Agent DB CRUD。
10. 进入 production rollout。

## 允许 SQL 形状

只允许：

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

## 必查 v1.1 字段

请只检查字段是否存在，不输出任何真实行。

当前 contract version 预期：

```text
delivery_platform.asset_views.v1.1
```

### ProjectAssetView

建议存在：

1. `permission_tags`
2. `confidentiality_level`
3. `last_seen_at`
4. `lifecycle_status`
5. `index_eligibility`

### FileAssetView

建议存在：

1. `permission_tags`
2. `confidentiality_level`
3. `last_seen_at`
4. `lifecycle_status`
5. `index_eligibility`

### ModelAssetView

必须确认：

1. `project_id`
2. `permission_tags`
3. `confidentiality_level`
4. `last_seen_at`
5. `lifecycle_status`
6. `index_eligibility`

### REST / API Key context

本次 SQL structure-only smoke 不验证调用者态 `project_scope`。请只报告：

```yaml
project_scope_static_view_expected: false
project_scope_rest_contract_required: true
```

### AuditEventView

必须确认：

1. `event_id`
2. `created_at`

并报告：

```yaml
event_id_checkpoint_expected: true
event_id_monotonic_claim_source: database_team_sanitized_response
```

## 输出格式

只返回 sanitized report：

```yaml
status: go | pause | no_go
db_connection_mode_used: string_without_secret
db_reachable: true | false
database_name_matches_expected: true | false
contract_version_expected: delivery_platform.asset_views.v1.1
views_found: []
views_missing: []
v1_1_fields_present_by_view: {}
v1_1_fields_missing_by_view: {}
expected_defaults_or_enums:
  confidentiality_level_default: UNKNOWN
  lifecycle_status_allowed:
    - active
    - archived
    - unknown
    - deleted_candidate
    - stale_unverified
  lifecycle_status_not_allowed_as_static_inference:
    - missing
    - moved
  index_eligibility_default: catalog_only
  permission_tags_expected_prefixes:
    - SOURCE_SYSTEM
    - SOURCE_VIEW
    - ASSET_KIND
    - PROJECT
    - CONFIDENTIALITY
    - INDEX_ELIGIBILITY
project_scope_static_view_expected: false
project_scope_rest_contract_required: true
where_1_eq_0_ok_by_view: {}
secret_printed: false
real_rows_read: false
true_business_data_output: false
writes_performed: false
go_pause_no_go_reason: string
```

## Go / Pause / No-Go

Go：

1. DB reachable。
2. database name matches expected。
3. 四个 View 存在。
4. 四个 View 的 `SHOW COLUMNS` 成功。
5. 四个 View 的 `WHERE 1 = 0` 成功。
6. v1.1 必查字段存在，尤其 `ModelAssetView.project_id`。
7. `project_scope` 未被误判为静态 View 可见范围。
8. 未输出 secret / 真实业务数据。
9. 未读取真实行。
10. 未写任何系统。

Pause：

1. v1.1 尚未完成。
2. 只读 env key 缺失。
3. MySQL client / Hermes readonly tooling 不可用。
4. 字段缺失但未发生违规动作。

No-Go：

1. 读取真实行。
2. 输出 secret 或真实业务数据。
3. 执行任何写入 / migration / NAS scan / indexing / rollout。

# Phase 2.72b DB LIMIT 30 Redacted Statistics Smoke Result

日期：2026-05-12
状态：Go

## 1. 结果摘要

测试机已完成 `delivery_platform.asset_views.v1.1` 的 `LIMIT 30` 脱敏统计 smoke，结果为 `Go`。

该 smoke 只输出聚合统计，没有输出 raw row、真实项目名、文件名、NAS 路径、ID 原值、`permission_tags` 原值、secret 或真实业务数据。

## 2. 安全确认

测试机报告确认：

```yaml
raw_rows_output: false
secret_printed: false
true_business_data_output: false
writes_performed: false
nas_scanned: false
migration_repair_backfill_reindex_cleanup_delete: false
data_steward_runtime_enabled: false
production_rollout: false
```

本轮没有：

1. 写平台 DB。
2. 写 Hermes Memory DB。
3. 写 OpenSearch / Qdrant / MinIO。
4. 扫描 NAS。
5. 执行 migration / repair / backfill / reindex / cleanup / delete。
6. 启用 Data Steward runtime。
7. 执行 mirror / indexing。
8. 执行 Agent CRUD。
9. 进入 production rollout。

## 3. 聚合统计摘要

### ProjectAssetView

```yaml
row_count_observed: 18
confidentiality_level_distribution: { UNKNOWN: 18 }
lifecycle_status_distribution: { active: 18 }
index_eligibility_distribution: { catalog_only: 18 }
permission_tags_prefix_coverage: { observed: 18, missing: 0, expected_prefixes_present: true }
model_file_count_bucket_distribution: { zero: 1, one: 1, two_to_five: 2, gt_five: 14 }
total_size_bytes_bucket_distribution: { zero: 1, lt_1mb: 1, 1mb_to_lt_100mb: 1, 100mb_to_lt_1gb: 1, gte_1gb: 14 }
null_highlights: { last_asset_updated_at: 1, all_other_checked_fields: 0 }
```

### FileAssetView

```yaml
row_count_observed: 30
file_kind_distribution: { DOCUMENT: 2, DRAWING: 26, MODEL: 2 }
file_ext_distribution: { dwg: 25, pdf: 3, rvt: 2 }
source_type_distribution: { MANUAL: 6, NAS_SCAN: 23, REVIEW: 1 }
process_status_distribution: { PROCESSED: 30 }
storage_provider_distribution: { METADATA: 3, NAS: 27 }
confidentiality_level_distribution: { UNKNOWN: 30 }
lifecycle_status_distribution: { active: 30 }
index_eligibility_distribution: { catalog_only: 30 }
permission_tags_prefix_coverage: { observed: 30, missing: 0, expected_prefixes_present: true }
size_bytes_bucket_distribution: { lt_1mb: 12, 1mb_to_lt_100mb: 18 }
null_highlights: { all_checked_fields: 0 }
```

### ModelAssetView

```yaml
row_count_observed: 30
model_format_distribution: { rvt: 30 }
discipline_distribution: { ARCHITECTURE: 8, GENERAL: 13, STRUCTURE: 8, __NULL__: 1 }
preview_available_distribution: { "0": 30 }
lightweight_status_distribution: { NOT_REQUIRED: 30 }
component_index_status_distribution: { NOT_REQUIRED: 30 }
confidentiality_level_distribution: { UNKNOWN: 30 }
lifecycle_status_distribution: { active: 30 }
index_eligibility_distribution: { catalog_only: 30 }
permission_tags_prefix_coverage: { observed: 30, missing: 0, expected_prefixes_present: true }
project_id_presence_count: 30
null_highlights: { all_checked_fields: 0 }
```

### AuditEventView

```yaml
row_count_observed: 30
event_id_presence_count: 30
event_id_monotonic_check_result: pass
event_id_monotonic_violation_count: 0
module_code_distribution: { core: 6, master-data: 24 }
target_type_distribution: { DELIVERABLE_ATTRIBUTE: 3, DELIVERABLE_DEFINITION: 4, DELIVERABLE_TYPE: 4, NODE_TYPE: 5, PROJECT: 3, SECTION_NODE: 8, USER: 3 }
null_highlights: { event_id: 0, created_at: 0 }
```

## 4. 权限 fail-closed 评估

```yaml
permission_tags_missing_count: 0
project_scope_static_view_expected: false
rest_project_scope_required: true
hermes_default_without_rest_scope: DENIED
```

Hermes 侧解释：

1. `permission_tags` 前缀覆盖完整，但仍不是最终用户权限。
2. `project_scope` 必须由 REST / API Key / caller context 提供。
3. 没有调用者授权范围时，Hermes 必须默认 `DENIED`。
4. `index_eligibility=catalog_only` 表示当前只能做资产目录层，不得进入正文 evidence / semantic indexing。

## 5. 当前结论

`LIMIT 30` 脱敏统计 smoke passed。

这意味着：

1. v1.1 字段不仅结构存在，值形态也基本可用于后续 readonly adapter planning。
2. `permission_tags` 覆盖率良好。
3. `confidentiality_level` 当前全部为 `UNKNOWN`，Hermes 必须按敏感 / fail-closed 处理。
4. `lifecycle_status` 当前样本为 `active`。
5. `index_eligibility` 当前样本为 `catalog_only`，不得进入 indexing。
6. `AuditEventView.event_id` 单调检查通过，可作为 checkpoint 规划依据。

下一步建议进入 Hermes v1.1 readonly adapter contract update planning：

1. 更新 fake adapter / contract tests 预期字段。
2. 保持 feature flags 默认 off。
3. 继续区分 asset catalog 与 document evidence。
4. 不启用 mirror / indexing / Agent CRUD。

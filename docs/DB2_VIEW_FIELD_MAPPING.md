# DB-2 View Field Mapping

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-2 schema handoff freeze；docs-only；未接真实平台

## 1. 固定来源

`source_system` 当前固定为 `delivery_platform`。

当前 `source_view` 只允许：

1. `ProjectAssetView`
2. `FileAssetView`
3. `ModelAssetView`
4. `AuditEventView`

新增 View 必须先走 contract version review，不得直接进入同步。

## 2. ProjectAssetView

当前平台已稳定或基本稳定字段：

`project_id`, `project_code`, `project_name`, `project_stage`, `discipline_scope`, `manager_name`, `owner_org_name`, `asset_status`, `model_file_count`, `total_size_bytes`, `last_asset_updated_at`

| Catalog 字段 | 映射规则 | 当前状态 | 缺失处理 |
|---|---|---|---|
| `source_id` | `project_id` | 已有 | 缺失则该 row 无法生成 `asset_uid`，proof 应拒绝或 deny |
| `asset_uid` | `delivery_platform:ProjectAssetView:<project_id>` | 派生 | 缺 `project_id` 不生成 |
| `project_id` | `project_id` | 已有 | 缺失则 `permission_status=DENIED` |
| `project_code` | `project_code` | 已有 | 留空，不作为主键 |
| `project_name` / `file_name` | `project_name` | 已有 | 留空 |
| `asset_kind` | 固定 `project` | 派生 | 固定写入 |
| `file_size` | `total_size_bytes` | 已有 | 留空 |
| `owner` | 优先 `manager_name`，否则 `owner_org_name` | 部分已有 | 留空 |
| `source_path` / `storage_location` | 无稳定字段 | 当前没有 | 留空 |
| `modified_at` | `last_asset_updated_at` | 已有 | 缺失时 proof 用 sync time 并写 `derived_metadata_source=SYNC_DERIVED` |
| `lifecycle_status` | `asset_status` 可作为辅助 | 部分已有 | 未明确映射时默认 `ACTIVE` |
| `data_quality_flags` | `asset_status` 异常可记录 | 派生 | 不因一次缺失判定删除 |
| `raw_payload` | 原始 View row | 可选 | 只用于排查，不作长期查询依据 |

## 3. FileAssetView

当前平台已稳定或基本稳定字段：

`file_id`, `project_id`, `project_code`, `project_name`, `file_name`, `file_ext`, `file_kind`, `discipline`, `version_no`, `size_bytes`, `checksum`, `storage_provider`, `storage_path`, `logical_path`, `source_type`, `process_status`, `created_at`, `updated_at`

| Catalog 字段 | 映射规则 | 当前状态 | 缺失处理 |
|---|---|---|---|
| `source_id` | `file_id` | 已有 | 缺失则不生成 `asset_uid` |
| `asset_uid` | `delivery_platform:FileAssetView:<file_id>` | 派生 | 缺 `file_id` 不生成 |
| `project_id` | `project_id` | 已有 | 缺失则 `permission_status=DENIED` |
| `project_code` | `project_code` | 已有 | 留空可接受 |
| `project_name` | `project_name` | 已有 | 留空可接受 |
| `asset_kind` | `file_kind`，缺失时 `file` | 已有 / 派生 | fallback 为 `file` |
| `file_name` | `file_name` | 已有 | 留空但写 data quality flag |
| `file_ext` | `file_ext` | 已有 | 留空 |
| `mime_type` | 由 `file_ext` 粗派生 | 派生 | 不能读取文件内容探测 |
| `file_size` | `size_bytes` | 已有 | 留空 |
| `content_hash` | `checksum` | 已有 | 留空；不得复用正文 evidence |
| `storage_location` | `storage_provider + ":" + storage_path` | 已有 | 只保存路径字符串，不访问 NAS |
| `source_path` | 优先 `logical_path`，否则 `storage_path` | 已有 | 留空 |
| `version_key` | `version_no` | 已有 | 留空 |
| `created_at` | `created_at` | 已有 | 留空 |
| `modified_at` | `updated_at` | 已有 | 缺失时 proof 用 sync time 并标记 `SYNC_DERIVED` |
| `parent_asset_uid` | `delivery_platform:ProjectAssetView:<project_id>` | 可派生 | 缺 `project_id` 留空且 deny |
| `lifecycle_status` | `process_status` 可作为辅助 | 部分已有 | 未明确时默认 `ACTIVE` |

## 4. ModelAssetView

当前平台已稳定或基本稳定字段：

`model_id`, `file_id`, `project_code`, `model_name`, `model_format`, `discipline`, `version_no`, `preview_available`, `lightweight_status`, `component_index_status`, `storage_path`, `updated_at`

| Catalog 字段 | 映射规则 | 当前状态 | 缺失处理 |
|---|---|---|---|
| `source_id` | `model_id` | 已有 | 缺失则不生成 `asset_uid` |
| `asset_uid` | `delivery_platform:ModelAssetView:<model_id>` | 派生 | 缺 `model_id` 不生成 |
| `project_code` | `project_code` | 已有 | 留空 |
| `project_id` | 当前 View 未稳定提供 | 当前没有 | 留空；没有 project_id 时默认不得进入检索上下文 |
| `asset_kind` | 固定 `model` | 派生 | 固定写入 |
| `file_name` | `model_name` | 已有 | 留空 |
| `file_ext` | `model_format` | 已有 | 留空 |
| `mime_type` | 由 `model_format` 粗派生 | 派生 | 不读取模型内容 |
| `source_path` | `storage_path` | 已有 | 留空 |
| `storage_location` | `storage_path` | 已有 | 留空 |
| `version_key` | `version_no` | 已有 | 留空 |
| `parent_asset_uid` | `delivery_platform:FileAssetView:<file_id>` | 可派生 | 缺 `file_id` 留空 |
| `modified_at` | `updated_at` | 已有 | 缺失时 proof 用 sync time 并标记 `SYNC_DERIVED` |
| `index_status` | 不由 `component_index_status` 提升 | 已有辅助字段 | DB-2 固定 `CATALOG_ONLY` |
| `parse_status` | 不由 `lightweight_status` 提升 | 已有辅助字段 | DB-2 固定 `NOT_REQUESTED` |

DB-2 不解析 BIM 模型，不建立构件索引，不写 preview / semantic index。

## 5. AuditEventView

当前平台已稳定或基本稳定字段：

`event_id`, `project_id`, `module_code`, `action_code`, `target_type`, `target_id`, `operator_id`, `summary`, `created_at`

| Catalog 字段 | 映射规则 | 当前状态 | 缺失处理 |
|---|---|---|---|
| `source_id` | `event_id` | 已有 | 缺失则不能作为 checkpoint 事件 |
| `asset_uid` | `delivery_platform:AuditEventView:<event_id>` | 派生 | 缺 `event_id` 不生成 |
| `project_id` | `project_id` | 已有 | 缺失则 deny |
| `asset_kind` | 固定 `audit_event` | 派生 | 固定写入 |
| `file_name` | 可用 `summary` 作短展示名 | 已有 | 留空 |
| `owner` | `operator_id` | 已有 | 留空 |
| `created_at` | `created_at` | 已有 | 留空 |
| `modified_at` | `created_at` | 已有 | 作为事件时间映射 |
| `last_event_id` | `event_id` | 已有 | 缺失时不得更新 checkpoint |
| `data_quality_flags` | 异常 action / target 可记录 | 派生 | 不作为业务事实 |

Audit event catalog row 不等于正文 evidence。`summary` 不得作为 citation 正文或长期事实写入。

## 6. 缺字段处理冻结

1. 缺 `permission_tags`：`permission_status=DENIED`。
2. 缺 `project_scope`：不得进入 prompt。
3. 缺 `project_id`：不得进入用户检索上下文。
4. 缺 `confidentiality_level`：写 `UNKNOWN`。
5. 缺 `last_seen_at`：proof 阶段使用同步时间，并写 `derived_metadata_source=SYNC_DERIVED`。
6. 缺 `source_modified_at`：优先映射 `updated_at` / `last_asset_updated_at` / `created_at`，并保留来源说明。
7. 缺 moved / stale / missing 明确状态：只允许写 `candidate_missing` 或 `UNKNOWN`；不得自动判定删除。
8. 路径变化只作为 catalog metadata 变化；不移动 NAS 文件。
9. hash 相同但路径变化，必须有平台事件或连续扫描证据才可标记 `MOVED`。
10. 一次扫描缺失不得标记真实 `DELETED`。

# DB-2 Schema Review Response

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：docs-only schema review response；未授权 migration；未接真实 MySQL / NAS / REST

## 1. 本轮结论

数据库 / NAS / 数字化交付平台侧已认可 `DB2_SCHEMA_CONTRACT.md` 可作为 DB-2 真实数据库接入前的 schema contract 基线。

本轮更新采用以下决策：

1. `external_asset_catalog` 作为默认表名。
2. `hermes_external_asset_catalog` 作为命名空间备选。
3. `asset_uid = source_system + ":" + source_view + ":" + source_id`。
4. `source_system` 默认固定为 `delivery_platform`。
5. `source_view` 固定为 `ProjectAssetView` / `FileAssetView` / `ModelAssetView` / `AuditEventView`。
6. `external_asset_sync_checkpoint` 纳入 DB-2 schema contract 的真实 migration 候选表。
7. DB-2 真实 migration 仍未授权。

## 2. 对 14 个问题的明确回答

1. 最终表名是否确定为 `external_asset_catalog`？
   - 已确认。默认使用 `external_asset_catalog`；只有数据库团队要求 Hermes 命名空间时才使用 `hermes_external_asset_catalog`。

2. 是否接受 `source_system` 固定为 `delivery_platform`？
   - 已确认。DB-2 真实接入默认 `source_system=delivery_platform`；同一环境不得混用 `platform` 与 `delivery_platform`。

3. `source_view` 是否固定为四个 View？
   - 已确认。DB-2 当前固定为 `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView`。新增 View 必须走 contract version review。

4. 是否将 View contract version 写入 mirror 表或同步 checkpoint？
   - 已确认需要。`contract_version` 写入 `external_asset_catalog`；`source_contract_version` 写入 `external_asset_sync_checkpoint`。

5. 是否新增 `external_asset_sync_checkpoint` 表？
   - 已确认纳入 schema contract。它只服务 mirror 同步，不存正文、不存 embedding、不影响 `documents` / `chunks`。

6. checkpoint rollback 记录保存在哪里？
   - 初版保存在 `external_asset_sync_checkpoint`。每个 checkpoint row 使用 `checkpoint_scope_key` 标识 `source_system + source_view (+ project_id)`，并保存 `run_id`、`last_event_id`、`overlap_started_at`、`last_synced_at` 和 `status`。更完整的 run history 可在后续 DB-2.x 评估，不阻塞当前 schema freeze。

7. MySQL JSON 字段是否确认使用 JSON 类型，而不是 TEXT？
   - 已确认目标 MySQL 使用 `JSON` 类型。若目标库为 PostgreSQL，等价使用 `JSONB`。初版不依赖 JSON 内部索引。

8. timestamp 是否统一按 UTC？
   - 已确认。所有 `*_at` 字段按 UTC 存储；平台字段时区由平台团队在真实接入前确认。

9. migration down 在开发 / 预生产 / 生产分别怎么处理？
   - 开发环境：允许 drop 新 mirror 表。
   - 预生产：未被共享依赖时允许 drop；一旦共享使用，采用 forward migration。
   - 生产：不直接 drop，采用停止同步、标记 deprecated、保留审计数据、forward migration。

10. DB-2 真实 migration 是否仍保持 docs-only，等待用户单独授权？
    - 已确认。当前仍 docs-only，不写 migration。真实 migration 必须等用户单独授权。

11. `lifecycle_status` 在平台未提供明确状态时是否默认 `ACTIVE`？
    - 已确认。平台未提供明确状态时默认 `ACTIVE`；同步缺失先写 `candidate_missing` 或 `data_quality_flags`，不因一次扫描缺失直接判定真实删除。

12. `permission_status` 在权限字段缺失时是否强制 `DENIED`？
    - 已确认。数据库默认值和应用写入均必须 fail closed 为 `DENIED`。

13. catalog-only 是否一定不会进入 `documents` / `chunks` / Qdrant / OpenSearch？
    - 已确认。DB-2 catalog-only 数据不进入这些正文 evidence / index 存储。

14. Missing Evidence 的响应格式是否已在 Hermes_memory 侧定义？
    - 已有边界定义：catalog-only 资产在正文回答场景必须返回 Missing Evidence，reason 建议为 `asset_catalog_only`。最终用户可见响应格式属于 DB-3 retrieval / answer contract，DB-2 不实现。

15. DB-3 启动条件是什么？
    - DB-3 只能在 DB-2 migration / fake fixtures / temporary DB proof / schema review 均通过后，由用户单独授权启动。DB-3 还必须明确 permission filter、Missing Evidence、catalog-only 与 document evidence 分层，并通过 Codex review 与测试 agent 复测。

## 3. 当前 View 已有字段

### ProjectAssetView

1. `project_id`
2. `project_code`
3. `project_name`
4. `project_stage`
5. `discipline_scope`
6. `manager_name`
7. `owner_org_name`
8. `asset_status`
9. `model_file_count`
10. `total_size_bytes`
11. `last_asset_updated_at`

### FileAssetView

1. `file_id`
2. `project_id`
3. `project_code`
4. `project_name`
5. `file_name`
6. `file_ext`
7. `file_kind`
8. `discipline`
9. `version_no`
10. `size_bytes`
11. `checksum`
12. `storage_provider`
13. `storage_path`
14. `logical_path`
15. `source_type`
16. `process_status`
17. `created_at`
18. `updated_at`

### ModelAssetView

1. `model_id`
2. `file_id`
3. `project_code`
4. `model_name`
5. `model_format`
6. `discipline`
7. `version_no`
8. `preview_available`
9. `lightweight_status`
10. `component_index_status`
11. `storage_path`
12. `updated_at`

### AuditEventView

1. `event_id`
2. `project_id`
3. `module_code`
4. `action_code`
5. `target_type`
6. `target_id`
7. `operator_id`
8. `summary`
9. `created_at`

## 4. 当前不能假设稳定的字段

以下字段可保留在 mirror schema，但不能作为平台 View 当前稳定字段处理：

1. `permission_tags`
2. `project_scope`
3. `confidentiality_level`
4. 完整 moved / stale / missing 映射
5. `source_modified_at`
6. `last_seen_at`
7. `is_latest`
8. `previous_source_path`
9. `data_quality_flags`

处理方式：

1. 能由平台后续补充的，标记为待平台字段。
2. 能由 Hermes_memory 计算的，标记为 mirror 派生字段。
3. 当前无法确认的，不作为真实接入前硬依赖。

## 5. Checkpoint 表策略

`external_asset_sync_checkpoint` 纳入 DB-2 schema contract，但真实创建仍需 migration 授权。

该表只服务 mirror 同步：

1. 不存正文。
2. 不存 chunk。
3. 不存 embedding。
4. 不影响 `documents` / `chunks`。
5. 可 drop / 可重建。

推荐 checkpoint 粒度：

1. 初版：`source_system + source_view`。
2. 扩展：`source_system + source_view + project_id`。

## 6. 仍然禁止

1. 不写真实 migration。
2. 不连接真实 MySQL。
3. 不接真实 NAS。
4. 不触发真实 REST 动作。
5. 不写 OpenSearch / Qdrant。
6. 不进入 DB-3 retrieval。
7. 不做 selective indexing。

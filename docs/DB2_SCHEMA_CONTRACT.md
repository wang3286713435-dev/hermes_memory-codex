# DB-2 Schema Contract

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：真实数据库接入前 schema contract review；docs-only；未授权 migration

## 1. 当前定位

DB-2 仍只允许：

1. fake adapter dry-run preview。
2. temporary DB proof-of-contract。
3. schema contract 文档冻结。

DB-2 仍禁止：

1. 连接真实 MySQL / NAS / REST。
2. 扫描真实 NAS。
3. 写 `documents` / `chunks`。
4. 写 OpenSearch / Qdrant。
5. 进入 DB-3 retrieval / selective indexing。
6. 创建 migration，除非用户后续单独授权。

## 2. 已确认

1. 表名默认使用 `external_asset_catalog`。
2. 如果数据库团队要求 Hermes 命名空间，备选表名为 `hermes_external_asset_catalog`。
3. 禁止使用 `documents`、`chunks`、`memories`、`facts` 等名称，避免误导为正文 evidence 或长期记忆事实表。
4. 主键使用 `asset_uid`。
5. 真实 mirror 的 `asset_uid` 格式冻结为 `source_system + ":" + source_view + ":" + source_id`。
6. 增加唯一约束 `UNIQUE (source_system, source_view, source_id)`。
7. `source_id` 是平台 View 原始 ID，不等于 `project_id`。
8. `project_id` 用于权限和项目范围过滤，不作为资产主键。
9. `source_path` 不作为主键，因为路径会移动或重命名。
10. `permission_status` 数据库默认值必须是 `DENIED`。
11. `permission_tags` 与 `project_scope` 初版使用 JSON 字段存储。
12. moved / stale / missing 资产保留在 catalog 表中，不直接物理删除。
13. `last_event_id` 是主要 checkpoint 候选字段，但不能作为唯一依据。
14. `updated_at` / `source_updated_at` 只能作为辅助，不作为唯一增量依据。
15. `raw_payload` 允许存在，只用于兼容和排查，不作为长期业务查询依据。
16. `source_system` 默认固定为 `delivery_platform`，同一环境不得混用 `platform` 与 `delivery_platform`。
17. `source_view` 当前固定为 `ProjectAssetView`、`FileAssetView`、`ModelAssetView`、`AuditEventView`；新增 View 必须走 contract version review。
18. `contract_version` 必须写入 mirror 表；checkpoint 表记录 `source_contract_version`。
19. 目标 MySQL 使用 `JSON` 类型；PostgreSQL 等价使用 `JSONB`。初版不依赖 JSON 内部索引。
20. 所有 timestamp 字段统一按 UTC 存储。
21. `external_asset_sync_checkpoint` 纳入 DB-2 schema contract 的 migration 候选表，只服务 mirror 同步。

注意：DB-1a fake adapter 的既有 `asset_uid` 仍是 `source_system + ":" + source_id`，这是 DB-1a fake contract。真实数据库 mirror 前，DB-2 写入层必须按本合同重新生成真实 mirror `asset_uid`。

## 2.1 当前平台 View 字段

当前平台已稳定或基本稳定的字段如下。DB-2 真实接入前，fake fixtures 应逐步向这些字段靠齐，但不得因此连接真实平台。

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

## 2.2 目标字段与预留字段

以下字段可以保留在 `external_asset_catalog`，但当前不能假设已经由平台 View 稳定提供：

1. `permission_tags`
2. `project_scope`
3. `confidentiality_level`
4. 完整 moved / stale / missing 映射
5. `source_modified_at`
6. `last_seen_at`
7. `is_latest`
8. `previous_source_path`
9. `data_quality_flags`

这些字段在 schema 中分别标记为：

1. mirror 侧预留字段。
2. 平台后续补充字段。
3. Hermes_memory 派生字段。

## 2.3 Source ID 映射

当前平台侧建议映射：

1. `ProjectAssetView.source_id = project_id`
2. `FileAssetView.source_id = file_id`
3. `ModelAssetView.source_id = model_id`
4. `AuditEventView.source_id = event_id`

这些映射只定义 mirror 身份，不改变平台原始 ID 的类型和语义。

## 3. 待数据库团队确认

1. 最终表名是否要求使用 Hermes 命名空间；默认仍是 `external_asset_catalog`。
2. `permission_tags` / `project_scope` 是否需要在后续拆成子表，例如 `external_asset_permissions`。
3. 枚举字段是否需要数据库层 `CHECK` 约束，还是先由应用层校验。
4. 索引命名、长度限制和字符集 / collation。
5. migration down 脚本策略：预生产允许 drop，生产只允许 forward migration。
6. 共享环境是否需要 shadow table；初版新增表不需要，后续破坏性变更再评估。

## 4. 待平台团队确认

1. `source_id` 在同一 `source_system + source_view` 内是否稳定唯一。
2. `AuditEventView.event_id` 是否保证单调递增；未确认前按可能乱序处理。
3. event_id 是否可能乱序、补写或跨 View 共用序列。
4. 如果没有 event_id，是否可用 `created_at + source_view cursor` 兜底。
5. moved / stale / missing / deleted 的完整平台状态映射。
6. `source_modified_at`、`last_seen_at` 的字段来源。

## 5. 字段契约

### 身份字段

| 字段 | 类型建议 | 状态 | 说明 |
|---|---|---|---|
| `asset_uid` | `VARCHAR(256)` | 已确认 | 主键，格式 `source_system:source_view:source_id` |
| `source_system` | `VARCHAR(64)` | 已确认 | 平台来源 |
| `source_view` | `VARCHAR(64)` | 已确认 | View 名称 |
| `source_id` | `VARCHAR(128)` | 已确认 | 平台 View 原始 ID |
| `project_id` | `VARCHAR(128)` | 待平台确认 | 当前 fake fixtures 有非数字项目 ID，不冻结为 `BIGINT` |
| `project_code` | `VARCHAR(128)` | 已确认 | 展示和人工排查 |
| `project_name` | `VARCHAR(255)` | 已确认 | 展示 |
| `contract_version` | `VARCHAR(64)` | 已确认 | 当前 source View contract version |

### 资产字段

| 字段 | 类型建议 | 状态 | 说明 |
|---|---|---|---|
| `asset_kind` | `VARCHAR(64)` | 已确认 | project / file / model 等 |
| `file_id` | `VARCHAR(128)` | 已确认 | File / Model 关联的平台 file id |
| `model_name` | `VARCHAR(512)` | 已确认 | 模型名 |
| `model_format` | `VARCHAR(64)` | 已确认 | IFC / RVT 等 |
| `discipline` | `VARCHAR(128)` | 已确认 | 专业 |
| `version_no` | `VARCHAR(128)` | 已确认 | 平台版本号 |
| `file_name` | `VARCHAR(512)` | 已确认 | 文件名 |
| `file_ext` | `VARCHAR(32)` | 已确认 | 扩展名 |
| `mime_type` | `VARCHAR(128)` | 已确认 | MIME |
| `source_path` | `TEXT` | 已确认 | 平台或 NAS 当前路径，不作主键 |
| `storage_provider` | `VARCHAR(64)` | 已确认 | 存储类型 |
| `storage_path` | `TEXT` | 已确认 | 存储路径 |
| `logical_path` | `TEXT` | 已确认 | 展示路径 |
| `file_size` | `BIGINT` | 已确认 | 文件大小 |
| `content_hash` | `VARCHAR(128)` | 已确认 | 文件 hash，缺失不得复用正文 evidence |
| `version_key` | `VARCHAR(128)` | 已确认 | 平台版本键 |
| `is_latest` | `BOOLEAN` | 已确认 | 是否最新 |

### 权限字段

| 字段 | 类型建议 | 状态 | 说明 |
|---|---|---|---|
| `permission_status` | `VARCHAR(32)` | 已确认 | 默认 `DENIED` |
| `project_scope` | `JSON` | 已确认 | 初版 JSON |
| `permission_tags` | `JSON` | 已确认 | 初版 JSON，缺失时 deny |
| `confidentiality_level` | `VARCHAR(32)` | 已确认 | 保密等级 |

`permission_status` 枚举：

1. `ALLOWED`
2. `DENIED`
3. `UNKNOWN`
4. `STALE`

## 6. 生命周期与状态

`lifecycle_status` 默认 `ACTIVE`，枚举：

1. `ACTIVE`
2. `MISSING`
3. `MOVED`
4. `STALE`
5. `ARCHIVED`
6. `EXCLUDED`
7. `DELETED`

策略：

1. 平台未提供明确状态时默认 `ACTIVE`。
2. 一次扫描缺失不得直接判定真实删除。
3. 同步缺失先标记 `candidate_missing` 或写入 `data_quality_flags`。
4. 真正 `MISSING` / `MOVED` / `STALE` 需要平台事件或连续扫描证据确认。
5. hash 相同但路径变化且有平台证据时，标记 `MOVED` 并保留 `previous_source_path`。
6. 不物理删除 mirror 记录，除非执行受控清理任务。

状态字段：

| 字段 | 默认值 | 说明 |
|---|---|---|
| `sync_status` | `PENDING` | catalog 同步状态 |
| `index_status` | `CATALOG_ONLY` | DB-2 不写正文索引 |
| `parse_status` | `NOT_REQUESTED` | DB-2 不解析正文 |
| `semantic_index_status` | `NOT_REQUESTED` | DB-2 不写向量 |
| `citation_status` | `NOT_REQUESTED` | DB-2 不提供正文 citation |

DB-2 不得因为 catalog mirror 写入成功，就把资产标记为可正文回答。只有 catalog 的资产，在用户问正文内容时必须返回 Missing Evidence，建议 reason 为 `asset_catalog_only`。

## 7. 最小索引

已确认的最小索引：

1. `PRIMARY KEY (asset_uid)`
2. `UNIQUE KEY uk_external_asset_source (source_system, source_view, source_id)`
3. `INDEX idx_external_asset_project (project_id)`
4. `INDEX idx_external_asset_project_code (project_code)`
5. `INDEX idx_external_asset_source_view (source_system, source_view)`
6. `INDEX idx_external_asset_permission (permission_status)`
7. `INDEX idx_external_asset_sync (sync_status)`
8. `INDEX idx_external_asset_event (last_event_id)`
9. `INDEX idx_external_asset_seen (last_seen_at)`
10. `INDEX idx_external_asset_lifecycle (lifecycle_status)`
11. `INDEX idx_external_asset_kind (asset_kind)`

PostgreSQL 可考虑 JSONB + GIN。MySQL 初版使用 `JSON` 类型但不强依赖 JSON 内部索引，项目级过滤优先使用 `project_id`、`project_code`、`permission_status`。

MySQL 注意事项：

1. 使用 `utf8mb4` 字符集。
2. 注意索引名长度限制。
3. 注意 `VARCHAR` 长度和唯一键长度。
4. `source_path`、`storage_path`、`logical_path` 是 `TEXT`，不建普通索引。
5. 路径检索短期由 OpenSearch / metadata index 承担，不由 DB 普通索引承担；DB-2 本身不写 OpenSearch。

## 8. Checkpoint 契约

字段：

1. `last_event_id BIGINT NULL`
2. `last_synced_at TIMESTAMP NOT NULL`
3. `source_updated_at TIMESTAMP NULL`
4. `source_modified_at TIMESTAMP NULL`
5. `last_seen_at TIMESTAMP NULL`

策略：

1. 首次同步全量读取稳定 View。
2. 记录最大 `last_event_id` 和 `last_synced_at`。
3. 后续优先按 AuditEventView / 事件流拉取变化。
4. 对 event_id 乱序或补写，保留 `created_at` overlap window 兜底。
5. `updated_at` 只能作为辅助，不作为唯一增量依据。
6. checkpoint 粒度为 `source_system + source_view`。
7. 如果平台规模要求，可后续扩展为 `source_system + source_view + project_id`。
8. 保留可重放同步窗口。

待平台团队确认：

1. `event_id` 是否保证单调递增。
2. 是否存在跨 View 乱序。
3. 无 event_id 时是否能提供 `created_at + source_view cursor`。

## 8.1 Checkpoint 表契约

`external_asset_sync_checkpoint` 纳入 DB-2 schema contract 的真实 migration 候选表。是否与 `external_asset_catalog` 同一轮创建，仍需用户单独授权 migration 后再决定。

该表只服务 mirror 同步：

1. 不影响 `documents` / `chunks`。
2. 不存正文。
3. 不存 embedding。
4. 可 drop / 可重建。
5. 不替代平台 checkpoint。

逻辑 schema 草案：

```sql
CREATE TABLE external_asset_sync_checkpoint (
    checkpoint_id VARCHAR(256) PRIMARY KEY,
    checkpoint_scope_key VARCHAR(256) NOT NULL,
    source_system VARCHAR(64) NOT NULL,
    source_view VARCHAR(64) NOT NULL,
    project_id VARCHAR(128) NULL,
    source_contract_version VARCHAR(64) NULL,
    last_event_id BIGINT NULL,
    overlap_started_at TIMESTAMP NULL,
    last_synced_at TIMESTAMP NOT NULL,
    run_id VARCHAR(128) NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    UNIQUE (checkpoint_scope_key)
);
```

Checkpoint rollback 位置：

1. 初版保存在 `external_asset_sync_checkpoint` 当前 row。
2. `checkpoint_scope_key` 由应用生成，初版为 `source_system + ":" + source_view`；项目级扩展时为 `source_system + ":" + source_view + ":" + project_id`。
3. 每次同步任务必须记录 `run_id`、上一个 checkpoint、当前 overlap window。
4. 更完整的 checkpoint run history 可在 DB-2.x 增加历史表，不阻塞当前 schema review。
5. 如果 checkpoint 不可信，停止同步，清空 mirror 表并全量重建。

## 9. Schema 草案

以下是逻辑 schema 草案。具体 SQL 方言在 migration 阶段按目标数据库调整。

```sql
CREATE TABLE external_asset_catalog (
    asset_uid VARCHAR(256) PRIMARY KEY,
    source_system VARCHAR(64) NOT NULL,
    source_view VARCHAR(64) NOT NULL,
    source_id VARCHAR(128) NOT NULL,
    contract_version VARCHAR(64) NULL,

    project_id VARCHAR(128) NULL,
    project_code VARCHAR(128) NULL,
    project_name VARCHAR(255) NULL,

    asset_kind VARCHAR(64) NULL,
    file_id VARCHAR(128) NULL,
    model_name VARCHAR(512) NULL,
    model_format VARCHAR(64) NULL,
    discipline VARCHAR(128) NULL,
    version_no VARCHAR(128) NULL,
    file_name VARCHAR(512) NULL,
    file_ext VARCHAR(32) NULL,
    mime_type VARCHAR(128) NULL,
    source_path TEXT NULL,
    storage_provider VARCHAR(64) NULL,
    storage_path TEXT NULL,
    logical_path TEXT NULL,

    file_size BIGINT NULL,
    content_hash VARCHAR(128) NULL,
    version_key VARCHAR(128) NULL,
    is_latest BOOLEAN NULL,

    permission_status VARCHAR(32) NOT NULL DEFAULT 'DENIED',
    project_scope JSON NULL,
    permission_tags JSON NULL,
    confidentiality_level VARCHAR(32) NULL,

    lifecycle_status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
    data_quality_flags JSON NULL,
    previous_source_path TEXT NULL,

    sync_status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    index_status VARCHAR(32) NOT NULL DEFAULT 'CATALOG_ONLY',
    parse_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUESTED',
    semantic_index_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUESTED',
    citation_status VARCHAR(32) NOT NULL DEFAULT 'NOT_REQUESTED',

    last_event_id BIGINT NULL,
    source_created_at TIMESTAMP NULL,
    source_updated_at TIMESTAMP NULL,
    source_modified_at TIMESTAMP NULL,
    last_seen_at TIMESTAMP NULL,
    last_synced_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    raw_payload JSON NULL,

    UNIQUE (source_system, source_view, source_id)
);
```

禁止保存：

1. 正文。
2. chunk。
3. embedding。
4. citation 正文。
5. 平台资产表的 source of truth。

## 10. Rollback 契约

已确认：

1. DB-2 migration 只允许新增 mirror 相关表和索引，不修改 `documents` / `chunks` / retrieval 主表。
2. 开发环境允许 drop 新 mirror 表。
3. 预生产未被共享依赖时允许 drop；一旦共享使用，采用 forward migration。
4. 如果已进入共享环境或生产环境，不直接 drop，改为 forward migration：
   - 停止同步任务。
   - 标记 mirror 表为 deprecated。
   - 保留数据用于审计和排查。
   - 新建修正 migration。
5. DB-2 写入失败时，可以清空 `external_asset_catalog` 后重新同步，因为它只是 mirror，不是 source of truth。
6. rollback 不得影响 `documents`、`chunks`、Qdrant、OpenSearch、memory kernel 或平台 MySQL 正式资产表。

待数据库团队确认：

1. 预生产环境 migration down 是否允许 `DROP TABLE external_asset_catalog`。
2. 生产环境 down 脚本是否采用 no-op + forward migration 策略。
3. 是否需要 shadow table；初版新增表不需要，未来破坏性变更再评估。
4. 是否需要 checkpoint history 表；初版只冻结 current checkpoint 表。
5. mirror 重建的预计耗时和平台限流风险。

Checkpoint 回退建议：

1. 每次真实同步前记录 run id、source_view、last checkpoint 和时间窗口。
2. 回退时停止同步任务。
3. 将 checkpoint 恢复到上一个安全 run。
4. 如 checkpoint 不可信，清空 mirror 表并执行全量重建。

## 11. 真实接入门槛

进入真实数据库前，必须全部满足：

1. 用户明确授权 migration。
2. 数据库团队确认表名、主键、唯一约束、字段类型、索引。
3. 平台团队确认 View contract version。
4. 平台团队确认 `source_system` / `source_view` / `source_id` 映射。
5. 平台团队确认 AuditEventView.event_id 语义。
6. `permission_status` 缺省 `DENIED` 写入数据库层默认值。
7. migration 只新增 mirror 表，不改 `documents` / `chunks` / retrieval 表。
8. fake fixtures 和 temporary DB proof 继续先行。
9. Codex review 无 P0/P1/P2。
10. 测试 agent 独立复测通过。
11. 真实 MySQL 连接信息、权限、只读 / 写入账号边界已确认。
12. 不扫描真实 NAS。
13. 不写 OpenSearch / Qdrant。
14. 不进入 DB-3 retrieval。
15. 不做 selective indexing。
16. 不触发真实 REST 动作。

## 12. 明确回答

1. 最终表名是否确定为 `external_asset_catalog`？已确认默认使用 `external_asset_catalog`；`hermes_external_asset_catalog` 仅作为命名空间备选。
2. 是否接受 `source_system` 固定为 `delivery_platform`？已确认接受，同一环境不得混用 `platform` 与 `delivery_platform`。
3. `source_view` 是否固定为 `ProjectAssetView` / `FileAssetView` / `ModelAssetView` / `AuditEventView`？已确认固定；新增 View 必须走 contract version review。
4. 是否将 View contract version 写入 mirror 表或同步 checkpoint？已确认，catalog 写 `contract_version`，checkpoint 写 `source_contract_version`。
5. 是否新增 `external_asset_sync_checkpoint` 表？已确认纳入 schema contract migration 候选表；真实创建仍需 migration 授权。
6. checkpoint rollback 记录保存在哪里？初版保存在 `external_asset_sync_checkpoint` 当前 row；完整 history 后续 DB-2.x 评估。
7. MySQL JSON 字段是否确认使用 JSON 类型，而不是 TEXT？已确认 MySQL 使用 `JSON`；PostgreSQL 等价 `JSONB`。
8. timestamp 是否统一按 UTC？已确认统一 UTC。
9. migration down 在开发 / 预生产 / 生产分别怎么处理？开发可 drop；预生产未共享可 drop、共享后 forward；生产只 forward migration。
10. DB-2 真实 migration 是否仍保持 docs-only，等待用户单独授权？已确认仍为 docs-only，必须等用户单独授权。
11. `lifecycle_status` 在平台未提供明确状态时是否默认 `ACTIVE`？已确认默认 `ACTIVE`；一次扫描缺失只写 candidate / data_quality。
12. `permission_status` 在权限字段缺失时是否强制 `DENIED`？已确认强制 `DENIED`。
13. catalog-only 是否一定不会进入 `documents` / `chunks` / Qdrant / OpenSearch？已确认一定不会。
14. Missing Evidence 的响应格式是否已在 Hermes_memory 侧定义？DB-2 已定义边界和 reason 建议 `asset_catalog_only`；最终用户可见格式属于 DB-3 retrieval / answer contract。
15. DB-3 启动条件是什么？DB-2 migration / fake fixtures / temporary DB proof / schema review 均通过后，由用户单独授权；还必须明确 permission filter、Missing Evidence、catalog-only 与 document evidence 分层，并通过 Codex review 与测试 agent 复测。

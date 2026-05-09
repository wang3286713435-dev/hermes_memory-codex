# DB-2 Schema Contract

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：真实数据库接入前 schema contract freeze；docs-only；未授权 migration

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

注意：DB-1a fake adapter 的既有 `asset_uid` 仍是 `source_system + ":" + source_id`，这是 DB-1a fake contract。真实数据库 mirror 前，DB-2 写入层必须按本合同重新生成真实 mirror `asset_uid`。

## 3. 待数据库团队确认

1. 最终表名使用 `external_asset_catalog` 还是 `hermes_external_asset_catalog`。
2. JSON 字段在目标数据库中使用 MySQL `JSON`、PostgreSQL `JSONB`，还是文本 JSON。
3. `permission_tags` / `project_scope` 是否需要在后续拆成子表，例如 `external_asset_permissions`。
4. 枚举字段是否需要数据库层 `CHECK` 约束，还是先由应用层校验。
5. JSON 内部索引是否需要；MySQL 初版不强依赖 JSON 内部索引。
6. 索引命名、长度限制和字符集 / collation。
7. timestamp 是否统一使用 UTC。
8. migration down 脚本策略：预生产允许 drop，生产只允许 forward migration。
9. 共享环境是否需要 shadow table；初版新增表不需要，后续破坏性变更再评估。

## 4. 待平台团队确认

1. `source_system` 的正式取值。
2. `source_view` 的正式枚举和 View contract version。
3. `source_id` 在同一 `source_system + source_view` 内是否稳定唯一。
4. `project_id` 是否永远是数字。如果不能保证，数据库字段必须保持 `VARCHAR(128)`。
5. `project_code` 和 `project_name` 的来源字段。
6. `AuditEventView.event_id` 是否保证单调递增。
7. event_id 是否可能乱序、补写或跨 View 共用序列。
8. 如果没有 event_id，是否可用 `created_at + source_view cursor` 兜底。
9. moved / stale / missing / deleted 的平台状态映射。
10. `source_created_at`、`source_updated_at`、`source_modified_at`、`last_seen_at` 的字段来源和时区。

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

### 资产字段

| 字段 | 类型建议 | 状态 | 说明 |
|---|---|---|---|
| `asset_kind` | `VARCHAR(64)` | 已确认 | project / file / model 等 |
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

1. 路径消失但未确认删除：标记 `MISSING`。
2. hash 相同但路径变化：标记 `MOVED`，保留 `previous_source_path`。
3. 长期未见或平台标记过期：标记 `STALE`。
4. 不物理删除 mirror 记录，除非执行受控清理任务。

状态字段：

| 字段 | 默认值 | 说明 |
|---|---|---|
| `sync_status` | `PENDING` | catalog 同步状态 |
| `index_status` | `CATALOG_ONLY` | DB-2 不写正文索引 |
| `parse_status` | `NOT_REQUESTED` | DB-2 不解析正文 |
| `semantic_index_status` | `NOT_REQUESTED` | DB-2 不写向量 |
| `citation_status` | `NOT_REQUESTED` | DB-2 不提供正文 citation |

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

PostgreSQL 可考虑 JSONB + GIN。MySQL 初版不强依赖 JSON 内部索引，项目级过滤优先使用 `project_id`、`project_code`、`permission_status`。

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
6. 推荐 checkpoint 粒度为 `source_system + source_view`。
7. 如果平台规模要求，可后续扩展为 `source_system + source_view + project_id`。

待平台团队确认：

1. `event_id` 是否保证单调递增。
2. 是否存在跨 View 乱序。
3. 无 event_id 时是否能提供 `created_at + source_view cursor`。

## 9. Schema 草案

以下是逻辑 schema 草案。具体 SQL 方言在 migration 阶段按目标数据库调整。

```sql
CREATE TABLE external_asset_catalog (
    asset_uid VARCHAR(256) PRIMARY KEY,
    source_system VARCHAR(64) NOT NULL,
    source_view VARCHAR(64) NOT NULL,
    source_id VARCHAR(128) NOT NULL,

    project_id VARCHAR(128) NULL,
    project_code VARCHAR(128) NULL,
    project_name VARCHAR(255) NULL,

    asset_kind VARCHAR(64) NULL,
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

1. DB-2 migration 只允许新增表和索引，不修改 `documents` / `chunks` / retrieval 主表。
2. 如果 migration 尚未进入生产，可允许 drop 新表。
3. 如果已进入共享环境或生产环境，不直接 drop，改为 forward migration：
   - 停止同步任务。
   - 标记 mirror 表为 deprecated。
   - 保留数据用于审计和排查。
   - 新建修正 migration。
4. DB-2 写入失败时，可以清空 `external_asset_catalog` 后重新同步，因为它只是 mirror，不是 source of truth。
5. rollback 不得影响 `documents`、`chunks`、Qdrant、OpenSearch、memory kernel 或平台 MySQL 正式资产表。

待数据库团队确认：

1. 预生产环境 migration down 是否允许 `DROP TABLE external_asset_catalog`。
2. 生产环境 down 脚本是否采用 no-op + forward migration 策略。
3. 是否需要 shadow table；初版新增表不需要，未来破坏性变更再评估。
4. checkpoint 回退记录保存在哪里。
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
3. 平台团队确认 source View、event_id、项目字段和时间字段。
4. `permission_status` 缺省 `DENIED` 写入数据库层默认值。
5. migration 只新增 `external_asset_catalog`，不改 `documents` / `chunks` / retrieval 表。
6. 写入代码先通过 fake fixtures 和 temporary DB proof。
7. Codex review 无 P0/P1/P2。
8. 测试 agent 独立复测通过。
9. 真实 MySQL 连接信息、权限、只读 / 写入账号边界已确认。
10. 不扫描真实 NAS。
11. 不写 OpenSearch / Qdrant。

## 12. 明确回答

1. 是否接受 `external_asset_catalog` 作为表名？已确认接受；`hermes_external_asset_catalog` 仅作为命名空间备选。
2. 是否接受 `asset_uid = source_system + ":" + source_view + ":" + source_id`？已确认接受；真实 mirror 使用该格式。
3. 是否接受 `UNIQUE(source_system, source_view, source_id)`？已确认接受。
4. `permission_tags` 和 `project_scope` 用 JSON、数组，还是子表？初版已确认用 JSON；是否拆子表待数据库团队确认。
5. `permission_status` 默认 `DENIED` 是否写入数据库层默认值？已确认必须写入数据库层默认值。
6. `last_event_id` 是否足够作为主 checkpoint？已确认它是主候选，但不允许作为唯一依据；需要 `created_at` overlap 兜底。
7. `event_id` 是否保证单调递增？待平台团队确认；未确认前按可能乱序处理。
8. moved / stale / missing 是否保留在 catalog 表中？已确认保留。
9. 是否需要 `previous_source_path`？已确认需要。
10. 是否同时保留 `source_created_at`、`source_updated_at`、`source_modified_at`、`last_seen_at`、`last_synced_at`？已确认保留。
11. `raw_payload` 是否允许存在？已确认允许，仅用于兼容和排查。
12. rollback 是否允许 drop 新表，还是只能 forward migration？预生产可 drop；共享或生产环境只允许 forward migration，待数据库团队最终确认。
13. 是否需要为 `project_id`、`permission_status`、`sync_status`、`last_event_id`、`lifecycle_status` 建索引？已确认需要。
14. DB-2 是否完全不触碰 `documents` / `chunks` / Qdrant / OpenSearch？已确认完全不触碰。
15. 真实数据库接入前是否仍坚持 fake fixtures + temp DB proof 先行？已确认必须先行。

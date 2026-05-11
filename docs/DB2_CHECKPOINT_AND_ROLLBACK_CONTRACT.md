# DB-2 Checkpoint And Rollback Contract

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-2 checkpoint / rollback handoff freeze；docs-only；未授权真实 migration

## 1. 定位

`external_asset_sync_checkpoint` 是 DB-2 的 migration candidate schema，只服务 Hermes mirror 同步。

它不服务：

1. 平台正式资产表。
2. NAS 文件状态。
3. `documents` / `chunks`。
4. Qdrant / OpenSearch。
5. memory kernel。
6. DB-3 retrieval。

## 2. Scope Key

默认 checkpoint 粒度：

```text
source_system + ":" + source_view
```

示例：

```text
delivery_platform:FileAssetView
```

后续规模扩大时可扩展为：

```text
source_system + ":" + source_view + ":" + project_id
```

示例：

```text
delivery_platform:FileAssetView:101
```

## 3. 最终 Schema

```sql
CREATE TABLE external_asset_sync_checkpoint (
    checkpoint_id VARCHAR(256) PRIMARY KEY,
    source_system VARCHAR(64) NOT NULL,
    source_view VARCHAR(64) NOT NULL,
    checkpoint_scope_key VARCHAR(256) NOT NULL,
    source_contract_version VARCHAR(64) NOT NULL,
    run_id VARCHAR(128) NOT NULL,

    last_event_id BIGINT NULL,
    last_synced_at TIMESTAMP NOT NULL,
    overlap_started_at TIMESTAMP NULL,

    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    last_success_at TIMESTAMP NULL,
    last_error_at TIMESTAMP NULL,
    last_error_message TEXT NULL,

    items_scanned BIGINT NOT NULL DEFAULT 0,
    items_upserted BIGINT NOT NULL DEFAULT 0,
    items_marked_missing BIGINT NOT NULL DEFAULT 0,

    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    UNIQUE KEY uk_external_asset_checkpoint_scope (
        source_system,
        source_view,
        checkpoint_scope_key
    )
);
```

MySQL 8 使用 `TIMESTAMP` 并按 UTC 写入。PostgreSQL 等价字段后续由 migration 阶段决定；DB-2 当前不扩大双数据库实现。

## 4. 字段说明

| 字段 | 说明 |
|---|---|
| `checkpoint_id` | Hermes 生成的 checkpoint row ID |
| `source_system` | 当前固定 `delivery_platform` |
| `source_view` | 四个稳定 View 之一 |
| `checkpoint_scope_key` | 默认 `source_system:source_view`，未来可加 project_id |
| `source_contract_version` | 当前 View contract version |
| `run_id` | 每次 sync run 必须生成，失败也要记录 |
| `last_event_id` | 上一个成功处理窗口的主要事件游标 |
| `last_synced_at` | 本 checkpoint 最近一次同步尝试时间 |
| `overlap_started_at` | 乱序 / 补写事件兜底窗口起点 |
| `status` | `PENDING` / `RUNNING` / `SUCCEEDED` / `FAILED` / `STALE` |
| `last_success_at` | 最近一次成功完成时间 |
| `last_error_at` | 最近一次失败时间 |
| `last_error_message` | 截断后的错误摘要，不保存敏感正文 |
| `items_scanned` | 本 run 扫描条数 |
| `items_upserted` | 本 run upsert mirror 条数 |
| `items_marked_missing` | 本 run 标记 candidate missing / missing 条数 |
| `created_at` | checkpoint row 创建时间，UTC |
| `updated_at` | checkpoint row 更新时间，UTC |

## 5. 增量同步策略

1. 首次同步按稳定 View 全量读取。
2. 成功后记录 `last_event_id`、`last_success_at`、`last_synced_at`。
3. 后续优先使用 `AuditEventView.event_id`。
4. 不假设 `event_id` 永远完整覆盖所有变化。
5. 保留 `created_at` overlap window，应对乱序、补写、跨系统导入。
6. `updated_at` / `modified_at` 只能作为辅助，不作为唯一 checkpoint。
7. 每次 run 必须幂等 upsert，重复窗口不得重复创建 catalog record。

## 6. 失败恢复

失败恢复必须满足：

1. 从上一个 `status=SUCCEEDED` 的 checkpoint 继续。
2. 重新拉取 `overlap_started_at` 之后的事件窗口。
3. 使用 `asset_uid` 和唯一约束保证幂等。
4. 新 run 写新的 `run_id`。
5. 失败时更新 `status=FAILED`、`last_error_at`、`last_error_message`。
6. 失败不得推进 `last_success_at`。

## 7. Rollback 合同

Rollback 只回滚 Hermes mirror / catalog mirror 状态：

1. 不回滚平台正式业务库。
2. 不回滚 NAS。
3. 不回滚真实文件。
4. 不回滚 `documents` / `chunks`。
5. 不回滚 Qdrant / OpenSearch。
6. 不影响 memory kernel。

环境策略：

1. 开发环境：允许 drop / rebuild `external_asset_catalog` 和 `external_asset_sync_checkpoint`。
2. 预生产：未被共享依赖时允许 drop；一旦共享使用，采用 forward migration。
3. 生产：不直接 drop，停止同步、标记 deprecated、保留数据审计、用 forward migration 修正。

Checkpoint rollback：

1. 停止同步任务。
2. 将 checkpoint 恢复到上一个成功 run 的 `last_event_id` 和 `overlap_started_at`。
3. 如果 checkpoint 不可信，清空 mirror 表并全量重建。
4. checkpoint rollback 只影响下一次同步游标，不影响 source of truth。

## 8. 重建预期

真实平台接入前，数据库团队需确认：

1. 全量重建预估耗时。
2. 平台 View 限流。
3. 是否需要分 project_id 重建。
4. 是否需要 checkpoint history 表。
5. 是否需要 shadow table。

DB-2 当前只冻结 current checkpoint 表；完整 run history 可进入 DB-2.x。

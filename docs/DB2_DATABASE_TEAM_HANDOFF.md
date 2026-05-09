# DB-2 Database Team Handoff

日期：2026-05-09
分支：`codex/data-steward-db0-contract`

## 1. 现在已经验证了什么

当前 DB-2 只做了两层安全演练：

1. fake adapter dry-run preview：读取假平台数据，生成“如果同步，会怎么处理每个资产”的清单。
2. temporary DB proof-of-contract：把这张清单写入测试创建的 SQLite 内存库，证明字段、主键、权限和状态规则可以落成表。

这两层都不是正式数据库接入：

1. 没有创建 migration。
2. 没有连接真实 MySQL。
3. 没有扫描真实 NAS。
4. 没有写 `documents` / `chunks`。
5. 没有写 OpenSearch / Qdrant。
6. 没有进入 DB-3 检索。

## 2. 给数据库团队的白话说明

我们要新增的是一张“企业资产目录表”。

它保存的是资产元数据，例如项目、文件、模型、权限标签、同步状态和最后事件号。它不保存文件正文，不保存切片，不负责搜索召回。

可以这样跟数据库团队说：

> Hermes 数据管家需要一张资产目录 mirror 表，用来保存平台侧项目 / 文件 / BIM 模型资产的稳定元数据。DB-2 阶段只同步 catalog，不写正文 evidence，不写 documents/chunks，不写向量或搜索索引。权限标签缺失时必须默认不可见。

## 3. 真实表需要数据库团队确认的点

建议先让数据库团队确认这些问题：

1. 表名是否使用 `external_asset_catalog`。
2. 主键是否使用 `asset_uid`，格式为 `source_system + ":" + source_id`。
3. 是否需要同时加唯一约束：`source_system` + `source_view` + `source_id`。
4. `permission_tags` 和 `project_scope` 用 JSON 字段、文本数组，还是单独子表。
5. `last_event_id` 是否作为增量同步 checkpoint 的主要字段。
6. `project_id`、`source_view`、`permission_status`、`sync_status`、`last_event_id` 是否需要索引。
7. `permission_tags` 缺失时，数据库默认值是否也要落成 `permission_status='denied'`。
8. moved / stale / missing 资产是否保留在表里，还是进入单独历史表。
9. 是否需要保留 `created_at`、`updated_at`、`modified_at`、`last_seen_at` 四类时间字段。
10. rollback 策略：如果 migration 失败，是否允许直接 drop 新表。

## 4. 真实数据库接入前的硬条件

进入真实数据库前必须先完成：

1. 用户明确授权 migration。
2. 数据库团队确认表结构和索引。
3. migration 只新增资产目录表，不改 `documents` / `chunks` / retrieval 表。
4. 写入代码仍使用 fake fixtures 或测试库先验证。
5. Codex B review 通过。
6. 测试 Codex 独立复测无 P0/P1/P2。

## 5. 可以发给数据库团队的材料

对接真实数据库时，建议附上：

1. `docs/DB2_ASSET_CATALOG_MIRROR_PLAN.md`
2. `docs/DB2_DATABASE_TEAM_HANDOFF.md`
3. `app/services/asset_catalog/mirror_preview.py`
4. `app/services/asset_catalog/temp_db.py`
5. `tests/test_data_steward_asset_catalog_mirror.py`
6. `tests/test_data_steward_asset_catalog_temp_db.py`

这些材料说明了字段、状态、权限默认 deny、catalog-only evidence 边界和临时库写入演练。

## 6. 仍然不能让数据库团队做的事

在用户单独授权前，不要让数据库团队：

1. 接真实平台 MySQL。
2. 扫描真实 NAS。
3. 把资产目录数据写入 `documents` / `chunks`。
4. 触发 OpenSearch / Qdrant 索引。
5. 做正文解析。
6. 做检索回答。
7. 改 memory kernel 主架构。

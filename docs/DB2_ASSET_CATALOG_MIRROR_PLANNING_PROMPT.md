# DB-2 Asset Catalog Mirror Planning Prompt

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：planning prompt / review gate，不是实现任务；baseline 禁止项已被后续用户授权的 planning / Ralph guard baseline 覆盖，implementation 禁止项仍有效

## 1. 当前基线

DB-1a fake View fixtures / fake adapter contract tests 已 baseline：

1. commit：`e9d1556`
2. tag：`phase-db1a-fake-view-adapter-baseline`
3. 当前 DB-1 能力只包括 fake JSON fixtures、只读 fake adapter、contract tests、默认关闭 feature flags 和验收文档。

DB-2 尚未开始实现。

## 2. 本 prompt 的目的

本 prompt 只用于后续 DB-2 planning。目标是让下一轮先产出 DB-2 Asset Catalog Mirror 的设计计划、review gate 和 implementation prompt 草案，而不是直接写代码。

本 prompt 不授权：

1. DB-2 mirror 实现。
2. DB migration。
3. SQLAlchemy model。
4. 真实 MySQL / NAS / REST 连接。
5. 写 `documents` / `chunks`。
6. 写 OpenSearch / Qdrant。
7. catalog retrieval。
8. selective indexing。
9. retrieval contract 或 memory kernel 主架构修改。
10. baseline。

## 3. 下一轮允许做的事

只有在用户明确说“进入 DB-2 planning”时，下一轮 Codex A 才允许做：

1. 阅读 DB-0 / DB-1 契约文档：
   - `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
   - `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
   - `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
   - `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
2. 梳理 DB-2 mirror 的最小字段。
3. 梳理 DB-2 sync preview 的输入 / 输出语义。
4. 梳理 checkpoint 策略，优先 `AuditEventView.event_id`。
5. 梳理 permission handling，特别是 `permission_tags` 缺失默认 deny。
6. 梳理 moved / stale / missing / checksum missing 的 mirror 状态语义。
7. 梳理测试计划，只能使用 fake fixtures / temporary DB / fixture DB。
8. 写一个 docs-only DB-2 planning 文档。
9. 写一个 future implementation prompt 草案，但必须明确该 prompt 尚未授权执行。

建议未来 planning 文档名称：

```text
docs/DB2_ASSET_CATALOG_MIRROR_PLAN.md
```

## 4. DB-2 Planning 必须回答的问题

下一轮 planning 文档必须回答：

1. mirror 是否需要 migration；如果需要，migration 的最小表结构是什么，何时才允许写。
2. 如果不允许 migration，如何用 temporary DB / fixture DB 做 proof-of-contract。
3. `external_asset_catalog` 或等价 mirror 的 P0 字段有哪些。
4. mirror 如何保存：
   - `asset_uid`
   - `source_system`
   - `source_id`
   - `source_view`
   - `contract_version`
   - `project_id`
   - `project_scope`
   - `permission_tags`
   - `sync_status`
   - `checksum_status`
   - `citation_status`
   - `last_event_id`
5. sync preview 如何表达：
   - `would_upsert`
   - `would_skip`
   - `would_deny`
   - `would_mark_moved`
   - `would_mark_stale`
   - `would_mark_missing`
   - `would_require_human_review`
6. `permission_tags` 缺失时如何 fail closed。
7. catalog-only 资产如何保证不进入 `documents` / `chunks`。
8. catalog-only 资产如何保证不写 OpenSearch / Qdrant。
9. DB-2 完成后如何仍不进入 DB-3 catalog retrieval。
10. 哪些检查必须由 Codex B review 后才能进入 implementation。

## 5. DB-2 Planning 输出格式

下一轮 planning 输出应包括：

1. Scope。
2. Non-goals。
3. Proposed mirror fields。
4. Sync preview contract。
5. Checkpoint policy。
6. Permission and evidence boundary。
7. Testing plan。
8. Implementation gate。
9. Hard stop conditions。
10. Future implementation prompt draft。

## 6. Review Gate

DB-2 implementation 前必须由 Codex B review 以下内容：

1. 是否仍与现有 `documents` / `chunks` 分离。
2. 是否仍不写 OpenSearch / Qdrant。
3. 是否仍不接真实 MySQL / NAS / REST。
4. 是否明确 migration 是否授权。
5. 是否明确 feature flags 默认 off。
6. 是否明确 `permission_tags` 缺失默认 deny。
7. 是否明确 catalog-only 不等于 document content evidence。
8. 是否明确 DB-2 完成后仍不自动进入 DB-3。

只有 review 通过且用户明确授权“进入 DB-2 implementation”后，才能写代码。

## 7. Hard Stop

出现以下任一情况必须停止：

1. 需要新增 migration。
2. 需要改 `app/models/**`。
3. 需要写 `documents` / `chunks`。
4. 需要写 OpenSearch / Qdrant。
5. 需要连接真实 MySQL。
6. 需要扫描真实 NAS。
7. 需要读取 `/Volumes/zyzn/卓羽智能项目`。
8. 需要接真实 REST。
9. 需要实现 catalog retrieval。
10. 需要改 retrieval contract。
11. 需要改 memory kernel 主架构。
12. 需要 baseline。

# DB-2 Asset Catalog Mirror Plan

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：dry-run sync preview 与 temporary DB proof-of-contract 已 baseline；schema review response docs-only；migration、真实平台接入和 DB-3 retrieval 未授权

## 1. Scope

DB-2 的目标是规划 Hermes_memory 自有 asset catalog mirror，用于保存平台稳定 View 的规范化 catalog metadata、checkpoint、权限占位和异常状态。DB-2 只处理 catalog mirror / sync preview 语义，不处理正文 evidence、retrieval、selective indexing 或真实平台联调。

本计划基于 DB-1a baseline：

1. commit：`e9d1556`
2. tag：`phase-db1a-fake-view-adapter-baseline`
3. 数据源：DB-1 fake `ProjectAssetView` / `FileAssetView` / `ModelAssetView` / `AuditEventView`。

DB-2 planning / implementation 结论：

1. 可以规划 `external_asset_catalog` 或等价 mirror。
2. planning 已完成 Codex B review，用户已授权进入 DB-2 最小 dry-run preview implementation。
3. migration 是否允许仍需用户显式授权。
4. 当前只允许 fake adapter 上的 catalog mirror dry-run preview、SQLite 内存库 proof-of-contract 和 docs-only schema review；不得写 migration，不得连接真实 MySQL / NAS / REST，不得写 `documents` / `chunks` / OpenSearch / Qdrant。

## 2. Non-goals

DB-2 不做：

1. 真实 MySQL 连接。
2. 真实 NAS 扫描。
3. 真实 REST / platform audit 写入。
4. 读取 `/Volumes/zyzn/卓羽智能项目`。
5. 写 `documents` / `chunks`。
6. 写 OpenSearch / Qdrant。
7. catalog retrieval。
8. selective indexing。
9. 正文解析。
10. SQLAlchemy model / Alembic migration，除非用户后续显式授权。
11. retrieval contract 修改。
12. memory kernel 主架构修改。
13. production scheduler / rollout。

## 3. Proposed Mirror Fields

DB-2 mirror 的 P0 字段应只覆盖 catalog mirror 最小闭环。字段可以映射到未来 `external_asset_catalog`，也可以先用于 temporary DB / fixture DB proof-of-contract。

| 字段 | 必需性 | 来源 | 说明 |
|---|---|---|---|
| `asset_uid` | P0 required | adapter normalized | DB-1a fake adapter 使用 `source_system + ":" + source_id`；真实 mirror schema contract 冻结为 `source_system + ":" + source_view + ":" + source_id` |
| `source_system` | P0 required | fixture / platform source | 例如 `delivery_platform` |
| `source_id` | P0 required | platform asset id | 平台 file id / model id / project id |
| `source_view` | P0 required | View name | `ProjectAssetView` / `FileAssetView` / `ModelAssetView` / `AuditEventView` |
| `contract_version` | P0 required | View contract | adapter 必须绑定并保存 |
| `project_id` | P0 required for project assets | View row | 项目边界和权限过滤依据 |
| `project_scope` | P0 required | adapter normalized | 服务级同步后的项目范围 |
| `source_path` | P0 for file/model | View row | 当前路径或平台存储路径 |
| `file_name` | P0 for file/model | View row | 文件名 |
| `file_ext` | P0 for file/model | View row | 扩展名 / 类型 |
| `file_size` | P0 for file/model | View row | 文件大小 |
| `created_at` | P0 optional | View row | 平台记录创建时间 |
| `updated_at` | P0 optional | View row | 只能作为辅助字段，不作为唯一 checkpoint |
| `permission_tags` | P0 required as list | View row / adapter | 缺失时保存为空并默认 deny |
| `permission_status` | P0 required | adapter normalized | `allowed` / `denied` |
| `permission_reason` | P0 required when denied | adapter normalized | 例如 `missing_permission_tags` |
| `sync_status` | P0 required | View row / adapter | `active` / `moved` / `stale` / `missing` |
| `checksum_status` | P0 required | adapter normalized | `present` / `missing` / `not_applicable` |
| `citation_status` | P0 required | adapter normalized | DB-2 默认 `metadata_only` |
| `index_status` | P0 optional | View row | DB-2 默认 catalog-only，不触发 indexing |
| `content_hash` | P1 optional | View row | checksum，有则保存；缺失不得复用正文 evidence |
| `modified_at` | P1 optional | View row | NAS mtime，不能单独作为变化依据 |
| `last_seen_at` | P1 optional | View row | 判断 stale / missing 的辅助字段 |
| `last_event_id` | P0 required for sync | AuditEventView | checkpoint 优先依据 |
| `last_synced_at` | P0 generated | Hermes_memory | mirror 同步时间；fixture tests 可用固定时间 |

P2 字段如 `confidentiality_level`、ACL snapshot、owner / department、version lineage、retention policy 后置，不作为 DB-2 implementation 阻塞项。

## 4. Sync Preview Contract

DB-2 首先应实现 dry-run sync preview 语义；写 DB 前必须有单独授权。

建议 preview item 字段：

| 字段 | 说明 |
|---|---|
| `asset_uid` | 目标资产 |
| `source_view` | 来源 View |
| `contract_version` | View contract version |
| `project_id` | 项目边界 |
| `action` | preview action |
| `reason` | action 原因 |
| `permission_status` | `allowed` / `denied` |
| `sync_status` | `active` / `moved` / `stale` / `missing` |
| `checksum_status` | `present` / `missing` / `not_applicable` |
| `citation_status` | 默认 `metadata_only` |
| `last_event_id` | 关联事件 |
| `writes_db` | dry-run 时固定 `false` |
| `writes_documents` | 固定 `false` |
| `writes_chunks` | 固定 `false` |
| `writes_opensearch` | 固定 `false` |
| `writes_qdrant` | 固定 `false` |

建议 preview actions：

1. `would_upsert`：active 且权限字段满足最小要求，可写入 mirror。
2. `would_skip`：重复事件、无变化、非目标 View 或不满足 scope。
3. `would_deny`：`permission_tags` 缺失、项目缺失或权限不匹配。
4. `would_mark_moved`：路径变化但 checksum 相同或 View 已标记 moved。
5. `would_mark_stale`：旧路径 / last_seen 过期 / View 已标记 stale。
6. `would_mark_missing`：View 已标记 missing 或生命周期 unavailable。
7. `would_require_human_review`：checksum 缺失、状态矛盾、路径异常或敏感目录。

Preview summary 必须包含：

1. `dry_run=true`
2. `writes_db=false`
3. `writes_documents=false`
4. `writes_chunks=false`
5. `writes_opensearch=false`
6. `writes_qdrant=false`
7. `requires_human_review_count`
8. `denied_count`
9. `last_event_id_candidate`

## 5. Checkpoint Policy

DB-2 checkpoint 规则：

1. 优先使用 `AuditEventView.event_id`。
2. `updated_at` 只能作为辅助显示字段，不作为唯一 checkpoint。
3. 如果未来只能使用 `created_at`，必须加 tie-breaker，例如 `event_id` 或 `source_id`。
4. 对乱序事件保留 overlap window，并按 `asset_uid` 幂等 upsert。
5. checkpoint 记录只属于 Hermes_memory mirror，不覆盖平台 checkpoint。
6. dry-run preview 只输出 `last_event_id_candidate`，不写 checkpoint。

DB-2 tests 至少应覆盖：

1. event id 单调递增。
2. after_event_id 过滤。
3. 重复 event id 幂等 skip。
4. moved / stale / missing 事件顺序不导致重复 indexing。

## 6. Permission And Evidence Boundary

DB-2 permission 规则：

1. `permission_tags` 缺失默认 deny。
2. `project_id` 缺失默认 deny。
3. `project_scope` 不匹配默认 deny。
4. lifecycle / sync status 不允许时不得进入 prompt-ready evidence。
5. DB-2 只保存 catalog metadata，不输出正文 evidence。

DB-2 evidence 规则：

1. mirror record 默认 `evidence_kind=asset_catalog_evidence`。
2. mirror record 默认 `citation_status=metadata_only`。
3. `content_evidence_available=false`。
4. catalog-only asset 不得写入 `documents` / `chunks`。
5. catalog-only asset 不得写入 OpenSearch / Qdrant。
6. 文件正文、条款解释、图纸内容、模型语义分析仍必须返回 Missing Evidence。
7. Missing Evidence reason 应保留或规划为 `asset_catalog_only`，但 DB-2 不实现 retrieval。

## 7. Testing Plan

DB-2 planning 后的 future implementation tests 应只使用 fake fixtures、temporary DB 或 fixture DB。

建议测试组：

1. `test_asset_catalog_mirror_preview_does_not_write_db`
   - dry-run preview summary 中所有 write flags 为 false。
2. `test_asset_catalog_mirror_preview_upsert_actions`
   - active allowed records 产生 `would_upsert`。
3. `test_asset_catalog_mirror_permission_tags_missing_deny`
   - missing permission_tags 产生 `would_deny`。
4. `test_asset_catalog_mirror_checkpoint_uses_event_id`
   - checkpoint candidate 来自最大 processed event_id。
5. `test_asset_catalog_mirror_updated_at_not_checkpoint`
   - updated_at 不作为唯一 checkpoint。
6. `test_asset_catalog_mirror_moved_stale_missing_actions`
   - moved / stale / missing 产生对应 preview action。
7. `test_asset_catalog_mirror_checksum_missing_requires_review`
   - checksum missing 产生 `would_require_human_review`。
8. `test_asset_catalog_mirror_catalog_only_never_writes_documents_or_indexes`
   - documents / chunks / OpenSearch / Qdrant write flags 固定 false。

如果未来允许 migration，必须额外测试：

1. migration 只新增 catalog mirror。
2. migration 不触碰现有 `documents` / `chunks` / retrieval tables。
3. rollback path 清晰。

## 7.1 Temporary DB Proof-of-Contract

DB-2 temporary DB proof-of-contract 只使用测试创建的 SQLite 内存库。

它验证：

1. dry-run preview 可以落成一张临时资产目录表。
2. 临时表只保存 catalog metadata，不创建 `documents` / `chunks` / index 表。
3. `asset_uid` 可以作为幂等 upsert 主键。
4. `permission_tags` 缺失导致的 `would_deny` 和 `missing_permission_tags` 可以保存。
5. `citation_status=metadata_only`、`evidence_kind=asset_catalog_evidence`、`content_evidence_available=false` 可以保存。
6. `last_event_id` 可以作为后续真实同步 checkpoint 的候选字段。

它不代表：

1. 正式数据库表已创建。
2. migration 已授权。
3. 真实 MySQL 已接入。
4. 真实 NAS 已扫描。
5. DB-3 retrieval 已开始。

## 8. Implementation Gate

DB-2 dry-run preview 第一片已满足：

1. DB-2 plan 通过 Codex B review。
2. 用户明确授权“进入 DB-2 implementation”。

DB-2 temporary DB proof-of-contract 已满足：

1. 用户明确授权只做临时数据库 proof-of-contract。
2. 用户明确禁止 migration。
3. 用户明确禁止真实 MySQL / NAS / REST。
4. 用户明确禁止进入 DB-3 retrieval。

后续任何 DB-2 extension 或 migration 前必须重新满足：

1. 用户明确是否允许 migration。
2. implementation prompt 明确白名单文件。
3. implementation prompt 明确禁止真实 MySQL / NAS / REST，除非用户另行授权真实平台联调。
4. implementation prompt 明确 tests 只用 fake fixtures / temporary DB / fixture DB，除非用户另行授权。
5. implementation prompt 明确不进入 DB-3 catalog retrieval。

推荐初次 implementation 白名单仅限：

1. `app/services/asset_catalog/**`
2. `tests/test_data_steward_asset_catalog_mirror.py`
3. 如 migration 被明确授权，才允许 `migrations/versions/**` 和相关 model 文件。

## 9. Hard Stop Conditions

出现以下任一情况必须停止：

1. 需要新增 migration，但用户尚未授权。
2. 需要改 `app/models/**`，但用户尚未授权。
3. 需要真实 MySQL / NAS / REST。
4. 需要读取 `/Volumes/zyzn/卓羽智能项目`。
5. 需要写 `documents` / `chunks`。
6. 需要写 OpenSearch / Qdrant。
7. 需要实现 catalog retrieval。
8. 需要 selective indexing。
9. 需要改 retrieval contract。
10. 需要改 memory kernel 主架构。
11. 需要 baseline。

## 10. Future Implementation Prompt Draft

以下 prompt 的 dry-run preview 部分已作为 DB-2 第一片执行；migration、DB 写入、真实平台接入和 DB-3 retrieval 仍未授权。

```text
当前分支：codex/data-steward-db0-contract。
不要 checkout，不要切分支，不要 commit，不要 baseline。

任务：实现 DB-2 Asset Catalog Mirror 的最小 dry-run sync preview。

前置条件：
1. 用户已明确授权进入 DB-2 implementation。
2. Codex B 已 review 并通过 DB2_ASSET_CATALOG_MIRROR_PLAN.md。
3. migration 是否允许已经在本 prompt 中明确。

允许范围：
1. 使用 DB-1 fake adapter / fake fixtures。
2. 实现 dry-run sync preview。
3. 输出 preview actions：would_upsert / would_skip / would_deny / would_mark_moved / would_mark_stale / would_mark_missing / would_require_human_review。
4. tests 使用 fake fixtures / temporary DB / fixture DB。

禁止范围：
1. 不连接真实 MySQL / NAS / REST。
2. 不扫描 /Volumes/zyzn/卓羽智能项目。
3. 不写 documents / chunks。
4. 不写 OpenSearch / Qdrant。
5. 不实现 catalog retrieval。
6. 不做 selective indexing。
7. 不改 retrieval contract。
8. 不改 memory kernel 主架构。
9. 不写平台 DB / audit。

验证：
1. DB-1 fake adapter tests 仍通过。
2. DB-2 mirror preview tests 通过。
3. ruff / py_compile / git diff --check 通过。
```

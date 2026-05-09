# DB-2 Fake Fixture Acceptance Cases

日期：2026-05-09
分支：`codex/data-steward-db0-contract`
状态：DB-2 fake fixture / temp DB proof acceptance contract；docs-only

## 1. 目的

这些 case 用来约束 DB-2 fake fixtures、dry-run preview 和 temporary DB proof-of-contract。

它们不是生产验收，不代表真实 MySQL、真实 NAS、真实权限系统或 DB-3 retrieval 已接入。

## 2. Acceptance Cases

| Case ID | 场景 | 输入要求 | 预期结果 |
|---|---|---|---|
| DB2-FIX-001 | 正常项目资产 | `ProjectAssetView` 含 `project_id`, `project_code`, `project_name` | 生成 `delivery_platform:ProjectAssetView:<project_id>`；不写正文索引 |
| DB2-FIX-002 | 正常文件资产 | `FileAssetView` 含 `file_id`, `project_id`, `file_name`, `storage_path` | 生成 `delivery_platform:FileAssetView:<file_id>`；`index_status=CATALOG_ONLY` |
| DB2-FIX-003 | 正常模型资产 | `ModelAssetView` 含 `model_id`, `file_id`, `model_name`, `storage_path` | 生成 `delivery_platform:ModelAssetView:<model_id>`；不解析模型 |
| DB2-FIX-004 | 审计事件资产 | `AuditEventView` 含 `event_id`, `project_id`, `created_at` | 生成 `delivery_platform:AuditEventView:<event_id>`；可作为 checkpoint 辅助 |
| DB2-FIX-005 | 缺权限字段 | 缺 `permission_tags` 或 `project_scope` | `permission_status=DENIED`；不得进入 prompt |
| DB2-FIX-006 | 缺 modified_at | 缺 `updated_at` / `last_asset_updated_at` | 使用同步时间或留空；写 `derived_metadata_source=SYNC_DERIVED` 或 data quality flag |
| DB2-FIX-007 | catalog-only 不进入 retrieval | 所有 mirror rows | `writes_documents=false`、`writes_chunks=false`、`writes_opensearch=false`、`writes_qdrant=false` |
| DB2-FIX-008 | missing candidate | 资产在同步窗口缺失但无平台删除事件 | 只写 `candidate_missing` / `data_quality_flags`；不判定真实删除 |
| DB2-FIX-009 | checkpoint 成功恢复 | 上一次成功 checkpoint 存在 | 下一次从 `last_event_id + overlap window` 继续 |
| DB2-FIX-010 | checkpoint 失败后 overlap 重跑 | run 失败且存在上一个成功 checkpoint | 不推进 `last_success_at`；新 run 使用 overlap window 重放 |
| DB2-FIX-011 | rollback catalog mirror | 清空 / 重建 mirror 表 | 不影响 source of truth、NAS、`documents`、`chunks`、Qdrant、OpenSearch |

## 3. Proof 命令边界

DB-2 proof 命令只允许使用：

1. fake fixtures。
2. temporary DB。
3. SQLite 内存库或等价测试库。

禁止：

1. 真实 MySQL。
2. 真实 NAS。
3. 真实 REST 动作。
4. 正文读取。
5. 生产 migration。
6. DB-3 retrieval。

## 4. 验收通过定义

通过条件：

1. 每个 fixture 资产都能生成稳定 `asset_uid`。
2. 重复 apply 不重复插入。
3. 权限缺失默认 `DENIED`。
4. catalog-only 不写正文 / chunk / index。
5. checkpoint 成功 / 失败恢复语义清楚。
6. rollback 只影响 mirror。
7. Codex review 无 P0/P1/P2。
8. 测试 agent 独立复测通过。

未通过条件：

1. 任意 catalog-only 资产进入 retrieval。
2. 任意缺权限资产被默认可见。
3. 任意 proof 连接真实 MySQL / NAS / REST。
4. 任意 proof 写 `documents` / `chunks` / Qdrant / OpenSearch。
5. 任意单次缺失被当成真实删除。

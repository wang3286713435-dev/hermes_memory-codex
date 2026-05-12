# DB LIMIT 30 Redacted Smoke Plan

日期：2026-05-12
状态：prompt ready, execution still requires explicit operator handoff

## 1. 目的

在 `structure_only` 已通过后，下一步候选是 `LIMIT 30` 脱敏样本 smoke。

该阶段只用于验证字段可用性、空值比例、状态分布和权限 fail-closed 风险，不用于检索、不进入 prompt、不写 mirror、不写 index。

## 2. 当前状态

测试机 v1.1 structure-only smoke 已返回 `Go`。

已新增 `docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md`，作为后续测试机执行入口。

本仓库当前未执行 `LIMIT 30`；是否让测试机执行该 prompt 仍需要用户显式交付。

## 3. 必须满足的前置条件

1. 用户明确授权。
2. 数据库团队同意脱敏输出规则。
3. structure-only 已通过。
4. 报告模板已确认不会输出 raw row。
5. 查询结果只用于统计，不保存真实样本。

## 4. 允许输出

允许输出：

1. row_count_observed：最多 30。
2. field_presence_rate。
3. null_count_by_field。
4. enum/status distribution，例如 `file_kind`、`process_status`、`model_format`、`lightweight_status`。
5. size bucket 统计，例如 `0`, `1B-1MB`, `1MB-100MB`, `100MB+`。
6. timestamp coverage，例如有无 created_at / updated_at。
7. permission field missing count。
8. lifecycle / index eligibility field missing count。

## 5. 禁止输出

禁止输出：

1. 真实项目名。
2. 真实文件名。
3. NAS 路径。
4. `asset_uid`。
5. `source_id`。
6. `project_id` 原值。
7. `file_id` / `model_id` / `event_id` 原值。
8. raw rows。
9. `summary` JSON 原文。
10. secret、token、password、API key、`.env` 真值。

## 6. 禁止动作

1. 写 DB。
2. 写 Hermes Memory DB。
3. 写 `documents` / `chunks`。
4. 写 OpenSearch / Qdrant / MinIO。
5. NAS scan。
6. migration / repair / backfill / reindex / cleanup / delete。
7. Data Steward runtime activation。
8. DB CRUD。
9. production rollout。

## 7. Go / Pause / No-Go

Go：

1. 统计可生成。
2. 无 raw row 输出。
3. 无 secret 输出。
4. 无真实业务标识输出。
5. 无写操作。

Pause：

1. 脱敏统计无法生成。
2. 字段缺失导致统计无意义。
3. 数据库团队未授权。

No-Go：

1. 输出 raw row。
2. 输出真实业务标识。
3. 输出 secret。
4. 发生写操作。

## 8. 下一步

如用户明确授权执行，把 `docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md` 交给测试机 Codex。

如果没有授权，继续停留在 planning / prompt ready 状态。

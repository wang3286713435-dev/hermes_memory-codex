# Phase 2.69 DB Structure-only Smoke Plan

日期：2026-05-11
状态：Codex A runbook / prompt planning completed

## 0. 2026-05-11 规划结果

结论：`ready_for_test_machine_structure_only_smoke`。

本轮只生成测试机侧 `structure_only` smoke runbook / prompt，不在开发机连接真实数据库，不执行 SQL，不读取真实行，不写 DB/index。

新增测试机执行入口：

1. `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`

该 prompt 明确：

1. 只允许 `SELECT 1`、`SELECT DATABASE()`、`SHOW FULL TABLES WHERE Table_type = 'VIEW'`、四个 `SHOW COLUMNS` 与四个 `WHERE 1 = 0` 空结构查询。
2. 禁止 `LIMIT 1`、`LIMIT 30`、`COUNT(*)` over business rows 或任何真实样本读取。
3. 禁止输出 secret、真实项目名、文件名、NAS 路径、`asset_uid`、`source_id`、raw row 或 SQL stderr。
4. 无 host / port / database / readonly credential 安全注入时必须 `Pause`。
5. 报告仅允许输出 schema / View / field summary 与 Go / Pause / No-Go。
6. 本阶段不授权 DB CRUD、migration、mirror write、NAS scan、OpenSearch / Qdrant 写入或 production rollout。

## 1. 背景

Phase 2.68 Data Steward DB Branch Intake / Merge Readiness Review 已完成，结论为 `ready_for_mainline_acceptance`。

用户已确认当前数据库团队口径：

1. 测试机真实 `host` / `port` 尚未在项目文档中提供，不能编造。
2. 本地 dev database 名称为 `delivery_platform`，端口默认 `3306`；测试机真实连接信息必须通过安全渠道提供。
3. 只读账号或 API key 不得通过聊天、Markdown、Git、截图明文传递。
4. 四个 View / REST contract 当前仍按 `delivery_platform.asset_views.v1`。
5. 仅授权 `structure_only` 检查。
6. 明确禁止输出真实项目名、文件名、NAS 路径或 raw row。

## 2. 本阶段定位

Phase 2.69 不是测试机真实连库执行阶段，而是为测试机侧 `structure_only` smoke 准备最小 runbook / prompt / acceptance criteria。

本阶段可以把“允许执行的 SQL 形状”和“禁止输出的内容”固化为文档，但不得在开发机连接真实数据库。

## 3. 允许的 structure-only 检查

测试机侧未来只允许执行以下结构握手语义：

```sql
SELECT 1;
SELECT DATABASE();
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SHOW COLUMNS FROM ProjectAssetView;
SHOW COLUMNS FROM FileAssetView;
SHOW COLUMNS FROM ModelAssetView;
SHOW COLUMNS FROM AuditEventView;
SELECT * FROM ProjectAssetView WHERE 1 = 0;
SELECT * FROM FileAssetView WHERE 1 = 0;
SELECT * FROM ModelAssetView WHERE 1 = 0;
SELECT * FROM AuditEventView WHERE 1 = 0;
```

执行者必须只记录：

1. 连接是否成功。
2. 当前 database 名称是否为预期库。
3. 四个 View 是否存在。
4. 四个 View 的字段名 / 类型 / nullable / key / default / extra。
5. `WHERE 1 = 0` 是否能返回空结构。
6. 是否有权限错误。
7. 是否有 contract mismatch。

## 4. 明确禁止

本阶段和测试机 `structure_only` smoke 均禁止：

1. `SELECT * FROM ... LIMIT 1 / LIMIT 30` 或任何真实行读取。
2. 输出真实项目名、文件名、NAS 路径、`asset_uid`、`source_id`、raw row。
3. 扫描 NAS。
4. 写平台 DB。
5. 写 Hermes Memory DB。
6. 写 `documents` / `chunks`。
7. 写 OpenSearch / Qdrant / MinIO。
8. 执行 migration。
9. 启用 Data Steward runtime features。
10. Agent 直接执行 DB CRUD。
11. production rollout。

## 5. 安全凭证交接

连接信息和凭证只能通过以下方式之一提供：

1. 企业密码库。
2. 密钥管理系统。
3. 一次性密钥链接。
4. 测试机本地受控 `.env` 注入。
5. CI/CD Secret。
6. 运维在测试机本地配置。

不得通过聊天、Markdown、Git、截图、日志或报告输出 secret。

报告中只能写：

1. key 是否存在。
2. host / port 是否已配置。
3. database 是否已配置。
4. 不输出真实 password / token / API key。

## 6. Go / Pause / No-Go

Go 条件：

1. 安全配置中存在 host / port / database / readonly credential。
2. `SELECT 1` 成功。
3. `SELECT DATABASE()` 返回预期库。
4. 四个 View 存在。
5. 四个 View 字段可读取。
6. `WHERE 1 = 0` 成功返回空结构。
7. 报告没有真实业务数据。

Pause 条件：

1. host / port / database 未配置。
2. 凭证未安全注入。
3. View 名称不匹配。
4. contract version 无法确认。
5. 只读权限不足以做结构检查。

No-Go 条件：

1. 必须读取真实样本才能继续。
2. 必须写 DB / migration / mirror / index 才能继续。
3. 输出了真实项目名、文件名、NAS 路径、raw row 或 secret。
4. 需要 Agent 直接增删改查平台数据库。

## 7. 数据库团队待确认

进入测试机真实执行前，还需要数据库团队 / 运维通过安全渠道提供或确认：

1. 测试机可访问的 DB host / port。
2. database 名称。
3. 只读账号或 API key 的安全注入方式。
4. 四个 View 是否在目标库中暴露：
   - `ProjectAssetView`
   - `FileAssetView`
   - `ModelAssetView`
   - `AuditEventView`
5. contract 是否仍为 `delivery_platform.asset_views.v1`。
6. 是否允许执行上文列出的 `structure_only` SQL。

## 8. 下一步

Codex B 审核 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`。审核通过后，由用户决定是否把 prompt 交给测试机 Codex 执行真实 `structure_only` smoke。

测试机执行前仍需数据库团队 / 运维通过安全渠道提供 host / port / database / readonly credential；不得要求 secret 明文。

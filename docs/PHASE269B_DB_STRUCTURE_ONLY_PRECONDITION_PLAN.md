# Phase 2.69b DB Structure-only Precondition Plan

日期：2026-05-11
状态：Codex A precondition prompt planning completed

## 0. 2026-05-11 规划结果

结论：`ready_for_test_machine_precondition_check`。

本轮新增测试机前置条件检查入口：

1. `docs/CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md`

该 prompt 用于测试机 Codex / operator 在不连接 DB、不执行 SQL、不安装工具的前提下确认：

1. Hermes_memory 安装路径 / HEAD / tag / dirty 状态。
2. DB host / port / database / readonly credential key names 是否存在。
3. secret 是否通过安全渠道注入，但不输出值。
4. MySQL client 或 Hermes readonly tooling 是否存在。
5. 前置条件不足时继续 `Pause`，不得自动重跑 DB smoke。

## 1. 背景

测试机侧执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md` 后返回 `Pause`：

1. 未确认当前环境的 Hermes_memory install / version。
2. checked secure environment keys 中未发现 DB host / port / database / readonly credential。
3. direct mysql client 不可用。
4. 未连接 DB，未执行 SQL，未读取真实行，未输出 secret 或真实业务数据。

该结果符合 Phase 2.69 的安全边界：前置条件不足时必须 Pause，而不是尝试猜测 host、打印 secret 或读取真实数据。

## 2. 当前结论

Phase 2.69 structure-only prompt 安全有效；阻塞点是测试机环境准备不足，不是 Hermes 主线代码问题。

下一步不应扩大到 `LIMIT 30`、mirror、DB CRUD、NAS scan 或 indexing，而应先补齐测试机 structure-only 前置条件。

## 3. Phase 2.69b 目标

Phase 2.69b 只做测试机前置条件补齐 runbook / prompt：

1. 确认测试机 Hermes_memory 安装路径与版本。
2. 确认 secure env key names 存在，但不打印值。
3. 确认 DB host / port / database 已配置。
4. 确认 readonly credential 已通过安全渠道注入。
5. 确认有可执行 structure-only SQL 的工具路径：
   - 优先 Hermes_memory 既有 readonly tooling。
   - 其次 direct MySQL client。
   - 如二者均无，Pause 并要求 operator 安装或指定工具。
6. 不执行真实 SQL，除非后续重新授权 `structure_only` smoke。

## 4. 需要数据库团队 / 运维配合

在测试机本地通过安全渠道提供：

1. DB host。
2. DB port。
3. database name。
4. readonly username / API key 标识。
5. readonly credential secret。
6. contract version：`delivery_platform.asset_views.v1`。
7. 可用连接方式：MySQL CLI、Python client、平台 REST，或 Hermes readonly smoke runner。

不得通过聊天、Markdown、Git、截图或日志明文传递 credential。

## 5. 允许检查

允许测试机 Codex / operator 检查：

1. 目录是否存在。
2. Git HEAD / tag / dirty 状态。
3. env key names 是否存在。
4. `mysql --version` 或等价 client 是否存在。
5. Hermes_memory 内是否已有 readonly smoke runner。
6. Docker / API / CLI 是否按需可用。

## 6. 禁止事项

仍禁止：

1. 连接 DB。
2. 执行 SQL。
3. 读取真实行。
4. 输出 secret / `.env` 真值。
5. 输出真实项目名、文件名、NAS 路径、raw row。
6. 扫描 NAS。
7. 写任何 DB / index / object storage。
8. migration / repair / backfill / reindex / cleanup / delete。
9. DB CRUD。
10. production rollout。

## 7. Go / Pause / No-Go

Go 条件：

1. Hermes_memory install / version 已确认。
2. DB host / port / database / readonly credential key names 已确认存在。
3. credential 通过安全渠道注入，未被打印。
4. 可用 SQL 执行工具已确认。
5. operator 确认下一步可重新运行 `structure_only` smoke。

Pause 条件：

1. 任一 key 缺失。
2. credential 未注入。
3. 工具缺失。
4. Hermes_memory 版本不明。

No-Go 条件：

1. secret 被打印。
2. 真实业务数据被输出。
3. 未授权执行 SQL 或读取真实行。
4. 发生写操作。

## 8. 下一步

若 Phase 2.69b 前置条件 Go，再重新执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`。

若仍 Pause，则回传缺失项，不要扩大范围。

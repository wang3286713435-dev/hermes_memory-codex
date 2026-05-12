# DB Team Direct Handoff Protocol

日期：2026-05-11
状态：active protocol

## 1. 背景

用户已确认：后续 DB / Data Steward 测试机 prompt、前置条件检查、数据库团队配合项，不再经由主线 Codex A 生成。

Codex B 可以直接与用户 / 数据库团队 / 测试机 Codex 对接，编写或审核 DB 相关 prompt，并根据测试机回传结果规划下一步。

## 2. 职责调整

### Codex B

负责：

1. 直接编写 DB / Data Steward 测试机 prompt。
2. 直接审核测试机 sanitized report。
3. 直接向用户列出数据库团队需要提供的最小信息。
4. 直接维护 DB 接入相关协议 / runbook / handoff docs。
5. 继续把 DB 接入控制在低耦合、只读优先、feature-flagged、contract-tested 的路线内。

### Codex A

仍负责：

1. 主线功能实现。
2. 主线 docs / runner / tests。
3. 非 DB 测试机 prompt 的常规文件化执行。

但 DB / Data Steward 测试机 prompt 不再要求 Codex A 先生成。

### 测试机 Codex

负责：

1. 按 Codex B 审核通过的 prompt 执行测试机侧 precondition / smoke。
2. 只回传 sanitized report。
3. 不自行扩大到样本读取、写入、NAS scan、CRUD、migration、indexing 或 rollout。

## 3. 当前适用范围

适用于：

1. DB structure-only precondition check。
2. DB structure-only smoke。
3. 后续如获授权的脱敏 sample smoke。
4. Data Steward / DB / NAS 相关测试机对接 runbook。

不适用于：

1. 常规 Hermes_memory 主线功能开发。
2. Mac mini 内部 MVP 文件问答试用。
3. production rollout。

## 4. 不变安全边界

即使改为 Codex B 直接对接，仍禁止：

1. 未授权连接真实 DB。
2. 未授权执行 SQL。
3. 未授权读取真实行。
4. 输出 secret、token、password、API key、`.env` 真值。
5. 输出真实项目名、文件名、NAS 路径、raw row。
6. 扫描 NAS。
7. 写平台 DB / Hermes Memory DB。
8. 写 `documents` / `chunks` / OpenSearch / Qdrant / MinIO。
9. 启用 Data Steward runtime features。
10. DB CRUD。
11. migration / repair / backfill / reindex / cleanup / delete。
12. production rollout。

## 5. 当前执行结论

Phase 2.69b 的 `docs/CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md` 已存在，并可由 Codex B 直接交付给测试机 Codex。

后续若测试机 precondition 返回 `Go`，Codex B 可直接审核并决定是否向用户建议重新执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`。

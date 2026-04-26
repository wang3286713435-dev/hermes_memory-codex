# Nightly Sprint Queue

## 使用规则

1. Codex A 只能执行本队列中的 bounded item。
2. 每晚最多执行 1-3 个 item。
3. 遇到 Yellow Lane 完成后必须停止等待 Codex B。
4. 遇到 Red Lane 或硬停止条件必须停止。
5. 每个 item 完成后必须更新 ACTIVE_PHASE、HANDOFF_LOG、latest.json 与 nightly run JSON。

## Queue

### 1. Phase 2.27b audit preview / dry-run 最小实现

- 类型：Green Lane
- 目标：读取 review record，输出 sanitized audit payload preview。
- 输入：`docs/NEXT_CODEX_A_PROMPT.md` 中的 Phase 2.27b 任务。
- 允许：
  - 新增 preview / dry-run 脚本。
  - 新增单元测试。
  - 临时目录 smoke。
  - 文档与交接文件同步。
- 禁止：
  - 写 `audit_logs`。
  - 写业务 DB。
  - 执行 repair。
  - 修改 facts / document_versions / OpenSearch / Qdrant。
  - 进入 rollout。
- 完成后：停止并等待 Codex B 审核是否 baseline。

### 2. Phase 2.27b Git baseline

- 类型：Yellow Lane
- 条件：Codex B 审核通过后才执行。
- 默认：不自动执行。
- 目标：提交 Phase 2.27b audit preview / dry-run 相关文件并打 tag。
- 禁止：
  - 混入无关 dirty。
  - 写业务 DB。
  - 执行 repair。
  - 自动进入下一 phase。

### 3. Phase 2.27c route planning

- 类型：Green Lane
- 目标：规划是否真实写 `audit_logs`。
- 允许：
  - 规划文档。
  - TODO / DEV_LOG / ACTIVE / HANDOFF / latest 同步。
- 禁止：
  - 直接实现 DB 写入。
  - 修改 `audit_logs`。
  - 执行 repair。
  - 进入 rollout。

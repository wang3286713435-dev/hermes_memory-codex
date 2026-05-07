# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。

Phase 2.51 Mac Mini Internal MVP Operator / Hot Update Runbook baseline 已完成后，下一轮只允许做路线规划，不允许直接进入实现、真实 Mac Mini deployment、repair、rollout 或 Data Steward。

## 本轮目标

Phase 2.51 post-baseline route planning。

评审下一步是否进入以下候选之一：

1. Phase 2.51a fake deployment record dry-run smoke。
2. Phase 2.51b minimal operator command sheet。
3. Phase 2.50b evidence pack planning。

## 背景

Phase 2.51 runbook 已固化：

1. Mac Mini 是 internal controlled MVP 运行机，不是 production rollout / 客户交付 / 自动审标 / 自动经营决策环境。
2. Mac Mini operator 只能拉取 reviewed baseline commit / tag。
3. hot update 前必须记录 current ref，失败时回滚 previous known-good tag。
4. canonical run record 是 `reports/internal_mvp_runs/<YYYYMMDD>_<session>.json`。
5. Markdown notes 只能作为 optional human notes，不得作为 Phase 2.49 bridge 的 `--input-run-record`。

## 规划候选

### A. Phase 2.51a fake deployment record dry-run smoke

目标：用 fake deployment / hot update record 验证 runbook 记录、review bridge 与 ignored report 策略是否顺畅。

边界：

- 只用 fake / temp 数据。
- 不读取真实 Mac Mini reports。
- 不执行真实 deployment。
- 不写 DB / OpenSearch / Qdrant。

### B. Phase 2.51b minimal operator command sheet

目标：把 runbook 中的命令提炼成一页可执行 command sheet，降低 operator 操作成本。

边界：

- docs-only。
- 不新增 deployment script。
- 不创建 cron / scheduler。
- 不执行真实命令。

### C. Phase 2.50b evidence pack planning

目标：规划 internal MVP daily review evidence pack 的目录、命名、人工复核字段与 Go / Pause / No-Go 证据挂接方式。

边界：

- planning-only。
- 不扫描真实 reports。
- 不上传证据。
- 不进入 rollout。

## 硬禁止

1. 不执行真实 Mac Mini deployment。
2. 不拉取远端或切换 tag。
3. 不启动 / 停止服务。
4. 不运行 API / CLI smoke，除非后续单独 prompt 明确授权。
5. 不读取真实 reports / run records。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete / migration。
8. 不进入 production rollout。
9. 不进入 Data Steward / BIM 实现。
10. 不修改 retrieval contract。
11. 不修改 memory kernel 主架构。

## 输出要求

只做规划与文档同步，不提交 Git。

返回：

1. 修改文件。
2. 路线评审结论。
3. 推荐下一步。
4. 最小边界。
5. 非目标。
6. 是否建议开始实现。

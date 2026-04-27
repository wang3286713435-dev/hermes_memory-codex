# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 当前状态

Phase 2.27f Review Audit Linkage Route Planning 已完成并进入 baseline。

当前 baseline 内容：

1. 新增 `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`。
2. 规划 archive / review / audit 三者只读关联诊断。
3. 推荐后续最小实现：只读 linkage summary。
4. 推荐使用 `report_hash` / `report_type` 关联 archived report 与 review record。
5. 推荐使用 `review_id` / `trace_id=report_review:<review_id>` 关联 review record 与 report-level audit event。
6. 缺少 archive / review / audit 任一环节时输出 warning，不自动 fail。
7. item-level / repair-level linkage、repair executor、真实 DB 写入与 rollout 继续后置。

## 下一步

本文件当前不是实现任务。

Codex A 下一步应等待 Codex B 审核 Phase 2.27f planning baseline。

如果用户要求执行本文件，Codex A 只应：

1. 读取 `AGENT_OPERATING_PROTOCOL.md`、`ACTIVE_PHASE.md`、`PHASE_BACKLOG.md`。
2. 报告 Phase 2.27f planning baseline 已完成，等待 Codex B review / 最小实现 prompt。
3. 不写功能代码。
4. 不提交 Git。
5. 不进入 Phase 2.27f 实现。

## 硬边界

1. 不写 `audit_logs`。
2. 不写业务 DB。
3. 不修改 facts。
4. 不修改 document_versions。
5. 不修改 OpenSearch。
6. 不修改 Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete。
8. 不进入 rollout。
9. 不改 retrieval contract。
10. 不改 memory kernel 主架构。
11. 不做 item-level audit summary。
12. 不把 audit event 当作 repair executed。

## Codex B 需处理

Codex B 应读取：

1. `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/HANDOFF_LOG.md`
4. `reports/agent_runs/latest.json`

然后决定：

1. 是否授权 Phase 2.27f 最小实现。
2. 是否继续后置 archive / review / audit 关联诊断。

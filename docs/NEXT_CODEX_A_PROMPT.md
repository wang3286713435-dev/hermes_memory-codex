# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。执行前必须先读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
5. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
6. `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
7. `/Users/Weishengsu/Hermes_memory/docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`

## 当前状态

Phase 2.38c Personnel Requirement Recall Tail Planning 已完成 Codex B review，并由本轮执行 docs-only Git baseline。

本文件当前不再作为新的实现任务入口。

## 下一轮建议

等待 Codex B 检查 Phase 2.38c baseline。

Codex B 如决定继续推进，应另行写入 Phase 2.38d personnel-only bounded implementation prompt。

## 硬边界

1. 不自动进入 Phase 2.38d。
2. 不修 retrieval ranking。
3. 不改 retrieval contract。
4. 不改 memory kernel 主架构。
5. 不写业务 DB。
6. 不修改 facts。
7. 不修改 document_versions。
8. 不修改 OpenSearch。
9. 不修改 Qdrant。
10. 不执行 repair / backfill / reindex / cleanup / delete。
11. 不进入 rollout。
12. 不自动审标。
13. 不把 `price_ceiling` 或 `project_manager_level` 当作可修复字段。

## 后续执行方式

如果用户再次要求执行本文件，Codex A 应先检查 `docs/ACTIVE_PHASE.md` 与 `docs/PHASE_BACKLOG.md`，确认 Codex B 是否已写入新的 Phase 2.38d 或其他阶段任务。

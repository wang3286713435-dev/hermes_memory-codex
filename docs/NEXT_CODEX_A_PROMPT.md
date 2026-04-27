# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.27g linkage readiness route planning 收口与 Git baseline。

只做 Git baseline，不写功能代码，不改 readiness runner，不写 DB，不写 `audit_logs`。

## 当前状态

Phase 2.27g 已完成路线规划：

1. 推荐 B + D：
   - 后续如需代码衔接，只做显式参数化读取 linkage summary。
   - Phase 2.29 MVP readiness freeze 中把 linkage summary 纳入人工验收项。
2. 不推荐默认扫描真实 `reports/` / `reviews/` / audit records。
3. 不推荐继续追加新的 Phase 2.27x 实现。
4. repair executor、rollout、真实 DB 写入、item-level linkage 继续后置。

## Baseline 执行步骤

1. 读取并遵守：
   - `docs/AGENT_OPERATING_PROTOCOL.md`
   - `docs/ACTIVE_PHASE.md`
   - `docs/PHASE_BACKLOG.md`
2. 本轮为 planning baseline，不运行 pytest。
3. 执行状态复核：
   ```bash
   git status --short
   git check-ignore -v reports/agent_runs/latest.json
   ```
4. 确认 staged 前 dirty 仅包含 Phase 2.27g 相关文件：
   - `docs/PHASE227G_LINKAGE_READINESS_ROUTE_PLAN.md`
   - `docs/TODO.md`
   - `docs/DEV_LOG.md`
   - `docs/ACTIVE_PHASE.md`
   - `docs/HANDOFF_LOG.md`
   - `docs/PHASE_BACKLOG.md`
   - `docs/NEXT_CODEX_A_PROMPT.md`
5. 仅 stage 上述 7 个文件。
6. 提交：
   - commit message：`docs: plan phase 2.27g linkage readiness route`
7. 打 tag：
   - `phase-2.27g-linkage-readiness-route-baseline`
8. 推送：
   - `git push origin main`
   - `git push origin phase-2.27g-linkage-readiness-route-baseline`
9. 更新 ignored 本地状态：
   - `reports/agent_runs/latest.json`
   - status 写为 `baseline`
   - 记录 commit、tag、pushed=true
   - 下一步建议写为 Phase 2.29 MVP readiness freeze planning。
10. 完成后停止，不进入 Phase 2.29 实现。

## Acceptance Criteria

1. 最终 `git status --short` 干净。
2. commit 只包含 Phase 2.27g planning 文档与交接文件。
3. tag 指向当前 HEAD。
4. `origin/main` 与本地 HEAD 对齐。
5. 未提交 `reports/agent_runs/latest.json`。
6. 未写功能代码。
7. 未写 DB / `audit_logs`。

## 硬边界

1. 不写功能代码。
2. 不修改 `scripts/phase225_readiness_audit.py`。
3. 不修改 `scripts/phase227f_review_audit_linkage.py`。
4. 不写 `audit_logs`。
5. 不写业务 DB。
6. 不修改 facts。
7. 不修改 document_versions。
8. 不修改 OpenSearch / Qdrant。
9. 不读取真实 reports / reviews 业务内容。
10. 不默认扫描本机 reports / reviews 目录。
11. 不执行 repair / backfill / reindex / cleanup / delete。
12. 不进入 rollout。
13. 不进入 repair executor。
14. 不进入 Phase 2.29 实现。

## 完成后汇报格式

请返回精简报告：

1. 修改文件。
2. 测试与验证结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 git status。
7. 是否建议进入 Phase 2.29。

下一步候选应是：

**Phase 2.29 MVP readiness freeze planning。**

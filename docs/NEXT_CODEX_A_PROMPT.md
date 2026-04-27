# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 本轮目标

Phase 2.27f archive / review / audit 只读 linkage summary 收口与 Git baseline。

只做 Git baseline，不写功能代码，不执行 repair，不写 DB，不写 `audit_logs`。

## 当前状态

Codex B 已审核 Phase 2.27f 最小实现与安全补丁：

1. `scripts/phase227f_review_audit_linkage.py` 已新增只读 linkage summary runner。
2. `tests/test_phase227f_review_audit_linkage.py` 已覆盖 12 条测试。
3. 顶层 audit event unsafe 字段漏口已关闭：
   - `document_id`：fail。
   - `fact_id`：fail。
   - `report_path` / 本机绝对路径：fail。
4. Codex B 复跑通过：
   - `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py`
   - `uv run pytest tests/test_phase227f_review_audit_linkage.py -q`，12 passed。

## Baseline 执行步骤

1. 读取并遵守：
   - `docs/AGENT_OPERATING_PROTOCOL.md`
   - `docs/ACTIVE_PHASE.md`
   - `docs/PHASE_BACKLOG.md`
2. 复跑轻量验证：
   ```bash
   uv run python -m py_compile scripts/phase227f_review_audit_linkage.py
   uv run pytest tests/test_phase227f_review_audit_linkage.py -q
   ```
3. 执行状态复核：
   ```bash
   git status --short
   git check-ignore -v reports/agent_runs/latest.json
   ```
4. 确认 staged 前 dirty 仅包含 Phase 2.27f 相关文件：
   - `scripts/phase227f_review_audit_linkage.py`
   - `tests/test_phase227f_review_audit_linkage.py`
   - `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
   - `docs/TODO.md`
   - `docs/DEV_LOG.md`
   - `docs/ACTIVE_PHASE.md`
   - `docs/HANDOFF_LOG.md`
   - `docs/PHASE_BACKLOG.md`
   - `docs/NEXT_CODEX_A_PROMPT.md`
5. 仅 stage 上述 9 个文件。
6. 提交：
   - commit message：`chore: add phase 2.27f review audit linkage`
7. 打 tag：
   - `phase-2.27f-review-audit-linkage-baseline`
8. 推送：
   - `git push origin main`
   - `git push origin phase-2.27f-review-audit-linkage-baseline`
9. 更新 ignored 本地状态：
   - `reports/agent_runs/latest.json`
   - status 写为 `baseline`
   - 记录 commit、tag、pushed=true
   - 下一步建议写为 Phase 2.27g route planning：是否将 linkage summary 显式参数化接入 readiness audit，或继续后置。
10. 完成后停止，不进入下一阶段实现。

## Acceptance Criteria

1. 最终 `git status --short` 干净。
2. commit 只包含 Phase 2.27f runner、测试、文档与交接文件。
3. tag 指向当前 HEAD。
4. `origin/main` 与本地 HEAD 对齐。
5. 未提交 `reports/agent_runs/latest.json`。
6. 未生成真实 reports / reviews / audit payload 产物。
7. 未写 DB / `audit_logs`。

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
13. 不进入 Phase 2.27g 实现。

## 完成后汇报格式

请返回精简报告：

1. 修改文件。
2. 测试结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 git status。
7. 当前风险 / 后续建议。

下一步候选应是：

**Phase 2.27g 路线规划：linkage summary 是否显式参数化接入 readiness audit。**

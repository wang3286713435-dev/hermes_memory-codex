# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.50 runbook artifact review，结论：通过；现在授权执行 docs-only Git baseline。

## 本轮目标

Phase 2.50 Internal MVP Daily Review Loop Runbook Artifact Git baseline。

只提交 Phase 2.50 runbook、交接文档和状态文档。不要进入 Phase 2.50a、Phase 2.51、真实 MVP Pilot、repair、rollout 或 Data Steward 实现。

## Codex B Review 结论

通过。

已确认：

1. `docs/PHASE250_INTERNAL_MVP_DAILY_REVIEW_LOOP_PLAN.md` 明确这是 internal controlled MVP daily review loop，不是 production rollout。
2. operator 输入来自 `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md`，真实 run records 保存在 ignored `reports/internal_mvp_runs/`。
3. 命令模板使用显式 `--input-run-record` placeholder，不默认扫描 `reports/`。
4. `decision_hint=go/pause/no_go` 解释清楚，`go` 没有被写成 rollout approval。
5. issue intake 映射覆盖 facts/transcript/snapshot as answer、第三文件污染、隐藏 Missing Evidence、alias/session blocker。
6. 人工责任边界覆盖投标、合同、采购、经营、客户沟通与 Data Steward。
7. 存储和隐私策略明确真实 run record / review report 不入 Git。
8. stop conditions 足够明确。
9. Nightly Sprint 边界禁止真实 Pilot、读取真实 records、写 DB / index、自动 baseline。
10. 后续候选保持为 fake smoke / evidence pack / Mac Mini operator checklist，不进入 repair 或 rollout。

## Baseline 白名单

只允许 stage / commit 以下文件：

1. `docs/PHASE250_INTERNAL_MVP_DAILY_REVIEW_LOOP_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不要 stage `reports/agent_runs/latest.json`。

## 必须排除

以下文件属于 out-of-scope dirty 或本地状态，必须保持排除：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`（ignored）

## 必跑验证

```bash
cd /Users/Weishengsu/Hermes_memory
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
```

不要运行 pytest。
不要运行 API / CLI smoke。
不要启动 / 停止服务。
不要读取真实 internal MVP run records。
不要写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。

## Git baseline

1. 只 stage 白名单 8 个文件。
2. commit message：`docs: add phase 2.50 internal mvp daily review loop`
3. tag：`phase-2.50-internal-mvp-daily-review-loop-baseline`
4. push `origin/main`。
5. push tag 到 `origin`。

## Baseline 后更新 ignored 状态

更新 `reports/agent_runs/latest.json`：

1. `phase=Phase 2.50 Internal MVP Daily Review Loop Runbook Artifact Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push result。
4. 记录验证结果。
5. `needs_codex_b_review=false`
6. `needs_codex_c_validation=false`

`latest.json` 必须保持 ignored，不得 stage。

## 硬禁止

1. 不进入 Phase 2.50a。
2. 不进入 Phase 2.51。
3. 不新增功能代码、scripts 或测试。
4. 不读取真实 reports / run records。
5. 不默认扫描 `reports/`。
6. 不运行 API / CLI smoke。
7. 不启动 / 停止服务。
8. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
9. 不执行 repair / backfill / reindex / cleanup / delete。
10. 不进入 production rollout。
11. 不进入 Data Steward / BIM 实现。
12. 不修改 retrieval contract。
13. 不修改 memory kernel 主架构。
14. 不 stage / commit out-of-scope dirty。

## 完成后输出

1. commit hash。
2. tag。
3. push 结果。
4. 验证结果。
5. final git status。
6. out-of-scope dirty 是否仍保留。
7. 是否建议进入 Phase 2.50a 或 Phase 2.51 planning。

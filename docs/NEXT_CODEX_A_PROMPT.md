# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。请严格按文件化交接机制执行；本轮只做 Phase 2.44c fake-data sanitized issue intake dry-run artifact 的 docs-only Git baseline。

本轮不写新规划、不写功能代码、不进入 Phase 2.44d、不生成真实 issue records、不生成真实 Pilot report、不扫描真实 `reports/`、不运行 API / CLI、不写 DB / facts / document_versions / OpenSearch / Qdrant、不进入 production rollout、不 repair、不 backfill、不 reindex、不 cleanup、不 delete、不做 Data Steward 实现。

## 必读文件

执行前必须读取：

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_DAY1_FAKE_ISSUE_DRY_RUN.md`
8. `/Users/Weishengsu/Hermes_memory/docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json`
9. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

## Baseline 依据

Phase 2.44c 已满足 baseline gate：

1. 当前 phase 有明确验收结果：fake-data sanitized issue intake dry-run artifact 已完成。
2. Codex B review 已通过：fake input 只含 placeholder aliases、document_ids、version_ids、citations、source locations 与 sanitized behavior，不含真实 raw answer / session / customer / amount / tender judgment。
3. 目标检查已通过：
   - `git diff --check`
   - `uv run python -m json.tool docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json`
   - `uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json --strict`
   - `uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json`
   - `uv run python -m json.tool reports/agent_runs/latest.json`
   - `git check-ignore -v reports/agent_runs/latest.json`
4. fake dry-run summary：`total=2`，`valid_records=2`，`invalid_count=0`，`by_issue_type.retrieval_recall=1`，`by_issue_type.trace_ux=1`，`by_priority.P1=2`，`go_pause_recommendation=continue_with_manual_review`。
5. 下一步将切换到 Phase 2.44d 候选或继续内部 Pilot issue intake，因此应先 baseline Phase 2.44c。

## 当前保留风险

这些是已知 Pilot 尾项，不是本轮 baseline 阻塞：

1. P1 `retrieval_recall`：`@主标书` 最高投标限价 / 招标控制价 / 投标报价上限仍为 Missing Evidence。
2. P1 `manual_review_required`：`@主标书` 资质 / 项目经理 / 联合体 / 业绩 / 人员等深层字段仍需人工复核。
3. P1 `structured_citation_ux`：Excel 硬件清单 cell citation 部分降级为 row / range。
4. P1/P2 `strategy_human_review`：公司未来方向分析仍需人工决策，部分风险 / 行业判断需人工复核。
5. P2 `trace_display_ux`：会议风险解释 / strategy trace 展示仍需 polish。
6. `continue_with_manual_review` 不是 rollout approval，不是 repair authorization。

这些尾项不得在本轮顺手修。

## Git baseline 范围

工作目录：`/Users/Weishengsu/Hermes_memory`

只允许 stage / commit 以下文件：

1. `docs/MVP_PILOT_DAY1_FAKE_ISSUE_DRY_RUN.md`
2. `docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json`
3. `docs/ACTIVE_PHASE.md`
4. `docs/PHASE_BACKLOG.md`
5. `docs/HANDOFF_LOG.md`
6. `docs/NIGHTLY_SPRINT_QUEUE.md`
7. `docs/NEXT_CODEX_A_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `reports/agent_runs/latest.json`（ignored 本地状态）
3. 任何真实 `reports/pilot_issues/*.json` 或真实 Pilot report
4. 任何 `app/`、`scripts/`、`tests/`、`migrations/` 文件
5. Hermes 主仓库

commit message：

```text
docs: add phase 2.44c fake issue intake dry-run
```

tag：

```text
phase-2.44c-fake-issue-intake-dry-run-baseline
```

## 验证命令

在 `/Users/Weishengsu/Hermes_memory` 执行：

```bash
git diff --check
uv run python -m json.tool docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json >/tmp/day1_fake_issue_input_check.json
uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json --strict >/tmp/day1_fake_issue_intake_validate.json
uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_FAKE_ISSUE_INPUT.json >/tmp/day1_fake_issue_intake_summary.json
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git status --short
```

本轮不运行 pytest；本轮为 docs/fake-data artifact baseline。

## Stage / commit / push 规则

1. 必须 selective staging，只 stage 白名单文件。
2. staged 后必须检查 `git diff --cached --name-only`。
3. 若 staged 文件超出白名单，必须 unstage 并停止。
4. commit 后创建 tag。
5. 推送 `origin/main` 与 tag。
6. baseline 后必须停止，不得进入 Phase 2.44d，不得生成真实 issue records，不得启动 Pilot 新轮次，不得自动发起 Codex C。

## 完成报告必须包含

1. commit hash。
2. tag 是否创建并指向当前 HEAD。
3. push 结果。
4. 最终 `git status --short`。
5. 是否只 stage / commit 白名单文件。
6. 是否保留无关 dirty：`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
7. 是否生成真实 Pilot report / issue records（必须为否）。
8. 是否写 DB / facts / document_versions / OpenSearch / Qdrant（必须为否）。
9. 是否进入 rollout / repair / Data Steward（必须为否）。
10. 下一步建议：进入 Phase 2.44d planning，评审是否用 explicit ignored local input 试跑真实 recorder workflow；仍不进入 production rollout。

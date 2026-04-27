# Next Codex A Prompt

这是 Codex A 的下一轮执行入口。Codex A 必须读取本文件完整内容执行，不依赖聊天窗口中的长 prompt。

## 执行前必须读取

1. `/Users/Weishengsu/Hermes_memory/docs/AGENT_OPERATING_PROTOCOL.md`
2. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

## 本轮目标

Phase 2.27e review audit eval / readiness 最小实现收口与 Git baseline。

本轮只做 baseline；不得继续进入下一阶段实现，不得执行 repair、rollout 或真实业务数据修改。

## 当前已确认事实

Codex B 已审核 Phase 2.27e 最小实现：

1. `scripts/phase225_readiness_audit.py` 新增只读 `report.review.created` 安全检查。
2. `report.review.created` 缺失时为 warning，不作为 fail。
3. unsafe report review audit payload 会被标记为 fail；该行为比原 prompt 更严格，但符合治理安全目标。
4. `--skip-service-check` 下服务不可用导致的下游检查降级为 warning，避免只读 smoke 误报失败。
5. `tests/test_phase225_readiness_audit.py` 已覆盖 missing/sanitized/unsafe report review audit。
6. `tests/test_phase227b_review_audit_preview.py` 已补强 item-level entity details 不进入 audit payload。
7. 未写真实业务 DB。
8. 未写真实 `audit_logs`。
9. 未修改 facts、document_versions、OpenSearch、Qdrant。
10. 未执行 repair、backfill、reindex、cleanup、delete、rollout。

Codex B 复跑验证：

1. `uv run python -m py_compile scripts/phase225_readiness_audit.py scripts/phase227b_review_audit_preview.py`：通过。
2. `uv run pytest tests/test_phase225_readiness_audit.py tests/test_phase227b_review_audit_preview.py -q`：`26 passed`。
3. `uv run python scripts/phase225_readiness_audit.py --skip-service-check --json`：`status=warn`、`failed=0`、`dry_run=true`、`destructive_actions=[]`。

## 只允许 stage 以下文件

1. `/Users/Weishengsu/Hermes_memory/scripts/phase225_readiness_audit.py`
2. `/Users/Weishengsu/Hermes_memory/tests/test_phase225_readiness_audit.py`
3. `/Users/Weishengsu/Hermes_memory/tests/test_phase227b_review_audit_preview.py`
4. `/Users/Weishengsu/Hermes_memory/docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
5. `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
6. `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`
7. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
8. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
9. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
10. `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`

不得 stage：

1. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
2. `/Users/Weishengsu/Hermes_memory/reports/nightly_runs/*.json`
3. 任何真实 report / review JSON
4. 任何未列入白名单的文件

## Baseline 前复核

执行：

```bash
git status --short
uv run python -m py_compile scripts/phase225_readiness_audit.py scripts/phase227b_review_audit_preview.py
uv run pytest tests/test_phase225_readiness_audit.py tests/test_phase227b_review_audit_preview.py -q
uv run python scripts/phase225_readiness_audit.py --skip-service-check --json
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 范围仅为 Phase 2.27e 实现 / 测试 / 文档 / 交接文件与 ignored local state。
2. tests 仍为 `26 passed`。
3. readiness smoke 仍为只读，`dry_run=true`、`destructive_actions=[]`。
4. `reports/agent_runs/latest.json` 仍被 ignored。
5. 无真实 report / review / nightly JSON 被 staged。
6. 无真实 DB / index / facts / version 数据变更。
7. 无 repair / backfill / reindex / cleanup / delete / rollout。

## Git 操作

如果复核通过：

```bash
git add \
  scripts/phase225_readiness_audit.py \
  tests/test_phase225_readiness_audit.py \
  tests/test_phase227b_review_audit_preview.py \
  docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md \
  docs/TODO.md \
  docs/DEV_LOG.md \
  docs/ACTIVE_PHASE.md \
  docs/HANDOFF_LOG.md \
  docs/PHASE_BACKLOG.md \
  docs/NEXT_CODEX_A_PROMPT.md

git diff --cached --name-only
git commit -m "chore: add phase 2.27e review audit eval checks"
git tag phase-2.27e-review-audit-eval-checks-baseline
git push origin main
git push origin phase-2.27e-review-audit-eval-checks-baseline
```

## 交接更新

baseline 成功后更新：

1. `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
2. `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
3. `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
4. `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`

`latest.json` 写入：

```json
{
  "phase": "Phase 2.27e Review Audit Eval Minimal Implementation",
  "status": "baseline",
  "git": {
    "commit": "<actual_commit_hash>",
    "tag": "phase-2.27e-review-audit-eval-checks-baseline",
    "pushed": true
  },
  "next_recommendation": "Return to Codex B for next route planning. Do not auto-enter next implementation."
}
```

## 停止条件

完成 baseline 后必须停止，不得进入下一阶段。

必须停止并报告：

1. dirty 文件超出白名单。
2. 测试失败。
3. 需要写真实业务 DB。
4. 需要真实 `audit_logs` 写入。
5. 需要 repair / backfill / reindex / cleanup / delete。
6. 需要修改 facts、document_versions、OpenSearch、Qdrant。
7. 需要 item-level audit summary。
8. 需要 rollout。
9. 需要 migration。
10. 需要自动进入下一阶段实现。

## 返回报告格式

请返回精简报告：

1. 修改文件
2. 测试与验证结果
3. 只读 smoke 结果
4. commit hash
5. tag
6. push 结果
7. 最终 `git status --short`
8. 是否仍有阻塞 / 风险
9. 是否建议进入下一阶段规划

不要执行 repair executor、rollout、真实业务数据修改或自动下一阶段开发。

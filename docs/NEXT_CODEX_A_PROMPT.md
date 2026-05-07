# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已复审 Phase 2.49 review-fix，结论：通过；现在授权执行 Git baseline。

## 本轮目标

Phase 2.49 Internal MVP Run Record Review Bridge Git baseline。

只提交 Phase 2.49 相关 runner、测试、规划文档与交接文档。不要进入 Phase 2.50。

## Codex B 复审结论

通过。

已确认：

1. `issue_summary.p0_count > 0` 且 `issues=[]` 时会生成 P0 placeholder，并输出 `decision_hint=no_go`。
2. `issue_summary.p1_count / p2_count / p3_count` 缺少详细 issue 时会生成 placeholder，P1 blocking，P2/P3 non-blocking。
3. `not_repair_cleanup_backfill_reindex_delete=false` 会生成 P0 boundary item，`evidence_policy.repair_authorized=true`，`decision_hint=no_go`。
4. `no_db_facts_document_versions_auditlogs_opensearch_qdrant_mutation=false` 会生成 P0 boundary item，`evidence_policy.data_mutation=true`，`decision_hint=no_go`。
5. Phase 2.42a review report 与 Phase 2.49 `decision_hint` 安全语义一致。
6. 仍不默认扫描 `reports/`，不读取真实 run records。
7. 固定 output safety flags 仍为：`production_rollout=false`、`repair_authorized=false`、`data_mutation=false`、`destructive_actions=[]`。

## Baseline 白名单

只允许 stage / commit 以下文件：

1. `scripts/phase249_internal_mvp_run_record_review.py`
2. `tests/test_phase249_internal_mvp_run_record_review.py`
3. `docs/PHASE249_INTERNAL_MVP_RUN_RECORD_REVIEW_PLAN.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/NIGHTLY_SPRINT_QUEUE.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

不要 stage `reports/agent_runs/latest.json`。

## 必须排除

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`（ignored）

## 必跑验证

```bash
cd /Users/Weishengsu/Hermes_memory
uv run python -m py_compile scripts/phase249_internal_mvp_run_record_review.py
uv run pytest tests/test_phase249_internal_mvp_run_record_review.py tests/test_phase242a_mvp_pilot_review_dry_run.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
```

不要运行 API / CLI smoke。
不要启动 / 停止服务。
不要读取真实 internal MVP run records。
不要写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。

## Git baseline

1. 只 stage 白名单 10 个文件。
2. commit message：`chore: add phase 2.49 internal mvp run record review bridge`
3. tag：`phase-2.49-internal-mvp-run-record-review-baseline`
4. push `origin/main`。
5. push tag 到 `origin`。

## Baseline 后更新 ignored 状态

更新 `reports/agent_runs/latest.json`：

1. `phase=Phase 2.49 Internal MVP Run Record Review Bridge Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push result。
4. 记录 tests：`20 passed`。
5. `needs_codex_b_review=false`
6. `needs_codex_c_validation=false`

`latest.json` 必须保持 ignored，不得 stage。

## 硬禁止

1. 不进入 Phase 2.50。
2. 不新增功能。
3. 不读取真实 reports / run records。
4. 不默认扫描 `reports/`。
5. 不运行 API / CLI smoke。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete。
8. 不进入 rollout。
9. 不进入 Data Steward 实现。
10. 不 stage / commit out-of-scope dirty。

## 完成后输出

1. commit hash。
2. tag。
3. push 结果。
4. 测试结果。
5. final git status。
6. out-of-scope dirty 是否仍保留。
7. 是否建议进入 Phase 2.50 planning。

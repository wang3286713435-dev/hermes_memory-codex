# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已完成 Phase 2.50a fake run record smoke review，结论：通过；现在授权执行 docs-only Git baseline。

## 本轮目标

Phase 2.50a Internal MVP Daily Review Loop Fake Run Record Smoke Git baseline。

只提交 Phase 2.50a fake smoke 结果文档和交接状态文档。不要进入 Phase 2.50b、Phase 2.51、真实 MVP Pilot、repair、rollout 或 Data Steward 实现。

## Codex B Review 结论

通过。

已确认：

1. `docs/PHASE250A_INTERNAL_MVP_RUNBOOK_SMOKE_RESULT.md` 明确 fake smoke 使用 `mktemp` 临时目录。
2. 没有读取真实 internal MVP run records。
3. sanitized JSON / Markdown 只写入显式临时 output-dir。
4. 未复核 visible Missing Evidence => `pause`，这是正确保守行为。
5. 显式复核 Missing Evidence => `go`。
6. `facts_as_answer=true` + third document contamination => `no_go`。
7. safety flags 保持：`dry_run=true`、`production_rollout=false`、`repair_authorized=false`、`destructive_actions=[]`、`data_mutation=false`。
8. 未运行 API / CLI，未启动服务，未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
9. 未进入 rollout、repair、Data Steward、Phase 2.50b 或 Phase 2.51。

Codex B 复核验证：

```bash
uv run python -m py_compile scripts/phase249_internal_mvp_run_record_review.py
uv run pytest tests/test_phase249_internal_mvp_run_record_review.py tests/test_phase242a_mvp_pilot_review_dry_run.py -q
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json reports/internal_mvp_runs/example.json reports/internal_mvp_runs/example.md reports/internal_mvp_runs/latest.json
```

结果：`20 passed`，其余检查通过。

## Baseline 白名单

只允许 stage / commit 以下文件：

1. `docs/PHASE250A_INTERNAL_MVP_RUNBOOK_SMOKE_RESULT.md`
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
5. 任何 `reports/internal_mvp_runs/**/*.json`
6. 任何 `reports/internal_mvp_runs/**/*.md`
7. 任何 `reports/internal_mvp_runs/latest.*`

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

1. 只 stage 白名单 8 个文件。
2. commit message：`docs: add phase 2.50a internal mvp runbook smoke result`
3. tag：`phase-2.50a-internal-mvp-runbook-smoke-baseline`
4. push `origin/main`。
5. push tag 到 `origin`。

## Baseline 后更新 ignored 状态

更新 `reports/agent_runs/latest.json`：

1. `phase=Phase 2.50a Internal MVP Daily Review Loop Fake Run Record Smoke Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push result。
4. 记录验证结果：`20 passed`。
5. `needs_codex_b_review=false`
6. `needs_codex_c_validation=false`

`latest.json` 必须保持 ignored，不得 stage。

## 硬禁止

1. 不进入 Phase 2.50b。
2. 不进入 Phase 2.51。
3. 不新增功能代码、scripts 或 tests。
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
7. 是否建议进入 Phase 2.50b evidence pack 或 Phase 2.51 Mac Mini operator checklist planning。

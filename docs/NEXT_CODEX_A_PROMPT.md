# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已 review Phase 2.51a Fake Deployment Record / Internal MVP Run Record Dry-run Smoke，结论：通过。下一轮只允许做 docs-only Git baseline。

## 本轮目标

Phase 2.51a Fake Deployment Record Dry-run Smoke Git Baseline。

只做 selective staging / commit / tag / push；不进入真实 Mac Mini deployment、Phase 2.50b、Phase 2.53、API / CLI smoke、repair、rollout 或 Data Steward。

## Codex B Review 结论

通过，理由：

1. `docs/PHASE251A_FAKE_DEPLOYMENT_RECORD_DRY_RUN.md` 清楚说明本轮只使用 fake / sanitized / temporary records。
2. fake deployment record 明确只是字段形状 / operator flow check，不是 deployment completion evidence。
3. canonical internal MVP run record 明确为 JSON。
4. Markdown notes 明确不是 Phase 2.49 bridge input。
5. Phase 2.49 bridge 只读取 `/tmp/hermes_phase251a_fake_smoke/fake_internal_mvp_run_record.json`。
6. review output 只写入 `/tmp/hermes_phase251a_fake_smoke/review_out`。
7. fake review `decision_hint=go` 已被文档限定为 fake internal controlled MVP continuation，不是 rollout approval。
8. 未读取真实 reports / run records，未启动 API / CLI / Docker，未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，未 repair，未 rollout。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
git check-ignore -v reports/deployment_records/example.json
git check-ignore -v reports/deployment_records/example.md
```

## 允许 stage 的文件

只允许 stage 以下文件：

1. `docs/PHASE251A_FAKE_DEPLOYMENT_RECORD_DRY_RUN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

## 必须排除 / 不得 stage

以下文件不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`
5. 任何真实 `reports/internal_mvp_runs/**`
6. 任何真实 `reports/deployment_records/**`
7. 任何真实 reports / reviews / run records。

## Baseline 操作

只在 staged 文件完全等于白名单时继续。

```bash
cd /Users/Weishengsu/Hermes_memory
git add docs/PHASE251A_FAKE_DEPLOYMENT_RECORD_DRY_RUN.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git diff --cached --name-only
```

确认 staged 仅上述 8 个文件后：

```bash
git commit -m "docs: baseline phase 2.51a fake deployment record dry-run"
git tag phase-2.51a-fake-deployment-record-dry-run-baseline
git push origin main
git push origin phase-2.51a-fake-deployment-record-dry-run-baseline
```

## Baseline 后复核

```bash
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
```

允许最终仍显示 out-of-scope dirty / untracked only if 它们是：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`

如果出现其他 dirty，停止并写交接。

## 硬禁止

1. 不写功能代码。
2. 不新增 / 修改 scripts 或 tests。
3. 不执行真实 Mac Mini deployment。
4. 不启动 / 停止服务。
5. 不运行 API / CLI smoke。
6. 不读取真实 reports / run records。
7. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
8. 不执行 repair / backfill / reindex / cleanup / delete / migration。
9. 不进入 production rollout。
10. 不进入 Data Steward / BIM 实现。
11. 不修改 retrieval contract。
12. 不修改 memory kernel 主架构。
13. baseline 后不得自动进入 Phase 2.50b / 2.53。

## 完成后状态

更新 `reports/agent_runs/latest.json`（ignored）：

1. `phase=Phase 2.51a Fake Deployment Record Dry-run Smoke Git Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push 结果。
4. `needs_codex_b_review=false`
5. `needs_codex_c_validation=false`
6. 下一步建议：进入下一阶段规划，优先考虑 Phase 2.50b evidence pack planning 或继续内部 MVP operator evidence work；仍不进入真实 deployment / rollout。

完成后停止，等待 Codex B / 用户检查。

# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。Codex B 已完成 Phase 2.45e Sanitized Deployment Record Template Artifact review，并批准进入 **docs-only Git baseline**。

## 当前状态

Phase 2.45e artifact 已完成并通过 Codex B review：

1. 新增 `docs/MAC_MINI_DEPLOYMENT_RECORD_TEMPLATE.md`。
2. 新增 `reports/deployment_records/.gitignore`。
3. 新增 `reports/deployment_records/README.md`。
4. Template 固定声明：
   - `record_type=mac_mini_deployment_record`
   - `deployment_executed_by_human=true`
   - `codex_executed_deployment=false`
   - `production_rollout_approved=false`
5. Template 覆盖 Git baseline、机器 / operator、env key-name checklist、NAS / external SSD、health-check evidence path、MVP smoke path、Go / Pause / No-Go、stop conditions、operator signoff。
6. `reports/deployment_records/.gitignore` 默认忽略真实 deployment record JSON / Markdown / latest / logs。
7. README 明确真实记录默认不入 Git，禁止 secrets / tokens / `.env` values / raw sensitive logs。

Codex B review 结论：

1. artifact 边界正确。
2. template 未被写成真实 deployment proof 或 rollout approval。
3. real deployment records 默认 ignored。
4. 可进入 Phase 2.45e docs-only Git baseline。
5. Mac mini 已到货，baseline 后主线可切入 Phase 2.46：Mac mini Day-0 real-machine setup / internal MVP application prep。
6. 但 Phase 2.45e 本轮仍不得执行真实部署。

## 本轮目标

只做 Phase 2.45e docs-only Git baseline。

不得新增功能、不得新增 deployment script、不得运行 Phase 2.45c runner、不得运行真实 API / CLI smoke、不得执行真实 Mac mini deployment、不得进入 Phase 2.46。

## 必须复跑

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git diff --check
git check-ignore -v reports/deployment_records/example.json
git check-ignore -v reports/deployment_records/example.md
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
```

确认：

1. dirty 只包含 Phase 2.45e 白名单文件与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `reports/deployment_records/example.json` 被 Git ignore 命中。
3. `reports/deployment_records/example.md` 被 Git ignore 命中。
4. `reports/agent_runs/latest.json` 被 Git ignore 命中。
5. 没有 scripts / tests / app / migrations / real deployment records / `.env` 被 staged。

不得运行：

1. pytest。
2. Phase 2.45c runner。
3. API / CLI smoke。
4. Hermes CLI chat。
5. real deployment commands。

## 允许 stage 的文件

只能 stage 以下文件：

1. `docs/MAC_MINI_DEPLOYMENT_RECORD_TEMPLATE.md`
2. `reports/deployment_records/.gitignore`
3. `reports/deployment_records/README.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/NIGHTLY_SPRINT_QUEUE.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

不得 stage：

1. `reports/agent_runs/latest.json`
2. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
3. `scripts/**`
4. `tests/**`
5. `app/**`
6. `migrations/**`
7. Hermes 主仓库
8. 真实 deployment record JSON / Markdown
9. 真实 reports / reviews / run JSON
10. `.env` 或 secret-bearing 文件

## Commit / Tag / Push

如果且仅如果 staged 文件完全匹配白名单，则执行：

```bash
git add docs/MAC_MINI_DEPLOYMENT_RECORD_TEMPLATE.md \
  reports/deployment_records/.gitignore \
  reports/deployment_records/README.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md
git commit -m "docs: add phase 2.45e deployment record template"
git tag phase-2.45e-deployment-record-template-baseline
git push origin main
git push origin phase-2.45e-deployment-record-template-baseline
```

## 硬边界

1. 不进入 Phase 2.46。
2. 不执行真实 Mac mini deployment。
3. 不新增 deployment script。
4. 不运行 Phase 2.45c runner。
5. 不运行真实 API / CLI smoke。
6. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
7. 不执行 repair / backfill / reindex / cleanup / delete。
8. 不进入 production rollout。
9. 不进入 Data Steward / BIM 实现。
10. 不修改 retrieval contract。
11. 不修改 memory kernel 主架构。

## Baseline 后更新

baseline 成功后更新 ignored `reports/agent_runs/latest.json`：

1. `phase=Phase 2.45e Sanitized Deployment Record Template Artifact Baseline`
2. `status=baseline`
3. `git.commit=<new_commit>`
4. `git.tag=phase-2.45e-deployment-record-template-baseline`
5. `git.pushed=true`
6. `needs_codex_b_review=false`
7. `next_recommendation=Mac mini 已到货；进入 Phase 2.46 前先由 Codex B 检查 baseline 状态，并写入 Day-0 real-machine setup / internal MVP application prep prompt。`

## 返回要求

返回精简报告：

1. 修改文件。
2. 验证结果。
3. commit hash / tag / push 结果。
4. final `git status --short`。
5. 是否进入下一阶段：否，baseline 后停止等待 Codex B / 用户。

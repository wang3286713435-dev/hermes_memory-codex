# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。Codex B 已完成 Phase 2.45c Read-only Health-check Script implementation review，并批准进入 **Git baseline**。

## 当前状态

Phase 2.45c implementation 已完成并通过 Codex B review：

1. 新增 `scripts/phase245c_health_check_dry_run.py`。
2. 新增 `tests/test_phase245c_health_check_dry_run.py`。
3. Runner 输出 JSON summary，固定：
   - `dry_run=true`
   - `writes_db=false`
   - `repairs=false`
   - `rollout_approved=false`
4. 默认只做 Git / env key-name / ignored runtime path 检查。
5. `--mount-path` 与 `--check-url` 必须显式传入。
6. `--check-url` 只做短 timeout HEAD / GET reachability，不发送 body / token。
7. 不访问真实 DB / OpenSearch / Qdrant。
8. 不运行真实 API / CLI smoke。
9. 不执行真实 Mac mini deployment。

Codex B review 结论：

1. 实现边界正确。
2. 目标测试通过。
3. 默认 dry-run 输出合法 JSON。
4. 可进入 Phase 2.45c Git baseline。
5. 不允许进入 Phase 2.45d。
6. 不允许执行真实 API / CLI smoke 或真实 Mac mini 部署。

## 本轮目标

只做 Phase 2.45c Git baseline。

不得新增功能、不得新增检查项、不得运行真实 API / CLI smoke、不得执行真实部署、不得进入下一 phase。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/TODO.md`
6. `docs/DEV_LOG.md`
7. `scripts/phase245c_health_check_dry_run.py`
8. `tests/test_phase245c_health_check_dry_run.py`
9. `reports/agent_runs/latest.json`

## Baseline 前检查

运行：

```bash
git status --short
uv run python -m py_compile scripts/phase245c_health_check_dry_run.py
uv run pytest tests/test_phase245c_health_check_dry_run.py -q
uv run python scripts/phase245c_health_check_dry_run.py --json > /tmp/phase245c_health_check.json
uv run python -m json.tool /tmp/phase245c_health_check.json >/tmp/phase245c_health_check_pretty.json
git diff --check
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 只包含 Phase 2.45c 白名单文件与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `reports/agent_runs/latest.json` 被 Git ignore 命中。
3. default dry-run 不访问真实 API / CLI / DB / OpenSearch / Qdrant。
4. 不存在 deployment output、DB/index/data 产物被 staged。

## 允许 stage 的文件

只能 stage 以下文件：

1. `scripts/phase245c_health_check_dry_run.py`
2. `tests/test_phase245c_health_check_dry_run.py`
3. `docs/PHASE245B_HEALTH_CHECK_DRY_RUN_PLAN.md`
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
3. `app/**`
4. `migrations/**`
5. Hermes 主仓库
6. 任何真实 reports / reviews / run JSON
7. 任何 `.env` 或 secret-bearing 文件

## Commit / Tag / Push

如果且仅如果 staged 文件完全匹配白名单，则执行：

```bash
git commit -m "chore: add phase 2.45c health check dry run"
git tag phase-2.45c-health-check-dry-run-baseline
git push origin main
git push origin phase-2.45c-health-check-dry-run-baseline
```

## 硬边界

本轮禁止：

1. 进入 Phase 2.45d。
2. 执行真实 Mac mini 部署。
3. 运行真实 API / CLI smoke。
4. 运行 Hermes CLI chat。
5. 写 DB / facts / document_versions / audit_logs。
6. 修改 OpenSearch / Qdrant。
7. repair / backfill / reindex / cleanup / delete。
8. production rollout。
9. Data Steward / BIM 实现。
10. 创建 production scheduler / cron。
11. 修改 retrieval contract 或 memory kernel 主架构。

## 完成后

更新 ignored `reports/agent_runs/latest.json`：

1. `status=baseline`
2. 记录 commit hash、tag、pushed=true。
3. 下一步建议只写为：等待 Codex B 确认 baseline 后，再由用户决定是否进入 Phase 2.45d Mac mini real-machine deployment record 或 Phase 2.45c follow-up。

最终输出必须包含：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 确认未 stage / commit `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
6. 确认未运行真实 API / CLI smoke、未执行真实部署、未写 DB / index。

完成 baseline 后停止，不得继续下一阶段。

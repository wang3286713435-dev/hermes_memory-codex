# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。

## 当前任务

Phase 2.46c Codex C local MVP smoke prompt artifact docs-only Git baseline。

Codex B 已审核通过 Phase 2.46c prompt artifact。你本轮只允许完成文档基线提交，不发起 Codex C，不运行 smoke，不启动服务，不进入 Phase 2.46d。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/NIGHTLY_SPRINT_PROTOCOL.md`
3. `docs/NIGHTLY_SPRINT_QUEUE.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`
9. `docs/CODEX_C_MAC_MINI_LOCAL_MVP_SMOKE_PROMPT.md`
10. `reports/agent_runs/latest.json`

## 本轮目标

只提交 Phase 2.46c Codex C local MVP smoke prompt artifact 文档基线。

## 允许 stage 的文件白名单

只能 stage 以下文件：

```text
docs/CODEX_C_MAC_MINI_LOCAL_MVP_SMOKE_PROMPT.md
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/HANDOFF_LOG.md
docs/NIGHTLY_SPRINT_QUEUE.md
docs/NEXT_CODEX_A_PROMPT.md
docs/TODO.md
docs/DEV_LOG.md
```

## 明确不得 stage / commit 的文件

1. 不得 stage `reports/agent_runs/latest.json`，它是 ignored 本地状态文件。
2. 不得 stage `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`，这是遗留无关 dirty。
3. 不得 stage reports / deployment_records / real smoke reports / real evidence artifacts。
4. 不得 stage scripts / tests / app / migrations。
5. 不得修改或 stage Hermes 主仓库。

## 轻量验证

执行：

```bash
git status --short
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 只包含 Phase 2.46c 白名单文件 + 遗留无关 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 不得被 staged。
3. `reports/agent_runs/latest.json` 被 ignore 命中，不得被 staged。
4. 没有真实 smoke report / evidence / deployment record 被 staged。

## Git baseline

若验证通过，执行：

```bash
git add docs/CODEX_C_MAC_MINI_LOCAL_MVP_SMOKE_PROMPT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git commit -m "docs: add phase 2.46c codex c mac mini smoke prompt"
git tag phase-2.46c-codex-c-mac-mini-smoke-prompt-baseline
git push origin main
git push origin phase-2.46c-codex-c-mac-mini-smoke-prompt-baseline
```

提交后更新 ignored 本地状态文件 `reports/agent_runs/latest.json`：

1. `phase`: `Phase 2.46c Codex C Local MVP Smoke Prompt Baseline`
2. `status`: `baseline`
3. `git.commit`: 写入实际 commit hash
4. `git.tag`: `phase-2.46c-codex-c-mac-mini-smoke-prompt-baseline`
5. `git.pushed`: `true`
6. `next_recommendation`: `Codex B may decide whether to authorize Codex C local MVP smoke execution. Do not auto-run smoke.`
7. `needs_codex_b_review`: `true`
8. `needs_codex_c_validation`: `false`

## 硬边界

本轮禁止：

1. 不发起 Codex C。
2. 不运行真实 smoke。
3. 不执行真实 Mac mini setup。
4. 不运行 Phase 2.45c health-check runner。
5. 不运行 API / CLI smoke。
6. 不生成真实 evidence / deployment record / MVP smoke report。
7. 不启动 Postgres / OpenSearch / Qdrant / Hermes_memory API / Hermes CLI。
8. 不读取或生成真实 secrets / `.env` values。
9. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
10. 不执行 repair / backfill / reindex / cleanup / delete / migration。
11. 不新增 deployment scripts / cron / scheduler / rollout automation。
12. 不进入 production rollout。
13. 不进入 Data Steward / BIM 实现。
14. 不修改 retrieval contract。
15. 不修改 memory kernel 主架构。

## 完成后输出

输出：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 明确 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 是否仍为未 staged 遗留 dirty。
6. 明确没有提交 `reports/agent_runs/latest.json`。
7. 明确没有运行 smoke / 生成真实 evidence / deployment record。
8. 下一步建议：等待 Codex B review，由用户决定是否显式授权 Codex C 执行 local MVP smoke。

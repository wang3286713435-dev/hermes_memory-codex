# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。

## 当前任务

Phase 2.47 / 2.47a / 2.47b Internal MVP operating artifacts combined docs baseline。

Codex B 已 review：

1. `docs/PHASE247_INTERNAL_MVP_OPERATING_LOOP_PLAN.md`
2. `docs/INTERNAL_MVP_DAILY_OPERATOR_CHECKLIST.md`
3. `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md`
4. `reports/internal_mvp_runs/.gitignore`
5. `reports/internal_mvp_runs/README.md`

结论：Phase 2.47 + 2.47a + 2.47b 已形成可复用 internal controlled MVP operating artifact 包，满足 Baseline Gate。你本轮只允许做 combined docs baseline；不得进入 Phase 2.48，不得运行 smoke，不得启动服务，不得生成真实 run record，不得 production rollout。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/NIGHTLY_SPRINT_PROTOCOL.md`
3. `docs/NIGHTLY_SPRINT_QUEUE.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`
9. `docs/PHASE247_INTERNAL_MVP_OPERATING_LOOP_PLAN.md`
10. `docs/INTERNAL_MVP_DAILY_OPERATOR_CHECKLIST.md`
11. `docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md`
12. `reports/internal_mvp_runs/.gitignore`
13. `reports/internal_mvp_runs/README.md`
14. `reports/agent_runs/latest.json`

## Baseline Gate 判断

本轮允许 baseline，因为：

1. 当前 phase 有明确验收结果：2.47 planning、2.47a checklist、2.47b run record template 均完成。
2. Codex B review 通过：artifact 包边界正确。
3. 目标静态检查通过：`git diff --check`、latest JSON 校验、ignore 检查通过。
4. 文档状态已同步：ACTIVE_PHASE、PHASE_BACKLOG、HANDOFF_LOG、NIGHTLY_SPRINT_QUEUE、TODO、DEV_LOG、ignored latest 已更新。
5. 下一步将切换到实际 Day-0 / Day-1 使用或 Phase 2.48 规划，需要将 reusable artifact 包固化。

## 允许 stage 的文件白名单

只能 stage 以下文件：

```text
docs/PHASE247_INTERNAL_MVP_OPERATING_LOOP_PLAN.md
docs/INTERNAL_MVP_DAILY_OPERATOR_CHECKLIST.md
docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md
reports/internal_mvp_runs/.gitignore
reports/internal_mvp_runs/README.md
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
2. 不得 stage 任何真实 `reports/internal_mvp_runs/*.json` 或 `*.md`。
3. 不得 stage `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`，这是遗留无关 dirty。
4. 不得 stage `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`。
5. 不得 stage `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`。
6. 不得 stage reports / deployment_records / real smoke reports / raw evidence artifacts。
7. 不得 stage scripts / tests / app / migrations。
8. 不得修改或 stage Hermes 主仓库。
9. 不得提交 secret、`.env` value、raw log、真实业务敏感内容。

## 轻量验证

执行：

```bash
git status --short
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
```

确认：

1. dirty 包含 Phase 2.47 / 2.47a / 2.47b 白名单文件，外加 out-of-scope 文件。
2. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 不得被 staged。
3. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md` 不得被 staged。
4. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md` 不得被 staged。
5. `reports/agent_runs/latest.json` 被 ignore 命中，不得被 staged。
6. `reports/internal_mvp_runs/*.json`、`*.md` 与 `latest.*` 被 ignore 命中。
7. 没有真实 run record、raw transcript、secret、`.env` value 或 deployment evidence 被 staged。

## Git baseline

若验证通过，执行：

```bash
git add docs/PHASE247_INTERNAL_MVP_OPERATING_LOOP_PLAN.md \
  docs/INTERNAL_MVP_DAILY_OPERATOR_CHECKLIST.md \
  docs/INTERNAL_MVP_PILOT_RUN_RECORD_TEMPLATE.md \
  reports/internal_mvp_runs/.gitignore \
  reports/internal_mvp_runs/README.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git diff --cached --name-only
git commit -m "docs: add phase 2.47 internal mvp operating artifacts"
git tag phase-2.47-internal-mvp-operating-artifacts-baseline
git push origin main
git push origin phase-2.47-internal-mvp-operating-artifacts-baseline
```

提交后更新 ignored 本地状态文件 `reports/agent_runs/latest.json`：

1. `phase`: `Phase 2.47 Internal MVP Operating Artifacts Baseline`
2. `status`: `baseline`
3. `git.commit`: 写入实际 commit hash
4. `git.tag`: `phase-2.47-internal-mvp-operating-artifacts-baseline`
5. `git.pushed`: `true`
6. `next_recommendation`: `User may start internal controlled MVP Day-0/Day-1 using checklist and local ignored run record template, or Codex B may plan Phase 2.48 P2 display tails triage. Production rollout remains forbidden.`
7. `needs_codex_b_review`: `true`
8. `needs_codex_c_validation`: `false`

## 硬边界

本轮禁止：

1. 不运行真实 smoke。
2. 不启动、停止或修改服务。
3. 不执行真实 Mac mini setup。
4. 不运行 Phase 2.45c health-check runner。
5. 不生成真实 deployment record / raw evidence artifact。
6. 不生成真实 internal MVP run record。
7. 不读取或生成真实 secrets / `.env` values。
8. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
9. 不执行 repair / backfill / reindex / cleanup / delete / migration。
10. 不新增 deployment scripts / cron / scheduler / rollout automation。
11. 不进入 production rollout。
12. 不进入 Data Steward / BIM 实现。
13. 不修改 retrieval contract。
14. 不修改 memory kernel 主架构。

## 完成后输出

输出：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 明确 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 是否仍为未 staged 遗留 dirty。
6. 明确 `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md` 与 `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md` 是否仍为未 staged out-of-scope 文件。
7. 明确没有提交 `reports/agent_runs/latest.json`。
8. 明确没有提交真实 `reports/internal_mvp_runs/*.json` / `*.md`。
9. 明确没有运行 smoke / 启动服务 / 写 DB / 生成真实 deployment record。
10. 下一步建议：用户可以在 Mac mini operations thread 使用 checklist + local ignored run record template 开始 Day-0 / Day-1；或由 Codex B 规划 Phase 2.48 P2 display tails triage。

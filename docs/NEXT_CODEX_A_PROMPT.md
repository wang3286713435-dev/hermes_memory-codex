# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮执行入口。

## 当前任务

Phase 2.46d Mac mini local MVP smoke result intake / docs-only baseline。

Codex B 已审查 Codex C 的真实终端 smoke 报告：本轮 `Go`，但只代表内部受控 MVP smoke 通过，不代表 production rollout、自动审标、自动投标、自动经营决策、repair 或 Data Steward 授权。

你本轮只允许把 Codex C smoke 结果做 sanitized 文档归档与 Git baseline；不得启动服务、不得重跑 smoke、不得写 DB / index、不得进入 Phase 2.47 实现。

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
10. `docs/MAC_MINI_DAY0_SETUP_CHECKLIST.md`
11. `docs/PHASE246B_MAC_MINI_EVIDENCE_ATTACHMENT_PLAN.md`
12. `reports/agent_runs/latest.json`

## Codex C smoke 结果摘要

将以下结果写入新的 sanitized phase 文档，不要保存 raw transcript、secret、`.env` value、完整日志或真实业务敏感内容。

```text
phase=Phase 2.46d Mac mini local MVP smoke result intake
session_id=20260507_170043_729824
api_health=pass, 200 OK
hermes_cli=pass
decision=Go
p0=0
p1=0
p2=2
production_rollout=false
repair_authorized=false
data_steward_authorized=false
```

Alias 绑定结果：

```text
@主标书 -> alias_bound, document_id=869d4684-0a98-4825-bc72-ada65c15cfc9, version_id=43558ba9-2813-42ff-b11b-3fbb4448a5bb, alias_missing=false, retrieval_suppressed=false
@会议纪要 -> alias_bound, document_id=92051cc6-56b5-4930-bdf0-119163c83a75, version_id=e3b422e3-35e2-4d89-8136-66a558e8cfbe, alias_missing=false, retrieval_suppressed=false
@硬件清单 -> alias_bound, document_id=402657e8-2ea8-48b7-8266-85aab45bbc41, version_id=f1c43bfd-6b1b-4ec1-99a6-c0650e2e2e14, alias_missing=false, retrieval_suppressed=false
@C塔方案 -> alias_bound, document_id=a52e75b3-fec9-4e08-8c0d-03b0e55cf21d, version_id=2e0adc17-f8ea-4ac3-b944-a788c1980616, alias_missing=false, retrieval_suppressed=false
```

Query 结果：

```text
Q1 主标书基础字段: pass; only @主标书 evidence; citation visible; limit/control price Missing Evidence visible; no contamination.
Q2 Excel citation: pass with P2; only @硬件清单 evidence; sheet_name=开始; cell_range=A3:P24 + Row 7; row/range citation is human-checkable but not exact single-cell.
Q3 PPTX citation: pass; only @C塔方案 evidence; slide_number=1; slide_title=卓羽智能.
Q4 会议纪要边界: partial/P2; only @会议纪要 evidence; transcript_as_fact not explicitly printed, but content did not treat transcript as confirmed facts.
Q5 公司方向分析: pass/P2; four target aliases cited; recommendations marked human-decision-required; Missing Evidence visible; no automatic business decision.
```

结论：

```text
Internal controlled MVP smoke may continue.
Production rollout remains forbidden.
All tender / business / contract / procurement / customer communication decisions require human owner confirmation.
Codex A has no blocking code fix from this smoke; only P2 display tails should be tracked.
```

## 本轮目标

1. 新增 `docs/PHASE246D_MAC_MINI_LOCAL_MVP_SMOKE_RESULT.md`，记录 sanitized smoke result、Go / Pause / No-Go、P0/P1/P2/P3、边界与后续建议。
2. 更新 `docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/NIGHTLY_SPRINT_QUEUE.md`、`docs/TODO.md`、`docs/DEV_LOG.md`。
3. 更新本文件，完成 Phase 2.46d docs-only Git baseline 任务描述。
4. 更新 ignored 本地状态 `reports/agent_runs/latest.json`，但不得 stage。
5. 只做 docs-only baseline；不新增脚本、不新增测试、不执行真实 smoke。

## 允许 stage 的文件白名单

只能 stage 以下文件：

```text
docs/PHASE246D_MAC_MINI_LOCAL_MVP_SMOKE_RESULT.md
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
3. 不得 stage reports / deployment_records / real smoke reports / raw evidence artifacts。
4. 不得 stage scripts / tests / app / migrations。
5. 不得修改或 stage Hermes 主仓库。
6. 不得提交任何 secret、`.env` value、raw log、真实业务敏感内容。

## 轻量验证

执行：

```bash
git status --short
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

确认：

1. dirty 只包含 Phase 2.46d 白名单文件 + 遗留无关 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
2. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 不得被 staged。
3. `reports/agent_runs/latest.json` 被 ignore 命中，不得被 staged。
4. 没有真实 smoke report / raw evidence / deployment record 被 staged。
5. 新增 phase 文档没有把 `Go` 写成 production rollout approval。

## Git baseline

若验证通过，执行：

```bash
git add docs/PHASE246D_MAC_MINI_LOCAL_MVP_SMOKE_RESULT.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git commit -m "docs: record phase 2.46d mac mini local mvp smoke result"
git tag phase-2.46d-mac-mini-local-mvp-smoke-result-baseline
git push origin main
git push origin phase-2.46d-mac-mini-local-mvp-smoke-result-baseline
```

提交后更新 ignored 本地状态文件 `reports/agent_runs/latest.json`：

1. `phase`: `Phase 2.46d Mac Mini Local MVP Smoke Result Baseline`
2. `status`: `baseline`
3. `git.commit`: 写入实际 commit hash
4. `git.tag`: `phase-2.46d-mac-mini-local-mvp-smoke-result-baseline`
5. `git.pushed`: `true`
6. `next_recommendation`: `Proceed to Phase 2.47 planning for internal controlled MVP operating loop / issue intake. Do not enter production rollout.`
7. `needs_codex_b_review`: `true`
8. `needs_codex_c_validation`: `false`

## 硬边界

本轮禁止：

1. 不运行真实 smoke。
2. 不启动、停止或修改服务。
3. 不执行真实 Mac mini setup。
4. 不运行 Phase 2.45c health-check runner。
5. 不生成真实 deployment record / raw evidence artifact。
6. 不读取或生成真实 secrets / `.env` values。
7. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
8. 不执行 repair / backfill / reindex / cleanup / delete / migration。
9. 不新增 deployment scripts / cron / scheduler / rollout automation。
10. 不进入 production rollout。
11. 不进入 Data Steward / BIM 实现。
12. 不修改 retrieval contract。
13. 不修改 memory kernel 主架构。
14. 不把 Internal controlled MVP smoke `Go` 写成自动审标、自动投标、自动经营决策或客户交付批准。

## 完成后输出

输出：

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 明确 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 是否仍为未 staged 遗留 dirty。
6. 明确没有提交 `reports/agent_runs/latest.json`。
7. 明确没有运行 smoke / 写 DB / 生成真实 deployment record。
8. 下一步建议：Phase 2.47 planning，聚焦内部受控 MVP operating loop、Pilot issue intake 与 P2 展示尾项跟踪；继续禁止 production rollout。

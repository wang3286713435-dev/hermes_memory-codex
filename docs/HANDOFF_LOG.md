# Handoff Log

## 2026-04-27 01:32 Phase 2.27b
- goal: 启用 Codex A 文件化交接协议，补齐 ACTIVE_PHASE、PHASE_BACKLOG、HANDOFF_LOG 与 latest.json。
- changed_files:
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮仅做交接协议状态文件同步。
- validation: 已读取 PRD、ROADMAP、TECHNICAL_DESIGN、TODO、DEV_LOG；确认 ACTIVE_PHASE / PHASE_BACKLOG 原缺失。
- risks: 当前 Phase 2.27b 规划文档仍未 baseline；latest.json 属本地状态文件，默认不作为真实报告提交。
- next: 建议 Codex B 审核交接协议；随后选择 Phase 2.27b baseline 或 audit preview 实现。
- commit/tag if any: 无。

## 2026-04-27 01:32 Phase 2.28
- goal: 固化 Agent Operating Protocol / 文件化交接机制基线。
- changed_files:
  - `docs/AGENT_OPERATING_PROTOCOL.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/PHASE227B_REVIEW_AUDIT_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/.gitignore`
  - `reports/agent_runs/README.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做协作协议与文档基线。
- validation: 已读取 PRD、ROADMAP、TECHNICAL_DESIGN、TODO、DEV_LOG、ACTIVE_PHASE、PHASE_BACKLOG。
- risks: latest.json 是 ignored 本地状态文件；Phase 2.27b 仍未实现 audit preview；repair executor、真实 audit_logs 写入和 rollout 仍禁止。
- next: 建议 Codex B 审核 Phase 2.28 协议后做 baseline，再进入 Phase 2.27b audit preview 实现。
- commit/tag if any: 无。

## 2026-04-27 02:06 Phase 2.28b
- goal: 新增 Codex A 固定任务入口 `docs/NEXT_CODEX_A_PROMPT.md`。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/AGENT_OPERATING_PROTOCOL.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做协议与文档入口补丁。
- validation: 已写入 Phase 2.27b audit preview / dry-run 完整下一轮任务；未创建脚本或测试。
- risks: latest.json 仍为 ignored 本地状态文件；Phase 2.27b 仍未实现；repair executor、真实 audit_logs 写入和 rollout 仍禁止。
- next: 建议 Codex B 审核后做 Phase 2.28b baseline，再执行 `docs/NEXT_CODEX_A_PROMPT.md`。
- commit/tag if any: 无。

## 2026-04-27 02:10 Phase 2.28c
- goal: 建立 Nightly Sprint Protocol / Queue，限定夜间 bounded autonomous sprint。
- changed_files:
  - `docs/NIGHTLY_SPRINT_PROTOCOL.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/nightly_runs/.gitignore`
  - `reports/nightly_runs/README.md`
  - `docs/AGENT_OPERATING_PROTOCOL.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做协议、队列与 ignore/README。
- validation: 已写入 Green / Yellow / Red Lane、夜间停止条件与初始 queue；未实现 Phase 2.27b。
- risks: Nightly Sprint 不等于生产 cron；baseline / tag / push 属 Yellow Lane；repair、migration、rollout 仍为 Red Lane。
- next: 建议 Codex B 审核后 baseline Phase 2.28c，再启动第一个 Green Lane queue item。
- commit/tag if any: 无。

## 2026-04-27 02:20 Phase 2.27b
- goal: 按 `docs/NEXT_CODEX_A_PROMPT.md` 实现 review record sanitized audit payload preview / dry-run。
- changed_files:
  - `scripts/phase227b_review_audit_preview.py`
  - `tests/test_phase227b_review_audit_preview.py`
  - `docs/PHASE227B_REVIEW_AUDIT_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`：通过。
  - `uv run pytest tests/test_phase227b_review_audit_preview.py -q`：`10 passed`。
- validation: 临时目录 fake review record preview 通过；payload 未包含 notes、reason、approved_action、item_decisions、本机绝对路径、entity id 或 executed。
- risks: 真实写 `audit_logs` 仍后置；item-level audit summary 仍后置；repair executor 与 rollout 仍禁止。
- next: 建议 Codex B 审核后进入 Phase 2.27b Git baseline。
- commit/tag if any: 无。

## 2026-04-27 02:35 Phase 2.27b
- goal: Codex B 通过文件交接系统写入 Phase 2.27b Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只更新下一轮 Codex A 文件化执行入口。
- validation: `NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27b baseline 任务；仍禁止写 audit_logs、写 DB、repair、rollout。
- risks: `reports/agent_runs/latest.json` 为 ignored 本地状态文件，不应提交；baseline 前仍需 Codex A 复跑 py_compile 与 pytest。
- next: Codex A 只需执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.27b baseline。
- commit/tag if any: 无。

## 2026-04-27 02:40 Phase 2.27c
- goal: Nightly Sprint Green Lane 执行 Phase 2.27c route planning，评审是否真实写 `audit_logs`。
- changed_files:
  - `docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
  - `reports/nightly_runs/20260427_024050.json`
- tests: 未运行；本轮只做规划与文档同步。
- validation: 已明确建议后续仅做 report-level sanitized audit 写入，必须显式 opt-in；真实 DB 写入属于 Yellow Lane，不允许夜间自动实现。
- risks: notes、reason、approved_action、完整 item_decisions 与 item-level entity details 仍须硬排除；repair executor、rollout、DB schema 扩大继续禁止。
- next: Codex B 审核 Phase 2.27c 规划；若通过，由用户显式授权 Phase 2.27d report-level review audit write MVP。
- commit/tag if any: 无。

## 2026-04-27 02:55 Phase 2.27c
- goal: Codex B 通过文件交接系统写入 Phase 2.27c Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只更新下一轮 Codex A 文件化执行入口。
- validation: `NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27c planning baseline 任务；仍禁止写 audit_logs、写 DB、repair、rollout。
- risks: `reports/agent_runs/latest.json` 与 `reports/nightly_runs/*.json` 为 ignored 本地状态文件，不应提交；Phase 2.27d 真实写 audit_logs 必须后续显式授权。
- next: Codex A 只需执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.27c planning baseline。
- commit/tag if any: 无。

## 2026-04-27 03:05 Phase 2.27c
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.27c route planning Git baseline。
- changed_files:
  - `docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做规划 baseline。
- validation: 已复核 ignored 状态；`latest.json` 与 nightly run JSON 不提交；未写 audit_logs、未写业务 DB、未执行 repair。
- risks: Phase 2.27d 真实写 audit_logs 属 Yellow Lane，必须 Codex B 审核与用户显式授权；repair executor 与 rollout 继续禁止。
- next: Codex B 审核本 baseline；如通过，由用户授权 Phase 2.27d report-level sanitized audit 写入 MVP。
- commit/tag if any: 待本轮 Git commit / tag 写入。

## 2026-04-27 03:05 Phase 2.27d
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，实现 report-level sanitized review audit 写入 MVP。
- changed_files:
  - `scripts/phase227b_review_audit_preview.py`
  - `tests/test_phase227b_review_audit_preview.py`
  - `docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`：通过。
  - `uv run pytest tests/test_phase227b_review_audit_preview.py -q`：`15 passed`。
- validation: 临时 SQLite live smoke 通过，显式 `--write-audit` 写入 `1` 条 sanitized `audit_logs`；stdout 与 DB payload 均未包含 notes、reason、approved_action、item_decisions、本机绝对路径、item-level entity details 或 executed。
- risks: 真实项目环境执行 `--write-audit` 仍属于 Yellow Lane；item-level audit summary、完整 review record 入库、repair executor 与 rollout 继续后置。
- next: 建议 Codex B 审核后执行 Phase 2.27d Git baseline；暂不进入下一阶段实现。
- commit/tag if any: 无。

## 2026-04-27 03:16 Phase 2.27d
- goal: 完成 Phase 2.27d Git baseline，不进入 Phase 2.27e 实现。
- changed_files:
  - `scripts/phase227b_review_audit_preview.py`
  - `tests/test_phase227b_review_audit_preview.py`
  - `docs/PHASE227C_REVIEW_AUDIT_WRITE_ROUTE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests:
  - `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`：通过。
  - `uv run pytest tests/test_phase227b_review_audit_preview.py -q`：`15 passed`。
- validation: `latest.json` 与 nightly run JSON 均保持 ignored；未 stage 真实 reports / reviews / agent run JSON；未写生产 / 真实业务 DB。
- risks: 后续如使用 `--write-audit` 仍需显式 opt-in；repair executor、item-level audit summary 与 rollout 继续禁止自动推进。
- next: 交回 Codex B 做 Phase 2.27e 路线规划；不要自动进入下一阶段。
- commit/tag if any: Phase 2.27d baseline commit / tag 以最终 Git 结果和 `latest.json` 为准。

## 2026-04-27 Phase 2.27d Codex B Review
- goal: 检查最新交接并进入 Nightly Sprint 前置判定。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase227b_review_audit_preview.py`：通过。
  - `uv run pytest tests/test_phase227b_review_audit_preview.py -q`：`15 passed`。
- validation: 当前 Phase 2.27d 已 validated，但尚未 baseline；`reports/agent_runs/latest.json` 与 `reports/nightly_runs/*.json` 均为 ignored local state。
- risks: Phase 2.27d baseline 属 Yellow Lane，完成后必须停止等待 Codex B；不得夜间自动进入 Phase 2.27e 或扩大 `--write-audit` 范围。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27d Git baseline 任务；Codex A 执行后必须停止。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27d Baseline Review
- goal: 检查 Codex A 最新交接，确认 Phase 2.27d baseline 是否完成。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未重新运行；本轮核对 Codex A 交接、Git HEAD、tag、origin/main 与 ignored local state。
- validation: Phase 2.27d baseline 已完成，HEAD 与 `origin/main` 均为 `65515681cd48679ebb90e055164c4ad9970bc743`，tag `phase-2.27d-review-audit-write-baseline` 指向 HEAD。
- risks: 后续 `--write-audit` 仍必须显式 opt-in；repair executor、rollout、item-level audit summary 继续后置。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27e planning 任务，只做路线规划，不写代码、不写 DB。
- commit/tag if any: 无。

## 2026-04-27 10:00 Phase 2.27e
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，规划 report review audit 是否纳入 readiness / eval。
- changed_files:
  - `docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮只做规划。执行 `git status --short` 与 `git check-ignore -v reports/agent_runs/latest.json` 复核状态。
- validation: 已完成 A-E 候选方向评审；推荐后续只做 deterministic eval / unit test 安全断言与 readiness audit 只读检查。
- risks: item-level audit summary、完整 review record 入库、repair executor、rollout 与真实业务 DB 扩大写入继续禁止。
- next: Codex B 审核 Phase 2.27e 规划；如通过，再生成最小实现 prompt。
- commit/tag if any: 无。

## 2026-04-27 12:34 Phase 2.27e
- goal: 完成 Phase 2.27e 路线规划 Git baseline，不进入实现。
- changed_files:
  - `docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests: 未运行 pytest；本轮只做规划 baseline。已复核 `git status --short` 与 `reports/agent_runs/latest.json` ignored 状态。
- validation: baseline 范围仅包含 Phase 2.27e 规划与交接文档；未写 `audit_logs`、未写 DB、未执行 repair / eval / rollout。
- risks: 后续实现必须保持 deterministic eval / fixture DB / readiness 只读边界；item-level audit 和 repair executor 继续后置。
- next: 交回 Codex B 审核 baseline，并决定是否授权 Phase 2.27e 最小实现。
- commit/tag if any: Phase 2.27e baseline commit / tag 以最终 Git 结果和 `latest.json` 为准。

## 2026-04-27 Phase 2.27e Codex B Review
- goal: 检查 Codex A 最新交接，审核 Phase 2.27e 路线规划。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做规划审核与下一轮文件化任务入口更新。
- validation: Phase 2.27e 规划边界正确；推荐路线为 deterministic eval / unit test 安全断言 + readiness audit 只读检查；未扩大 DB 写入范围。
- risks: item-level audit summary、完整 review record 入库、repair executor、rollout 继续后置；后续实现不得触碰真实业务 DB。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27e planning baseline 任务；Codex A 执行后必须停止。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27e Baseline Review
- goal: 检查项目进度，确认 Phase 2.27e planning baseline，并生成最小实现任务入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.27e planning baseline 已完成，HEAD 与 `origin/main` 对齐，tag `phase-2.27e-review-audit-eval-plan-baseline` 指向 HEAD。
- risks: 后续实现必须保持 readiness audit 只读、review audit 写入仅限临时 SQLite / fixture DB 测试；不得触碰真实业务 DB。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27e 最小实现任务；Codex A 执行后必须停止等待 Codex B 审核。
- commit/tag if any: 无。

## 2026-04-27 13:02 Phase 2.27e
- goal: 执行 NEXT_CODEX_A_PROMPT，完成 review audit 安全断言与 readiness audit 只读检查。
- changed_files:
  - `scripts/phase225_readiness_audit.py`
  - `tests/test_phase225_readiness_audit.py`
  - `tests/test_phase227b_review_audit_preview.py`
  - `docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: `py_compile` 通过；`uv run pytest tests/test_phase225_readiness_audit.py tests/test_phase227b_review_audit_preview.py -q` 为 `26 passed`。
- validation: readiness audit `--skip-service-check --json` 输出 `status=warn`、`failed=0`、`dry_run=true`、`destructive_actions=[]`。
- risks: `docs/NEXT_CODEX_A_PROMPT.md` 存在既有 dirty，非本轮修改；缺少 `report.review.created` 仍为 warning。
- next: Codex B review 后再决定是否进入 Phase 2.27e Git baseline。
- commit/tag if any: 无。

## 2026-04-27 13:42 Phase 2.27e
- goal: 完成 Phase 2.27e review audit eval / readiness 最小实现 Git baseline。
- changed_files:
  - `scripts/phase225_readiness_audit.py`
  - `tests/test_phase225_readiness_audit.py`
  - `tests/test_phase227b_review_audit_preview.py`
  - `docs/PHASE227E_REVIEW_AUDIT_EVAL_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests: `py_compile` 通过；`uv run pytest tests/test_phase225_readiness_audit.py tests/test_phase227b_review_audit_preview.py -q` 为 `26 passed`。
- validation: readiness audit `--skip-service-check --json` 输出 `status=warn`、`failed=0`、`dry_run=true`、`destructive_actions=[]`；`reports/agent_runs/latest.json` 仍 ignored。
- risks: 缺少 `report.review.created` 仍为 warning；item-level audit summary、repair executor、真实业务 DB 写入与 rollout 继续后置。
- next: 交回 Codex B 做下一阶段路线规划，不自动进入实现。
- commit/tag if any: Phase 2.27e baseline commit / tag 以 final output 与 `reports/agent_runs/latest.json` 为准。

## 2026-04-27 Phase 2.27e Codex B Implementation Review
- goal: 检查项目进度，审核 Phase 2.27e 最小实现。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase225_readiness_audit.py scripts/phase227b_review_audit_preview.py`：通过。
  - `uv run pytest tests/test_phase225_readiness_audit.py tests/test_phase227b_review_audit_preview.py -q`：`26 passed`。
  - `uv run python scripts/phase225_readiness_audit.py --skip-service-check --json`：`status=warn`、`failed=0`、`dry_run=true`、`destructive_actions=[]`。
- validation: 实现边界正确；readiness audit 仅只读检查 report-level sanitized audit；未写真实 DB / audit_logs，未修改 facts、versions、OpenSearch、Qdrant。
- risks: unsafe report review audit 被标为 fail，强于原提示词的 warning，Codex B 认为该收紧符合治理安全目标；item-level audit、repair executor 与 rollout 继续后置。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27e Git baseline 任务；Codex A 执行后必须停止。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27e Baseline Review
- goal: 检查项目进度，确认 Phase 2.27e baseline，并生成下一阶段路线规划任务。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.27e baseline 已完成，HEAD 与 `origin/main` 对齐，tag `phase-2.27e-review-audit-eval-checks-baseline` 指向 HEAD。
- risks: report review audit 缺失仍为 warning；item-level audit、repair executor、真实业务 DB 写入与 rollout 继续后置。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27f route planning 任务，只做规划，不写代码、不写 DB、不执行 repair。
- commit/tag if any: 无。

## 2026-04-27 13:56 Phase 2.27f
- goal: 规划 archive / review / audit 三者关联诊断。
- changed_files:
  - `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮只做规划与文档同步。
- validation: 已评审 A-E 候选方向；推荐后续只做 archive / review / audit 只读 linkage summary。
- risks: linkage summary 不得被误读为 repair executed；不得输出本机路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。
- next: Codex B 审核 Phase 2.27f 规划；如通过，再生成 Git baseline prompt。
- commit/tag if any: 无。

## 2026-04-27 14:05 Phase 2.27f
- goal: 完成 Phase 2.27f archive / review / audit 关联诊断规划 Git baseline。
- changed_files:
  - `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests: 未运行 pytest；本轮为 planning baseline。已复核 `git status --short` 与 `reports/agent_runs/latest.json` ignored 状态。
- validation: baseline 范围仅包含 Phase 2.27f 规划与交接文档；未写 `audit_logs`、未写 DB、未执行 repair / eval / rollout。
- risks: 后续实现必须只用 fake manifest / fake review / fake audit event；不得输出本机路径、notes、reason、approved_action 或 item-level entity details。
- next: 交回 Codex B 审核 baseline，并决定是否授权 Phase 2.27f 最小实现。
- commit/tag if any: Phase 2.27f baseline commit / tag 以最终 Git 结果和 `latest.json` 为准。

## 2026-04-27 Phase 2.27f Codex B Review
- goal: 检查项目进度，审核 Phase 2.27f archive / review / audit 关联诊断规划，并生成 baseline 任务。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做 Codex B review 与下一轮文件化任务入口更新。
- validation: Phase 2.27f 规划边界安全；仅建议后续只读 linkage summary，不写 DB、不写 `audit_logs`、不执行 repair、不输出 item-level entity details。
- risks: linkage summary 后续实现必须继续显式 `repair_executed=false`；真实 reports / reviews / audit payload 仍需避免本机路径、notes、reason、approved_action 与完整 item_decisions。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27f Git baseline 任务；Codex A 执行后必须停止，不进入实现。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27f Baseline Review
- goal: 检查项目进度，确认 Phase 2.27f planning baseline，并生成最小实现任务入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.27f planning baseline 已完成，HEAD 与 `origin/main` 对齐，tag `phase-2.27f-review-audit-linkage-plan-baseline` 指向 HEAD。
- risks: 后续实现必须只读、只用 fake manifest / fake review / fake audit event；不得输出本机路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27f 最小实现任务；Codex A 执行后必须停止等待 Codex B 审核。
- commit/tag if any: 无。

## 2026-04-27 14:26 Phase 2.27f
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 archive / review / audit 只读 linkage summary 最小实现。
- changed_files:
  - `scripts/phase227f_review_audit_linkage.py`
  - `tests/test_phase227f_review_audit_linkage.py`
  - `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py` 通过；`uv run pytest tests/test_phase227f_review_audit_linkage.py -q` 通过，9 passed。
- validation: 临时目录 fake manifest/review/audit pass；missing audit warn；unsafe audit fail。未读取真实 reports / reviews，未写 DB 或 audit_logs。
- risks: linkage summary 不得被误读为 repair executed；不建议直接纳入 readiness 默认扫描；item-level / repair-level linkage 继续后置。
- next: Codex B 审核 Phase 2.27f 最小实现；通过后再执行 Git baseline。
- commit/tag if any: 无。

## 2026-04-27 14:49 Phase 2.27f
- goal: 修复 review audit linkage 对 audit event 顶层 unsafe 字段未检测的问题。
- changed_files:
  - `scripts/phase227f_review_audit_linkage.py`
  - `tests/test_phase227f_review_audit_linkage.py`
  - `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py` 通过；`uv run pytest tests/test_phase227f_review_audit_linkage.py -q` 通过，12 passed。
- validation: 临时目录 smoke 覆盖 sanitized pass、missing audit warn、unsafe result_json fail、unsafe top-level fail；未读取真实 reports / reviews，未写 DB 或 audit_logs。
- risks: `docs/NEXT_CODEX_A_PROMPT.md` 有既有 dirty 未处理；readiness 默认扫描与 item-level linkage 继续后置。
- next: Codex B 审核安全补丁；通过后再执行 Phase 2.27f Git baseline。
- commit/tag if any: 无。

## 2026-04-27 14:58 Phase 2.27f
- goal: 完成 archive / review / audit 只读 linkage summary 收口与 Git baseline。
- changed_files:
  - `scripts/phase227f_review_audit_linkage.py`
  - `tests/test_phase227f_review_audit_linkage.py`
  - `docs/PHASE227F_REVIEW_AUDIT_LINKAGE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests: `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py` 通过；`uv run pytest tests/test_phase227f_review_audit_linkage.py -q` 通过，12 passed。
- validation: baseline 范围仅包含 Phase 2.27f runner、测试、文档与交接文件；未写 DB、未写 `audit_logs`、未执行 repair。
- risks: linkage summary 不得被误读为 repair executed；readiness 默认扫描、item-level linkage 与 repair executor 继续后置。
- next: Phase 2.27g 路线规划：评审 linkage summary 是否显式参数化接入 readiness audit。
- commit/tag if any: tag `phase-2.27f-review-audit-linkage-baseline`；commit hash 以 Git 结果和 `reports/agent_runs/latest.json` 为准。

## 2026-04-27 15:07 Phase 2.27g
- goal: 规划 linkage summary 是否显式参数化接入 readiness audit。
- changed_files:
  - `docs/PHASE227G_LINKAGE_READINESS_ROUTE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮为 planning-only phase。已执行 `git status --short` 复核。
- validation: 已评审 A-E 候选方向；推荐 B + D，即显式参数化作为后续候选，同时纳入 Phase 2.29 人工 readiness freeze 清单。
- risks: 默认扫描真实 reports / reviews 可能泄露本机路径或人工审阅信息；repair executor 与 rollout 继续禁止。
- next: Codex B 审核 Phase 2.27g planning；通过后执行 planning baseline，再进入 Phase 2.29 MVP readiness freeze planning。
- commit/tag if any: 无。

## 2026-04-27 15:13 Phase 2.27g
- goal: 完成 linkage readiness route planning Git baseline。
- changed_files:
  - `docs/PHASE227G_LINKAGE_READINESS_ROUTE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests: 未运行 pytest；本轮为 planning baseline。执行 `git status --short` 与 `git check-ignore -v reports/agent_runs/latest.json` 复核。
- validation: baseline 范围仅包含 Phase 2.27g planning 文档与交接文件；未写功能代码、未写 DB、未写 `audit_logs`。
- risks: Phase 2.29 readiness freeze 不等于 rollout；后续若接入 readiness audit，必须显式参数化，不得默认扫描真实 reports / reviews。
- next: 进入 Phase 2.29 MVP readiness freeze planning。
- commit/tag if any: tag `phase-2.27g-linkage-readiness-route-baseline`；commit hash 以 Git 结果和 `reports/agent_runs/latest.json` 为准。

## 2026-04-27 Phase 2.27f Codex B Implementation Review
- goal: 检查项目进度，审核 Phase 2.27f 只读 linkage summary 最小实现。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py`：通过。
  - `uv run pytest tests/test_phase227f_review_audit_linkage.py -q`：`9 passed`。
  - Codex B 临时负例：audit event 顶层 `document_id` 当前错误返回 `status=pass`。
- validation: 实现总体符合只读 / no DB / no audit_logs 边界，但 unsafe 检测只覆盖 `request_json` / `result_json`，未覆盖 audit event 顶层敏感字段。
- risks: 顶层 `document_id`、`fact_id`、`report_path` 或绝对路径若未 fail，可能破坏 Phase 2.27f 的脱敏诊断边界。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27f 安全补丁任务；Codex A 执行后必须停止，不 baseline。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27f Safety Patch Review
- goal: 检查项目进度，审核 Phase 2.27f 顶层 audit unsafe 字段安全补丁。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase227f_review_audit_linkage.py`：通过。
  - `uv run pytest tests/test_phase227f_review_audit_linkage.py -q`：`12 passed`。
  - Codex B 负例复验：顶层 `document_id`、`fact_id`、`report_path` 均返回 `status=fail`。
- validation: 顶层 unsafe audit 字段漏口已关闭；输出 failure paths 不泄露真实敏感值；仍未写 DB、未写 `audit_logs`、未执行 repair。
- risks: linkage summary 仍不得被解释为 repair executed；readiness 默认扫描与 item-level linkage 继续后置。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27f Git baseline 任务；Codex A 执行后必须停止。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27f Baseline Check
- goal: 检查项目进度，确认 Phase 2.27f baseline，并生成 Phase 2.27g 路线规划任务。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.27f baseline 已完成，HEAD `b921361` 与 `origin/main` 对齐，tag `phase-2.27f-review-audit-linkage-baseline` 指向 HEAD。
- risks: 不应继续无限追加 2.27x；Phase 2.27g 应作为 linkage/readiness 关系的最后路线裁决子阶段，后续建议进入 Phase 2.29 MVP readiness freeze。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.27g 路线规划任务；只做文档，不写代码。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27g Codex B Review
- goal: 检查项目进度，审核 Phase 2.27g linkage readiness route planning。
- changed_files:
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做 Codex B review 与状态更新。
- validation: Phase 2.27g 规划边界安全，推荐 B + D：显式参数化作为后续候选，并纳入 Phase 2.29 MVP readiness freeze 人工验收项；禁止默认扫描真实 reports/reviews，禁止 repair executor / rollout。
- risks: 不应继续无限追加 Phase 2.27x；Phase 2.27g baseline 后建议进入 Phase 2.29。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已是 Phase 2.27g planning baseline 任务；Codex A 执行后必须停止，不进入 Phase 2.29 实现。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.27g Baseline Check
- goal: 检查项目进度，确认 Phase 2.27g baseline，并生成 Phase 2.29 MVP readiness freeze planning 任务。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.27g baseline 已完成，HEAD `9bd685c` 与 `origin/main` 对齐，tag `phase-2.27g-linkage-readiness-route-baseline` 指向 HEAD。
- risks: Phase 2.29 是 MVP readiness freeze planning，不等于 production rollout；不得继续无限追加 2.27x。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.29 MVP readiness freeze planning 任务；只做规划，不写代码。
- commit/tag if any: 无。

## 2026-04-27 15:29 Phase 2.29
- goal: 规划 MVP readiness freeze 边界、复验清单与 Go/No-Go 标准，不写功能代码。
- changed_files:
  - `docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；planning-only；已复核 `git status --short` 与 `git check-ignore -v reports/agent_runs/latest.json`
- validation: 已完成候选 MVP 能力盘点、复跑验证项、人工验收项、Go/No-Go 标准与后置范围划分；明确 readiness freeze 不等于 rollout；推荐下一步仅做 Phase 2.29a freeze checklist / freeze report dry-run
- risks: freeze 结论若缺少复验与人工验收，容易被误判为可直接 rollout；facts 仍不得替代 retrieval evidence 或 final answer
- next: Codex B 审核后执行 Phase 2.29 planning baseline；baseline 后再进入 Phase 2.29a
- commit/tag if any: 无。

## 2026-04-27 15:44 Phase 2.29 Baseline
- goal: Phase 2.29 MVP readiness freeze planning 收口与 Git baseline。
- changed_files:
  - `docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；planning baseline；已复核 `git status --short` 与 `git check-ignore -v reports/agent_runs/latest.json`
- validation: planning 文档、TODO/DEV_LOG、ACTIVE/HANDOFF/BACKLOG 均已进入 baseline；下一轮入口推进为 Phase 2.29a freeze checklist / freeze report dry-run。
- risks: Phase 2.29a 仍不得进入 rollout、repair executor、真实 reports/reviews 默认扫描或 facts 自动抽取。
- next: 执行 Phase 2.29a freeze checklist / freeze report dry-run。
- commit/tag if any: 见本轮 final 与 ignored latest.json。

## 2026-04-27 15:50 Phase 2.29a
- goal: 实现 MVP freeze checklist / freeze report dry-run，不写 DB、不执行 repair、不进入 rollout。
- changed_files:
  - `scripts/phase229a_freeze_report_dry_run.py`
  - `tests/test_phase229a_freeze_report_dry_run.py`
  - `docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile scripts/phase229a_freeze_report_dry_run.py`; `uv run pytest tests/test_phase229a_freeze_report_dry_run.py -q` -> 8 passed
- validation: 临时目录 fake eval/readiness/repair JSON dry-run 通过；输出保持 dry_run=true、destructive_actions=[]、rollout_ready=false、production_rollout=false、repair_executed=false；未读取真实 reports/reviews。
- risks: warn 状态需要人工判断；freeze report 不等于 production rollout ready；repair executor 和 facts 自动抽取继续后置。
- next: Codex B review 后执行 Phase 2.29a Git baseline。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.29a Codex B Review
- goal: 检查项目进度，审核 Phase 2.29a freeze report dry-run 最小实现。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase229a_freeze_report_dry_run.py`：通过。
  - `uv run pytest tests/test_phase229a_freeze_report_dry_run.py -q`：`8 passed`。
  - Codex B 负例复验：`repair_executed=true` 与 `production_rollout=true` evidence input 均返回 fail。
- validation: 实现保持只读；不默认扫描真实 reports/reviews；不写 DB；输出恒定 `rollout_ready=false`、`production_rollout=false`、`repair_executed=false`。
- risks: freeze report 不等于 production rollout ready；warn/fail 仍需人工判断，不得自动进入 rollout。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.29a Git baseline 任务；Codex A 执行后必须停止。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.29 Codex B Review
- goal: 检查项目进度，审核 Phase 2.29 MVP readiness freeze planning。
- changed_files:
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做 Codex B review 与状态更新。
- validation: Phase 2.29 规划边界正确，已从“继续补工具”切换到“冻结可验收 MVP 候选版本”；明确 readiness freeze 不等于 rollout，Phase 2.29a 仅建议 freeze checklist / freeze report dry-run。
- risks: freeze 结论不得被误读为 production ready；facts 仍不得替代 retrieval evidence；repair executor、facts 自动抽取、完整 RBAC/ABAC 与 rollout 继续后置。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已是 Phase 2.29 planning baseline 任务；Codex A 执行后必须停止，不进入 Phase 2.29a 实现。
- commit/tag if any: 无。

## 2026-04-27 16:00 Phase 2.29a Baseline
- goal: Phase 2.29a freeze report dry-run 收口与 Git baseline。
- changed_files:
  - `scripts/phase229a_freeze_report_dry_run.py`
  - `tests/test_phase229a_freeze_report_dry_run.py`
  - `docs/PHASE229_MVP_READINESS_FREEZE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile scripts/phase229a_freeze_report_dry_run.py`; `uv run pytest tests/test_phase229a_freeze_report_dry_run.py -q` -> 8 passed
- validation: staged 白名单仅包含 Phase 2.29a 文件；未写 DB、未读取真实 reports/reviews、未执行 rollout 或 repair；下一轮入口推进为 Phase 2.29b readiness freeze baseline decision planning。
- risks: freeze report 不等于 production rollout ready；warn/fail 仍需人工判断，不得自动进入 rollout。
- next: 进入 Phase 2.29b readiness freeze baseline decision planning。
- commit/tag if any: 见 final 与 ignored latest.json。

## 2026-04-27 16:14 Phase 2.29b
- goal: 规划 readiness freeze baseline decision，不写功能代码、不写 DB、不执行 rollout 或 repair。
- changed_files:
  - `docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；planning-only；已复核 `git status --short` 与 `git check-ignore -v reports/agent_runs/latest.json`
- validation: 明确 freeze report pass/warn/fail 映射；warn 必须人工确认；fail 必须 No-Go；Phase 2.29b 只生成 decision record / no-go reasons。
- risks: pass 不等于 production ready；warn 不得自动进入 MVP candidate；production rollout、repair executor、facts 替代 evidence、默认 reports/reviews 扫描和真实 DB mutation 均为 No-Go。
- next: Codex B 审核后执行 Phase 2.29b planning baseline；baseline 后实现 decision record dry-run。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.29b Codex B Review
- goal: 检查项目进度，审核 Phase 2.29b readiness freeze decision planning。
- changed_files:
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做 Codex B review 与状态更新。
- validation: Phase 2.29b 规划边界安全；只做 decision record/no-go reasons，禁止 rollout、repair executor、真实 DB mutation、默认扫描真实 reports/reviews 与 facts 替代 retrieval evidence。
- risks: `pass` 不等于 production ready；`warn` 不能自动进入 MVP candidate，必须人工确认。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已是 Phase 2.29b planning baseline 任务；Codex A 执行后必须停止，不进入实现。
- commit/tag if any: 无。

## 2026-04-27 16:22 Phase 2.29b Baseline
- goal: Phase 2.29b readiness freeze baseline decision planning 收口与 Git baseline。
- changed_files:
  - `docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；planning baseline；已复核 `git status --short` 与 `git check-ignore -v reports/agent_runs/latest.json`
- validation: planning 文档、TODO/DEV_LOG、ACTIVE/HANDOFF/BACKLOG 均进入 baseline；下一轮入口推进为 Phase 2.29b decision record dry-run 最小实现。
- risks: `pass` 不是 production ready；`warn` 不得自动进入 MVP candidate；任何 rollout、repair executor、真实 DB mutation 继续禁止。
- next: 执行 Phase 2.29b decision record dry-run 最小实现。
- commit/tag if any: 见 final 与 ignored latest.json。

## 2026-04-27 16:33 Phase 2.29b
- goal: 执行 NEXT_CODEX_A_PROMPT，完成 readiness freeze decision record dry-run 最小实现。
- changed_files:
  - `scripts/phase229b_freeze_decision_dry_run.py`
  - `tests/test_phase229b_freeze_decision_dry_run.py`
  - `docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile scripts/phase229b_freeze_decision_dry_run.py`; `uv run pytest tests/test_phase229b_freeze_decision_dry_run.py -q` -> 8 passed
- validation: 临时目录 pass / warn / fail dry-run smoke 通过；未读取真实 reports / reviews，未写 DB，未生成 rollout / repair 产物。
- risks: `pass` 只表示 MVP freeze candidate 候选资格，不等于 production rollout ready；`warn` 仍需人工确认；repair executor 继续后置。
- next: Codex B review 后执行 Phase 2.29b Git baseline。
- commit/tag if any: 无。

## 2026-04-27 16:53 Phase 2.29b Baseline
- goal: Phase 2.29b decision record dry-run 收口与 Git baseline。
- changed_files:
  - `scripts/phase229b_freeze_decision_dry_run.py`
  - `tests/test_phase229b_freeze_decision_dry_run.py`
  - `docs/PHASE229B_READINESS_FREEZE_DECISION_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile scripts/phase229b_freeze_decision_dry_run.py`; `uv run pytest tests/test_phase229b_freeze_decision_dry_run.py -q` -> 8 passed
- validation: `reports/agent_runs/latest.json` 已确认 ignored；baseline 未写 DB、未写 `audit_logs`、未执行 rollout 或 repair；下一轮入口推进为 Phase 2.29c 路线规划。
- risks: `pass` 不等于 production rollout ready；`warn` 不得自动进入 MVP candidate；repair executor 继续后置。
- next: 进入 Phase 2.29c MVP freeze candidate 人工复核 / release candidate checklist 路线规划。
- commit/tag if any: 见 final 与 ignored latest.json。

## 2026-04-27 Phase 2.29b Codex B Review
- goal: 检查项目进度，审核 Phase 2.29b decision record dry-run 最小实现。
- changed_files:
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase229b_freeze_decision_dry_run.py`：通过。
  - `uv run pytest tests/test_phase229b_freeze_decision_dry_run.py -q`：`8 passed`。
  - Codex B 临时 CLI smoke：pass -> approved_for_mvp_freeze_candidate；warn -> needs_manual_review；fail -> no_go。
- validation: 实现只读取显式 freeze report JSON；未读取真实 reports/reviews；未写 DB；未生成 rollout/repair 产物；输出保持 `dry_run=true`、`production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`。
- risks: `pass` 仍不等于 production ready；`warn` 仍需人工确认；repair executor 与 rollout 继续后置。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已是 Phase 2.29b Git baseline 任务；Codex A 执行后必须停止，不进入下一阶段。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.29b Baseline Check / 2.29c Drift Cleanup Prompt
- goal: 检查 Phase 2.29b baseline，并将 Codex D drift findings 转为下一轮 docs-only 修复任务。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.29b baseline 已完成，HEAD `f888aa7` 与 `origin/main` 对齐，tag `phase-2.29b-freeze-decision-dry-run-baseline` 指向 HEAD；下一轮入口改为 docs-only drift cleanup。
- risks: 文档漂移修复不得混入代码、测试、DB、rollout、repair executor 或真实 reports/reviews 扫描。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.29c docs drift cleanup 任务；Codex A 执行后必须停止等待 review。
- commit/tag if any: 无。

## 2026-04-27 17:05 Phase 2.29c
- goal: 执行 NEXT_CODEX_A_PROMPT，完成 TODO / Nightly Sprint Queue 历史状态漂移清理。
- changed_files:
  - `docs/TODO.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；docs-only；执行 `git status --short` 与限定文档 `git diff` 只读检查。
- validation: 旧 rerank、dense ingestion、Aliyun provider smoke、audit_logs 状态已改为历史状态并对齐后续 phase 完成事实；Nightly queue 已归档 2.27b/2.27c 旧任务。
- risks: docs drift cleanup 不等于 release candidate checklist；`--write-audit` opt-in 不等于 repair executed；production rollout 与 repair executor 继续后置。
- next: Codex B review 后执行 Phase 2.29c docs drift cleanup baseline。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.29c Baseline
- goal: Phase 2.29c docs drift cleanup 收口与 Git baseline。
- changed_files:
  - `docs/TODO.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；docs-only；复核 `git status --short`，未发现代码、脚本或测试变更。
- validation: Phase 2.29c 文档漂移修复进入 baseline；Nightly queue 标记 docs cleanup completed，并将下一项推进为 Phase 2.29d release candidate checklist planning。
- risks: baseline 不等于 release candidate 通过；production rollout、repair executor、DB mutation、default reports/reviews scan 继续禁止。
- next: 进入 Phase 2.29d MVP freeze candidate 人工复核 / release candidate checklist planning。
- commit/tag if any: 见 final 与 ignored latest.json。

## 2026-04-27 Phase 2.29c Codex B Review
- goal: 检查项目进度，审核 Phase 2.29c docs drift cleanup。
- changed_files:
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮 docs-only；Codex B 复核 `git diff` 确认仅涉及允许文档。
- validation: TODO 旧 rerank/dense/Aliyun/audit 状态已改为历史状态并对齐后续 phase；Nightly Sprint Queue 已归档 2.27 旧队列并切换到 Phase 2.29 docs-only / checklist planning 队列；无代码、脚本、测试、DB、索引或真实 reports/reviews 变更。
- risks: docs cleanup 不等于 release candidate checklist；release candidate planning 需在 baseline 后单独推进。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已是 Phase 2.29c docs drift cleanup Git baseline 任务；Codex A 执行后必须停止。
- commit/tag if any: 无。

## 2026-04-27 17:28 Phase 2.29d
- goal: 执行 NEXT_CODEX_A_PROMPT，完成 MVP freeze candidate 人工复核 / release candidate checklist 路线规划。
- changed_files:
  - `docs/PHASE229D_RELEASE_CANDIDATE_CHECKLIST_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；docs-only planning；执行 `git status --short`、限定文档 diff 与 ignored 状态检查。
- validation: release candidate checklist 已限定为只读证据与人工签核；明确 candidate 不等于 rollout，不执行 repair，不写 DB，不默认扫描真实 reports / reviews。
- risks: stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e` 继续保留为 warning；soft policy 不是完整 RBAC/ABAC；facts 不得替代 retrieval evidence。
- next: Codex B review 后执行 Phase 2.29d planning Git baseline；baseline 后再评审 Phase 2.29e checklist dry-run。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.29d Baseline
- goal: Phase 2.29d release candidate checklist planning 收口与 Git baseline。
- changed_files:
  - `docs/PHASE229D_RELEASE_CANDIDATE_CHECKLIST_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；docs-only planning baseline；复核 `git status --short`、ignored latest.json 与业务目录无变更。
- validation: Phase 2.29d planning 进入 baseline；未写代码、脚本、测试、DB、`audit_logs`、facts、versions、OpenSearch、Qdrant、reports/reviews 真实产物。
- risks: MVP freeze candidate checklist 不等于 production rollout；repair executor 与 DB mutation 继续禁止。
- next: 进入 Phase 2.29e checklist dry-run 最小实现规划 / 实现评审；不直接 rollout。
- commit/tag if any: 见 final 与 ignored latest.json。

## 2026-04-27 Phase 2.29d Codex B Review
- goal: 检查项目进度，审核 Phase 2.29d release candidate checklist planning。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮只做 Codex B review 与下一轮 baseline prompt 更新。
- validation: Phase 2.29d planning 边界安全；release candidate checklist 被限定为只读证据与人工签核，不等于 rollout；未写代码、DB、audit_logs、索引或真实 reports/reviews。
- risks: stale confirmed fact、soft policy、facts 不替代 evidence、专用 rerank key smoke 等 known risks 需继续保留；Phase 2.29e 若实现也只能 dry-run。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.29d planning baseline 任务；Codex A 执行后必须停止，不进入实现。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.30a Practical MVP Pilot Prompt
- goal: 用户要求加速进入公司实际可用 MVP，检查 Phase 2.29d baseline 后，将下一轮入口切换为 Practical MVP Pilot Pack。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行；本轮只做 Codex B 进度检查与下一轮文件化任务入口更新。
- validation: Phase 2.29d baseline 已完成，HEAD `7060d38` 与 `origin/main` 对齐；下一轮不继续堆 readiness 文档，而是面向审标、文件提取和公司方向分析整理实用 MVP pilot。
- risks: Practical MVP Pilot 仍不是 production rollout；所有输出必须保留 evidence/citation，facts 不得替代 retrieval evidence。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.30a Practical MVP Pilot Pack；Codex A 执行后必须停止等待 review。
- commit/tag if any: 无。

## 2026-04-27 18:09 Phase 2.30a
- goal: 执行 NEXT_CODEX_A_PROMPT，整理内部受控 Practical MVP Pilot Pack。
- changed_files:
  - `docs/PHASE230_PRACTICAL_MVP_PILOT_PLAN.md`
  - `docs/MVP_PILOT_RUNBOOK.md`
  - `docs/MVP_TENDER_REVIEW_PLAYBOOK.md`
  - `docs/MVP_FILE_EXTRACTION_PLAYBOOK.md`
  - `docs/MVP_STRATEGY_ANALYSIS_PLAYBOOK.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；docs-only；执行 `git status --short` 并确认无代码、脚本、测试变更。
- validation: 已形成标书审查、文件提取、公司方向辅助分析 playbook 与 12 条 Codex C 验收 query；明确 Pilot 不是 rollout，facts 不替代 evidence。
- risks: 真实终端验收尚未执行；发展方向建议必须人工决策；无 evidence 不得给确定结论。
- next: Codex B review 后交给 Codex C 执行 12 条 Pilot query；通过后再做 docs baseline。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.30a Codex B Review
- goal: 检查项目进度，审核 Practical MVP Pilot Pack 是否可进入 Codex C 真实终端验收。
- changed_files:
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮 docs-only review。Codex B 复核 pilot plan、runbook、tender/file/strategy playbook 与 git status，确认无代码、脚本、测试、DB、索引或真实 reports/reviews 变更。
- validation: 2.30a 文档包覆盖审标、文件提取、公司方向辅助分析；包含 12 条 pilot query、Codex C 回传字段与 pass/fail 判定；明确 Pilot 不等于 rollout，facts 不替代 retrieval evidence。
- risks: 真实终端验收尚未执行；发展方向建议必须人工决策；无 evidence 不得给确定结论。
- next: 交给 Codex C 按 `docs/MVP_PILOT_RUNBOOK.md` 与 `docs/PHASE230_PRACTICAL_MVP_PILOT_PLAN.md` 执行 12 条真实终端验收；通过后再做 Phase 2.30a docs baseline。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.30a Codex C Validation Review
- goal: 吸收 Codex C 12 条真实终端验收结果，并决定是否允许 Phase 2.30a baseline / 内部 Pilot。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮为 Codex B review / prompt handoff。
- validation: Codex C 验收结果为 `4/12 pass, 8 partial, 0 failed`；API / Hermes CLI 可用；未出现 facts 替代 evidence、transcript 误作 fact 或第三文件污染；Excel/PPTX 在标题检索下可返回 structured citation。
- risks: `@硬件清单`、`@会议纪要`、`@C塔方案` alias / session scope 不稳定；`retrieval_suppressed=true` 可能阻断显式 alias 绑定 / 使用；主标书深层召回和 PPTX Slide 1 仍是后续质量尾项。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.30b alias/session stability fix；Codex A 完成后需 Codex B review，再交给 Codex C 复跑 12 条 Pilot query。
- commit/tag if any: 无。

## 2026-04-27 20:55 Phase 2.30b
- goal: 修复 Practical MVP Pilot 中标题类 alias 绑定 / session 稳定性阻塞。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: py_compile 通过；主仓库 venv 缺 pytest；direct assertion tests 覆盖 `test_session_document_scope.py` 与 `test_phase214b_cli_smoke_eval.py`，48 个测试函数通过。
- validation: 标题 alias bind resolver 未命中时不再 suppress retrieval；同轮 retrieval 唯一命中文档后完成 alias bind；missing alias suppress 规则保持不变。
- risks: 真实 Hermes CLI smoke 未执行；仍需 Codex C 复跑 12 条 Pilot query。深层召回质量尾项不属于本轮。
- next: Codex B review 代码 diff；Codex C 验证 `@硬件清单`、`@会议纪要`、`@C塔方案` 与 alias compare。
- commit/tag if any: 无。

## 2026-04-27 21:38 Phase 2.30b
- goal: 补齐 Codex B review 指出的无书名号 / 自然语言标题 alias 绑定缺口。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: py_compile 通过；pytest 不可用；direct assertion tests 覆盖 `test_session_document_scope.py` 与 `test_phase214b_cli_smoke_eval.py`，53 个测试函数通过。
- validation: `把会议纪要文件设为 @会议纪要`、`把硬件清单设为 @硬件清单`、`把C塔方案设为 @C塔方案`、`把当前主标书设为 @主标书`、`把当前标书设为 @主标书` 已纳入测试覆盖。
- risks: 未做真实 Hermes CLI 复验；仍需 Codex B review 后交给 Codex C 复跑 12 条 Pilot。
- next: Codex B review follow-up diff；通过后 Codex C 复验 alias/session 稳定性。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.30b Codex B Review
- goal: 审核 Codex A 的 alias/session 修复是否足以交给 Codex C 复跑 Pilot。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 复跑主仓库 py_compile 通过；手动执行新增 3 个 title-bind fallback 测试函数通过。
- validation: 2.30b 原修复方向正确，但测试只覆盖 `把《标题》设为 @alias`。Pilot runbook 的真实 prompt 是 `把会议纪要文件设为 @会议纪要`、`把当前主标书设为 @主标书` 等无书名号自然语言形式；当前 `_extract_title_candidates()` 仍可能无法抽取 title，导致继续 suppress retrieval。
- risks: 若不补齐无书名号 alias bind，Codex C 复验大概率仍会出现 `@会议纪要` / `@硬件清单` / `@C塔方案` alias_missing。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.30b review follow-up，要求 Codex A 补齐真实 runbook alias prompt 测试与实现；暂不交给 Codex C，暂不 baseline。
- commit/tag if any: 无。

## 2026-04-27 Phase 2.30b Codex B Follow-up Review
- goal: 复核 Codex A 补齐无书名号 / 自然语言 alias bind 后是否可进入 Codex C 复验。
- changed_files:
  - `reports/agent_runs/latest.json`
  - `docs/HANDOFF_LOG.md`
- tests: Codex B 复跑主仓库 py_compile 通过；直接执行 `test_session_document_scope.py` 与 `test_phase214b_cli_smoke_eval.py` 中 53 个测试函数，全部通过；`latest.json` JSON 校验与 ignore 校验通过。
- validation: follow-up 已覆盖 `把会议纪要文件设为 @会议纪要`、`把硬件清单设为 @硬件清单`、`把C塔方案设为 @C塔方案`、`把当前主标书设为 @主标书`、`把当前标书设为 @主标书`；missing alias suppress 语义保持不变。
- risks: 真实 Hermes CLI 仍未复验；主仓库 venv 缺 pytest，采用 direct assertion tests；深层召回质量尾项和 PPTX Slide 1 不属于 2.30b。
- next: 交给 Codex C 复跑 12 条 Pilot query，重点检查 `@硬件清单`、`@会议纪要`、`@C塔方案` 与 `@会议纪要 vs @主标书` alias/session 稳定性；通过后再进入 baseline。
- commit/tag if any: 无。

## 2026-04-28 Phase 2.30b Codex C Validation Passed
- goal: 吸收 Codex C 真实终端复验结果，并授权 Phase 2.30a / 2.30b baseline。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮未跑 pytest；依据 Codex C 真实终端复验：12 条 Pilot query 为 `10/12 pass, 2 partial, 0 failed`。
- validation: 四个 alias 在同一 session 后续 query 中均稳定；未再出现 `alias_missing` 或 `retrieval_suppressed` 误阻断；`facts_as_answer=false`、`transcript_as_fact=false` 全部稳定；compare 无第三文件污染。
- risks: partial 为召回质量尾项：最高投标限价、业绩要求未被当前召回覆盖；公司方向分析中主标书 / 硬件清单对战略方向直接证据不足。内部试用仍需人工复核和人工决策，不等于 production rollout。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已切换为 Phase 2.30a / 2.30b 双仓库 Git baseline；`docs/NIGHTLY_SPRINT_QUEUE.md` 已允许 Codex A 夜间自动模式执行该 Yellow Lane baseline，完成后必须停止。
- commit/tag if any: 无。

## 2026-04-28 Phase 2.30 Baseline Review / Phase 2.31 Prompt
- goal: 检查 Nightly Sprint baseline 是否完成，并推进下一轮内部受控 MVP Pilot 操作规划入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮只做状态检查与下一轮 prompt 更新。
- validation: Hermes_memory commit `15e05d4`、Hermes 主仓库 commit `13097693`、tag `phase-2.30b-practical-mvp-pilot-baseline` 均已存在；Hermes_memory 工作区干净，主仓库仅保留既存无关 dirty。
- risks: Phase 2.31 只能规划内部受控试用，不能进入 production rollout；深层召回和经营建议仍需人工复核。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已改为 Phase 2.31 internal controlled MVP Pilot operations planning；`docs/NIGHTLY_SPRINT_QUEUE.md` 已将 Phase 2.30 baseline 归档，并把 Phase 2.31 planning 设为 next Green Lane。
- commit/tag if any: 无。

## 2026-04-28 02:33 Phase 2.31
- goal: 完成内部受控 MVP Pilot 试用操作规划。
- changed_files:
  - `docs/PHASE231_INTERNAL_MVP_PILOT_OPERATIONS_PLAN.md`
  - `docs/MVP_PILOT_USER_GUIDE.md`
  - `docs/MVP_PILOT_FEEDBACK_TEMPLATE.md`
  - `docs/MVP_PILOT_KNOWN_RISKS.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮 docs-only；执行 `git status --short` 并确认 `reports/agent_runs/latest.json` 仍被 ignore。
- validation: 已定义试用范围、角色职责、每次使用流程、人工复核标准、反馈模板、known risks 与 1-2 天最小成功标准；未写代码、未写 DB、未改索引、未进入 rollout。
- risks: 深层字段召回仍需人工复核；经营建议必须人工决策；soft ACL 不是完整 RBAC/ABAC；当前仍非 production rollout。
- next: Codex B review Phase 2.31 文档；通过后再做 docs baseline。
- commit/tag if any: 无。

## 2026-04-28 02:46 Phase 2.31 Codex B Review / Nightly Launcher
- goal: 审核 Phase 2.31 内部受控 MVP Pilot 文档，并修正 Nightly Sprint “有协议但不会自动推进”的可操作性缺口。
- changed_files:
  - `docs/NIGHTLY_CODEX_A_PROMPT.md`
  - `docs/NIGHTLY_SPRINT_PROTOCOL.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/AGENT_OPERATING_PROTOCOL.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 仅读取与复核文档；后续需运行 `git status --short` 与 ignore 检查。
- validation: Phase 2.31 docs-only planning 内容符合 MVP Pilot 边界；Nightly Sprint 当前不能自行唤醒 Codex A，必须由用户睡前启动 Codex A 执行 `docs/NIGHTLY_CODEX_A_PROMPT.md`。
- risks: 仍不创建 production cron / scheduler；若没有正在运行的 Codex A 会话，夜间队列不会执行。
- next: Codex A 可执行 `docs/NIGHTLY_CODEX_A_PROMPT.md`。队列 Item 1 为 docs-only baseline；成功后可继续 Item 2 Phase 2.32 feedback intake planning。
- commit/tag if any: 无。

## 2026-04-28 03:01 Phase 2.31 / 2.32 Nightly Sprint
- goal: 执行 `docs/NIGHTLY_CODEX_A_PROMPT.md`，完成 Phase 2.31 docs baseline，并继续 Phase 2.32 feedback intake planning。
- changed_files:
  - `docs/PHASE232_MVP_PILOT_FEEDBACK_INTAKE_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
  - `reports/nightly_runs/20260428_030111.json`
- tests: 未运行 pytest；docs-only / planning；执行 `git status --short` 与 ignore 检查。
- validation: Phase 2.31 docs-only baseline 完成并推送；Phase 2.32 已规划 feedback intake 来源、triage 字段、P0/P1/P2/P3、Go/No-Go 与非目标；未写代码、未写 DB、未执行 repair、未进入 rollout。
- risks: feedback intake 当前仍是人工流程，不是自动 issue / repair 系统；P0/P1 需 Codex B review，必要时 Codex C 复验。
- next: 停止等待 Codex B review Phase 2.32；通过后再做 docs-only baseline。
- commit/tag if any: `184533a` / `phase-2.31-pilot-ops-nightly-launcher-baseline`。

## 2026-04-28 Phase 2.32 Codex B Review
- goal: 审核 Nightly Sprint 执行结果，确认 Phase 2.32 feedback intake planning 是否符合 PRD / Pilot 边界，并准备 baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: `git status --short`、`git diff --check`、`python3 -m json.tool reports/agent_runs/latest.json`、`python3 -m json.tool reports/nightly_runs/20260428_030111.json`、ignore 检查均已核验。
- validation: Nightly Sprint 按队列完成 Item 1 与 Item 2：Phase 2.31 baseline 已推送，Phase 2.32 planning docs-only 完成并停止等待 B review；未写代码、未写 DB、未改索引、未进入 repair 或 rollout。
- risks: Phase 2.32 仍是人工反馈分诊流程，不是自动 issue / repair 系统；P0/P1 反馈后仍需 Codex B 和必要时 Codex C。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已写入 Phase 2.32 docs-only baseline 任务；执行后停止等待 Codex B。
- commit/tag if any: 无。

## 2026-04-28 Phase 2.32 Baseline Review / Phase 2.33 Prompt
- goal: 检查 Phase 2.32 docs baseline 是否完成，并准备 Phase 2.33 Day-1 Pilot execution packet 入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: `git status --short`、`git diff --check`、ignore 检查与 latest/nightly JSON 校验均已执行。
- validation: Phase 2.32 baseline 已完成：commit `160ce62`，tag `phase-2.32-feedback-intake-plan-baseline`；未发现代码、DB、索引、repair 或 rollout 越界。
- risks: 下一阶段仍必须保持内部受控 Pilot；Day-1 run sheet 只能组织试用流程，不得解释为 production rollout。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已写入 Phase 2.33 Day-1 execution packet docs-only planning。
- commit/tag if any: 无。

## 2026-04-28 15:32 Phase 2.33
- goal: 完成内部 MVP Pilot Day-1 execution packet docs-only planning。
- changed_files:
  - `docs/MVP_PILOT_DAY1_RUN_SHEET.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮 docs-only；执行 `git status --short` 并确认 `reports/agent_runs/latest.json` 仍被 ignore。
- validation: Day-1 run sheet 已覆盖目标 / 非目标、角色、时间表、alias 绑定、10 条最小 query set、输出保存字段、人工复核、问题分级与 Go / Pause；未写代码、未写 DB、未改索引、未进入 rollout。
- risks: Pilot 仍依赖人工保存输出与人工复核；深层字段召回、经营建议和 soft ACL 风险继续保留；Phase 2.33 需 Codex B review 后再 baseline。
- next: Codex B review `docs/MVP_PILOT_DAY1_RUN_SHEET.md`；通过后执行 docs-only baseline，不自动进入真实 rollout。
- commit/tag if any: 无。

## 2026-04-28 15:53 Phase 2.33 Baseline
- goal: 执行 Phase 2.33 Day-1 run sheet docs-only Git baseline。
- changed_files:
  - `docs/MVP_PILOT_DAY1_RUN_SHEET.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
- tests: `git status --short`、`git diff --check`、`git check-ignore -v reports/agent_runs/latest.json`、`git check-ignore -v reports/nightly_runs/test.json`。
- validation: Dirty 文件限定为 Phase 2.33 文档白名单；未写代码、未运行 pytest、未写 DB、未改索引、未进入 repair 或 rollout。
- risks: baseline 后不得自动进入真实 Pilot 或 Phase 2.34；Day-1 仍需人工复核 citation、facts/transcript 边界与 contamination。
- next: 完成 commit/tag/push 后停止，交 Codex B 检查 Git 状态。
- commit/tag if any: commit hash 记录在最终报告与 ignored `reports/agent_runs/latest.json`；tag `phase-2.33-pilot-day1-run-sheet-baseline`。

## 2026-04-28 Phase 2.33 Codex B Review
- goal: 审核 Day-1 run sheet 是否符合内部受控 MVP Pilot 边界，并准备 docs-only baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`
- tests: `git status --short`、`git diff --check`、`python3 -m json.tool reports/agent_runs/latest.json` 与 ignore 检查均已执行。
- validation: Day-1 run sheet 覆盖目标、非目标、角色、时间表、alias 绑定、10 条最小 query set、输出保存、人工复核、P0/P1 分级与 Go / Pause；未发现 rollout、repair、DB、索引或代码越界。
- risks: Day-1 仍依赖人工保存输出和人工复核；深层字段召回与经营建议仍需人工确认。
- next: `docs/NEXT_CODEX_A_PROMPT.md` 已写入 Phase 2.33 docs-only baseline 任务；执行后停止等待 Codex B。
- commit/tag if any: 无。

## 2026-04-28 16:42 Phase 2.34 Codex B Intake
- goal: 吸收 Codex C Day-1 Pilot 真实终端验收报告，并写入 Phase 2.34 bounded fix 任务入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮为 Codex B intake / prompt handoff。
- validation: Codex C Day-1 结果为 `7 pass / 3 partial / 0 fail`，P0 为 `0`；`@主标书`、`@硬件清单`、`@C塔方案`、`@会议纪要` 四个 alias 均稳定；未出现 facts 替代 evidence、transcript_as_fact 或实际第三文件污染。
- risks: Q1/Q2 主标书深层字段召回仍为 P1 backlog；Q8 compare 输出层误报 `third_document_mixed=true` 是当前 Phase 2.34 bounded fix；Q7/Q10 长输出延迟为 P2 backlog。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只修 Q8 compare false-positive；完成后交 Codex B review，再由 Codex C 复验。
- commit/tag if any: 无。

## 2026-04-28 17:21 Phase 2.34
- goal: 修复 Day-1 Query 8 compare 第三文件污染标记误报。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: py_compile 通过；主仓库 venv 缺 pytest；direct assertion selected tests 7 passed；zero-arg direct assertion tests 43 passed；tmp_path direct assertion tests 9 passed。
- validation: 最终 evidence 均在 compare 文档集合内时 `third_document_mixed=false`；真实第三文档 evidence 仍触发 `unexpected_document_id`；候选过滤仅作为 `out_of_scope_document_ids_filtered` 诊断。
- risks: Q1/Q2 主标书深层字段召回仍为 P1 backlog；Q7/Q10 延迟仍为 P2 backlog；需要 Codex C 真实终端复验 Q8。
- next: Codex B review 代码与测试结果；Codex C 复验 Q8 compare 和 facts/transcript 边界。
- commit/tag if any: 无。

## 2026-04-28 17:59 Phase 2.34 Validation
- goal: 吸收 Codex C 真实终端复验结果，并准备 Phase 2.34 Git baseline 入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮未新增测试；沿用 Phase 2.34 代码层 direct assertion 结果与 Codex C 真实终端复验。
- validation: API `/health` 与 Hermes CLI 可用；session `20260428_174853_31a315`；`@主标书` 与 `@会议纪要` 绑定成功；Q8 compare 输出 `third_document_mixed=false`、`third_document_mixed_document_ids=[]`、`contaminationflags=none`；facts/transcript 抽样保持 false。
- risks: Q1/Q2 主标书深层字段召回仍为 P1 backlog；Q7/Q10 延迟仍为 P2 backlog；baseline 不等于 rollout。
- next: 执行 Phase 2.34 双仓 Git baseline，提交白名单文件并停止等待 Codex B。
- commit/tag if any: 无。

## 2026-04-28 Phase 2.35 Codex B Intake
- goal: 检查 Phase 2.34 baseline 状态，并进入 Phase 2.35 主标书深层字段召回专项。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未运行 pytest；本轮为 Codex B 阶段切换 / prompt handoff。
- validation: Phase 2.34 baseline 已完成：Hermes_memory commit `789ed22`，Hermes 主仓库 commit `5de49bf5`，tag `phase-2.34-compare-contamination-baseline`；Hermes_memory 工作区干净，Hermes 主仓库仅剩既有无关 dirty。
- risks: Phase 2.35 容易扩成完整自动审标，必须限定为 retrieval evidence 改善；若 evidence 不足，继续输出 Missing Evidence。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只在 Hermes_memory 做 diagnostic-first 最小实现；完成后交 Codex B review，必要时 Codex C 复验 Day-1 Q1/Q2。
- commit/tag if any: 无。

## 2026-04-28 18:49 Phase 2.35
- goal: 执行主标书深层字段召回专项 diagnostic-first 最小实现。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `tests/test_tender_metadata_retrieval.py`
  - `tests/test_phase235_tender_deep_field_retrieval.py`
  - `docs/PHASE235_TENDER_DEEP_FIELD_RETRIEVAL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: py_compile 通过；`uv run pytest tests/test_tender_metadata_retrieval.py tests/test_retrieval_contract.py tests/test_phase235_tender_deep_field_retrieval.py -q` 为 `22 passed`。
- validation: 新增 price ceiling 与 qualification deep-field metadata anchors；扩展 section scope 与 phrase boosts；新增 deep-field trace；snapshot 仍为导航，`snapshot_as_answer=false`。
- risks: 未做真实 Hermes CLI 复验；若真实文本未解析或未索引，仍应 Missing Evidence；本阶段不是自动审标。
- next: Codex B review；通过后建议 Codex C 复验 Day-1 Q1/Q2，再决定 Phase 2.35 baseline。
- commit/tag if any: 无。

## 2026-04-28 Phase 2.35 Codex C Validation Intake
- goal: 吸收 Phase 2.35 真实终端复验结果，并准备 bounded follow-up。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮未运行 pytest；Codex C 复验只读执行，未修改代码、文档、DB 或索引。
- validation: Q1 基础字段通过，但最高投标限价 / 招标控制价 / 投标报价上限仍 Missing Evidence；Q2 投标资质 fail，项目经理 / 联合体 / 业绩 / 人员要求 partial；无编造金额、资质、业绩或人员数量。
- risks: 终端 trace 显示 `deep_field_profile=single_pass`，需与 retrieval profile 对齐；首次 session 出现 alias 绑定后丢失，第二次 session 正常，需诊断但不应盲目大改。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，做 Phase 2.35b trace/profile 对齐、metadata precision、alias 首次绑定诊断。
- commit/tag if any: 无。

## 2026-04-28 Phase 2.35b
- goal: 执行 Phase 2.35b bounded follow-up：trace/profile 对齐、metadata precision 修复、alias 首次绑定诊断。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `tests/test_tender_metadata_retrieval.py`
  - `docs/PHASE235_TENDER_DEEP_FIELD_RETRIEVAL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py -q` 为 `13 passed`；`uv run pytest tests/test_tender_metadata_retrieval.py tests/test_retrieval_contract.py tests/test_phase235_tender_deep_field_retrieval.py -q` 为 `26 passed`；py_compile 与 `git diff --check` 通过；主仓库 alias direct assertion diagnostics 10 passed。
- validation: API trace 顶层新增 metadata profile/status；price ceiling strong match 要求具体金额；qualification strong match 要求资质等级 + 类别；alias 首次绑定问题未在 direct assertion 中复现。
- risks: 若 Codex C 仍看到 `deep_field_profile=single_pass`，可能是 Hermes 主仓库展示 / adapter flattening 问题；真实标书没有具体金额或资质等级时仍应 Missing Evidence。
- next: 交 Codex B review；通过后由 Codex C 重跑 Day-1 Q1/Q2。
- commit/tag if any: 无。

## 2026-04-29 Phase 2.35c Codex B Intake
- goal: 吸收 Codex C Phase 2.35b 真实终端复验失败，并写入 alias/session 最小修复入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B 交接，不运行 pytest；已读取主仓 alias/session 相关入口与 AGENTS.md。
- validation: Codex C session `20260429_024717_785309` 中，`@主标书` bind 输出 document/version 正确，但正式 Q1/Q2 均为 `alias_missing=true / retrieval_suppressed=true`，未进入 retrieval，因此无法验证 Phase 2.35b deep-field trace。
- risks: 若盲目 baseline，会把一个无法进入 Q1/Q2 retrieval 的 Pilot 阻塞带入基线；下一轮必须先修主仓 alias/session。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做主仓库 alias/session 最小修复；完成后 Codex B review，再由 Codex C 重跑 Day-1 Q1/Q2。
- commit/tag if any: 无。

## 2026-04-29 16:36 Phase 2.35c
- goal: 执行主仓库 alias/session 最小修复，解决 `@主标书` bind 成功后正式 Q1/Q2 变成 `alias_missing / retrieval_suppressed` 的阻断问题。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/PHASE235_TENDER_DEEP_FIELD_RETRIEVAL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 主仓库 py_compile 通过；主仓库 `.venv` 缺 pytest，改用 6 个 direct assertion tests 覆盖新增 / 相邻 alias 路径并通过；Hermes_memory Phase 2.35 目标 pytest `13 passed`。
- validation: 只读检查真实 state，Codex C session `20260429_024717_785309` 未持久化 `@主标书`；修复将“上一轮已锁定的当前文件”等说法纳入 current-document bind / retrieval fallback，并验证跨 store resume 可 resolve。
- risks: 尚未做真实 Hermes CLI 复验；Phase 2.35b deep-field 效果仍需 Codex C 重跑 Day-1 Q1/Q2。
- next: Codex B review；通过后 Codex C 重新执行 `@主标书` 绑定与 Day-1 Q1/Q2，确认不再 alias_missing / retrieval_suppressed。
- commit/tag if any: 无。

## 2026-04-29 16:58 Phase 2.35c Codex C Validation
- goal: 吸收 Phase 2.35c 真实终端复验结果，判断 alias/session 修复与 baseline 条件。
- changed_files:
  - `docs/PHASE235_TENDER_DEEP_FIELD_RETRIEVAL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
- tests: 本轮未新增测试；Codex C 真实终端复验只读执行，未写代码、文档、DB、索引或提交。
- validation: session `20260429_165301_e3c312` 中 `@主标书` bind 后正式 Q1/Q2 均为 `alias_resolved`，`alias_missing=false`，`retrieval_suppressed=false`；evidence 仅来自主标书。
- risks: 限价具体金额、资质具体等级 / 类别、类似业绩、人员要求仍为 retrieval recall 尾项；`metadata_deep_field_profile=null` 与 `deep_field_profile=single_pass` 仍需后续 trace/display 处理。
- next: 建议执行 Phase 2.35c Git baseline，但结论口径必须限定为 alias/session 修复已收口，不得写成 deep-field recall 完全收口。
- commit/tag if any: 无。

## 2026-04-29 17:17 Phase 2.35c Baseline Prep
- goal: 复跑 Phase 2.35c baseline 前验证，并准备 Git baseline。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `tests/test_tender_metadata_retrieval.py`
  - `tests/test_phase235_tender_deep_field_retrieval.py`
  - `docs/PHASE235_TENDER_DEEP_FIELD_RETRIEVAL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
- tests: Hermes_memory targeted regression `26 passed`; Hermes main session scope regression `48 passed`; both repos `git diff --check` passed.
- validation: Codex C real terminal validation already passed for alias/session; deep-field recall remains partial and must be recorded as tail work.
- risks: Do not stage main repo `uv.lock`, `docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`, or `tests/agent/test_memory_kernel_adapter_reload.py`.
- next: Commit/tag/push Phase 2.35c baseline in both repos; keep baseline wording bounded.
- commit/tag if any: pending.

## 2026-04-29 17:46 Phase 2.36
- goal: 规划主标书 deep-field recall / trace tail item 收敛方案。
- changed_files:
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: docs-only planning，未运行 pytest；未运行真实 API / CLI smoke。
- validation: Phase 2.35c alias/session baseline 已完成；规划按 price ceiling、qualification、project manager、consortium、performance、personnel 与 trace display 分类剩余 tail items。
- risks: 限价金额、资质等级 / 类别、业绩、人员要求仍可能是真实源文缺字段；必须继续保留 Missing Evidence，不得编造。
- next: Codex B review；通过后建议 Phase 2.36a 做 trace polish + section-targeted retrieval diagnostics。
- commit/tag if any: 无。

## 2026-04-30 09:20 Phase 2.36a Codex B Review
- goal: 审核 Phase 2.36a retrieval-layer trace polish + diagnostics 实现，并决定是否可 baseline。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `tests/test_phase236_tender_deep_field_trace.py`
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: `uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py` passed；`uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py tests/test_retrieval_contract.py -q` => `30 passed`；`git diff --check` passed。
- validation: 代码层 review 通过。实现稳定输出 `metadata_deep_field_profile`、`deep_field_profile`、`deep_field_section_hints`、`deep_field_query_aliases`、`deep_field_missing_reason`、`deep_field_diagnostics`，并用 fixture 区分 concrete evidence 与 placeholder / generic evidence。
- risks: 当前只证明 Hermes_memory retrieval-layer trace；若真实 CLI 仍显示 `metadata_deep_field_profile=null` 或 `deep_field_profile=single_pass`，则需要单独授权 Hermes 主仓库 adapter/context trace display follow-up。
- next: 建议 Codex C 只做 `@主标书` Q1/Q2 terminal-visible trace 抽样；通过后再执行 Phase 2.36a Git baseline。
- commit/tag if any: 无。

## 2026-04-30 09:55 Phase 2.36a Codex C Trace Sampling
- goal: 吸收 Codex C 真实终端抽样结果，判断 Phase 2.36a 是否可 baseline。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B 交接，不运行 pytest。
- validation: Codex C fallback session `20260430_005108_6db393` 中 Q1/Q2 alias 已 resolved，evidence 仅主标书，`snapshot_as_answer=false`、`facts_as_answer=false`、`transcript_as_fact=false`，无编造。
- risks: 终端 trace 仍未透出 Hermes_memory 新字段：`metadata_deep_field_profile=null`、`deep_field_profile=null`、`deep_field_diagnostics=null`，`query_aliases` 只显示 `主标书`。指定一步绑定 prompt session `20260430_005006_4ad0a0` 仍 `alias_missing=true / retrieval_suppressed=true`。
- next: 不 baseline Phase 2.36a；进入 Phase 2.36b，修复 Hermes 主仓库 adapter/kernel/context_builder trace 映射与 `绑定为 @alias` / 中文弯引号 title alias binding。
- commit/tag if any: 无。

## 2026-04-30 10:18 Phase 2.36b Codex B Review
- goal: 审核 Phase 2.36b 主仓 trace display / alias prompt handling 实现，并决定是否可交 Codex C。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/adapters/hermes_memory_adapter.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 主仓 `./.venv/bin/python -m py_compile agent/memory_kernel/adapters/hermes_memory_adapter.py agent/memory_kernel/kernel.py agent/memory_kernel/context_builder.py agent/memory_kernel/session_document_scope.py` passed；主仓 `./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py -q` => `59 passed`；两仓 `git diff --check` passed。
- validation: Codex B review 通过。主仓已补 deep-field trace flatten / promotion / context rendering；alias parser 已覆盖 `绑定为`、`绑定成` 与中文弯引号标题。
- risks: 仍需 Codex C 真实终端复验，确认 Step 1 一步绑定与 Q1/Q2 terminal-visible trace 实际通过。不得将当前实现误写为 deep-field recall 完整收口。
- next: Codex C 重跑 Step 1 / Q1 / Q2 抽样；若通过，再进入 Phase 2.36b Git baseline。
- commit/tag if any: 无。

## 2026-04-30 10:42 Phase 2.36b Codex C Validation
- goal: 吸收 Codex C 真实终端复验结果，判断 Phase 2.36b 是否可 baseline。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B 交接，不运行 pytest。
- validation: Codex C session `20260430_020429_7517f4` 中 Step 1 一步 alias binding 已通过；Q1/Q2 terminal-visible trace 已显示 `pricing_scope` / `qualification_scope`、deep-field aliases 与 diagnostics；安全边界保持 false/false/false。
- risks: 暂不 baseline。Q1 diagnostics 显示 concrete found / present=true，但答案仍为限价 Missing Evidence，存在 trace / answer boundary 不一致；Q2 将“一级注册建造师电子证书要求”表述为“项目经理=一级注册建造师”，存在过度解释风险。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，做 Phase 2.36c diagnostics / answer boundary semantic consistency 最小修复。
- commit/tag if any: 无。

## 2026-04-29 17:55 Phase 2.36 Codex B Review
- goal: 审核 Phase 2.36 planning，并写入 Phase 2.36a 最小实现任务入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B review / prompt handoff，不运行 pytest。
- validation: `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md` 分类清晰，保持 Missing Evidence 口径，未要求自动审标、rollout、DB 或索引变更；允许进入 bounded Phase 2.36a。
- risks: Phase 2.36a 只能补 trace polish 与 diagnostics，不能宣称 deep-field recall 完全收口；若发现 terminal-visible trace 卡在 Hermes 主仓库，需要停止并回交，不要直接改主仓库。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，实现 Hermes_memory 侧 trace polish + section-targeted retrieval diagnostics，并运行目标测试。
- commit/tag if any: 无。

## 2026-04-29 17:35 Phase 2.35c Baseline Review / Phase 2.36 Prompt
- goal: 检查 Phase 2.35c baseline 状态，并将下一轮安全任务切换到 Phase 2.36 deep-field recall / trace tail planning。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B 检查与交接，不运行 pytest。
- validation: Hermes_memory HEAD `ec77c96` 已打 tag `phase-2.35c-alias-session-baseline`；Hermes 主仓库 HEAD `ead4e899` 已打同名 tag。`reports/agent_runs/latest.json` 标记 Phase 2.35c baseline 已完成并 pushed。
- risks: Deep-field recall 仍 partial；限价具体金额、资质等级 / 类别、类似业绩、人员要求仍不得编造。主仓库既有无关 dirty 仍不得混入后续提交。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.36 路线规划与文档同步；不写功能代码、不跑真实 smoke、不提交 baseline。
- commit/tag if any: 无。

## 2026-04-30 00:29 Phase 2.36a
- goal: 执行 Phase 2.36a trace polish + section-targeted retrieval diagnostics 最小实现。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `tests/test_phase236_tender_deep_field_trace.py`
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py`：通过。
  - `uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py -q`：`17 passed`。
  - `uv run pytest tests/test_retrieval_contract.py -q`：`13 passed`。
  - `git diff --check`：通过。
- validation: retrieval-layer trace 现在稳定输出 deep-field profile、section hints、query aliases、Missing Evidence reason 与 diagnostics；fixture 覆盖 concrete price / placeholder price / concrete qualification / generic certificate list。
- risks: 未做真实 API / CLI smoke；若终端 trace 仍显示 null / single_pass，需授权检查 Hermes 主仓库 adapter/context 展示层。真实主标书缺字段仍必须 Missing Evidence。
- next: Codex B review Phase 2.36a；通过后再决定 Git baseline 或 Codex C 抽样复验。
- commit/tag if any: 无。

## 2026-04-30 01:37 Phase 2.36b
- goal: 修复 Hermes 主仓库 deep-field trace display 映射与一步 alias binding prompt handling。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/adapters/hermes_memory_adapter.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `/Users/Weishengsu/.hermes/hermes-agent/.venv/bin/python -m py_compile agent/memory_kernel/adapters/hermes_memory_adapter.py agent/memory_kernel/kernel.py agent/memory_kernel/context_builder.py agent/memory_kernel/session_document_scope.py`：通过。
  - `/Users/Weishengsu/.hermes/hermes-agent/.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py -q`：`59 passed`。
  - `git diff --check`：Hermes 主仓库与 Hermes_memory 均通过。
- validation: 主仓库 adapter/kernel 已提升 Hermes_memory deep-field trace 字段，context block 已独立渲染 deep-field diagnostics；alias parser 已支持中文弯引号标题与 `绑定为 / 绑定成 @alias`。
- risks: 未做真实 API / CLI smoke；terminal-visible trace 与一步 alias binding 仍需 Codex C 复验。deep-field recall 本身仍 partial，限价金额、具体资质等级、业绩、人员要求不足仍应 Missing Evidence。
- next: Codex B review Phase 2.36b；通过后由 Codex C 复验 Step 1 / Q1 / Q2 终端 trace。
- commit/tag if any: 无。

## 2026-04-30 12:15 Phase 2.36c
- goal: 修复 deep-field diagnostics 与 Missing Evidence / 项目经理等级 answer boundary 语义一致性。
- changed_files:
  - `app/services/retrieval/tender_metadata.py`
  - `app/services/retrieval/service.py`
  - `tests/test_phase236_tender_deep_field_trace.py`
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `UV_CACHE_DIR=.uv-cache uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py`：通过。
  - `UV_CACHE_DIR=.uv-cache uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py tests/test_retrieval_contract.py -q`：`33 passed`。
  - `.venv/bin/python -m pytest ...` fallback：`33 passed`。
- validation: 限价 concrete evidence 现在需最终 retrieval evidence 含具体金额；metadata anchor 无最终金额时输出 Missing Evidence diagnostics。项目经理等级仅明确岗位等级要求才算 explicit，电子证书格式 / 材料条款不会被推断为岗位等级。
- risks: 未做真实 API / CLI smoke；deep-field recall 仍 partial；Phase 2.36c 仍需 Codex B review 与 Codex C 复验。
- next: Codex B review Phase 2.36c；通过后交 Codex C 复验 Step 1 / Q1 / Q2。
- commit/tag if any: 无。

## 2026-04-30 12:48 Phase 2.36c Codex B Review
- goal: 审核 Phase 2.36c diagnostics / answer boundary 语义一致性修复，并决定是否可交 Codex C。
- changed_files:
  - `app/services/retrieval/tender_metadata.py`
  - `app/services/retrieval/service.py`
  - `tests/test_phase236_tender_deep_field_trace.py`
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `UV_CACHE_DIR=.uv-cache uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py`：通过。
  - `UV_CACHE_DIR=.uv-cache uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py tests/test_retrieval_contract.py -q`：`33 passed`。
  - `git diff --check`：通过。
- validation: Codex B review 通过。实现限定在 Hermes_memory retrieval diagnostics 语义校正：最终 retrieval evidence 会重新判定 concrete evidence；metadata anchor 无最终具体金额时输出 Missing Evidence；电子证书格式 / 材料条款不会被推断为项目经理等级。
- risks: 仍未做真实 API / CLI smoke；deep-field recall 仍 partial，限价金额、具体资质等级、业绩、人员数量仍不得编造。当前不建议 baseline。
- next: 交 Codex C 重跑 Step 1 / Q1 / Q2，重点检查终端可见 diagnostics 与答案边界是否一致。
- commit/tag if any: 无。

## 2026-04-30 13:05 Phase 2.36c Codex C Validation / Baseline Prompt
- goal: 吸收 Codex C 真实终端复验结果，并写入 Phase 2.36c baseline 任务入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B 交接，不运行 pytest。
- validation: Codex C session `20260430_123308_6660a8` 通过。Step 1 alias binding 为 `alias_bound`，`alias_missing=false`，`retrieval_suppressed=false`。Q1 已无 `concrete_evidence_present=true` 与限价 Missing Evidence 冲突；Q2 `project_manager_level_explicit=false`，未把电子证书格式 / 材料条款推断为项目经理等级。安全边界 `snapshot_as_answer=false`、`facts_as_answer=false`、`transcript_as_fact=false` 稳定，未混入第三文件。
- risks: deep-field recall 仍 partial；真实限价金额、资质具体等级 / 类别、业绩、人员数量仍为后续尾项，必须继续 Missing Evidence / 人工复核。Q1 组合查询 profile 可显示 `schedule_scope`，但 price aliases / Missing Evidence diagnostics 已正确透出，非 baseline 阻塞。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，仅做 Phase 2.36c Git baseline；baseline 后停止，不进入下一阶段。
- commit/tag if any: pending。

## 2026-04-30 14:22 Phase 2.37 Route Planning Prompt
- goal: 在 Phase 2.36c baseline 后写入下一阶段路线规划入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff，不运行 pytest；未运行真实 API / CLI smoke。
- validation: Phase 2.36c baseline 已确认：HEAD `d491a44`，tag `phase-2.36c-tender-deep-field-diagnostics-baseline`。下一阶段建议先做 MVP Pilot issue intake / triage planning，把真实试用反馈转为结构化 issue records，不直接修复或 rollout。
- risks: 不得将 Phase 2.37 规划误执行为 repair、自动审标、DB 写入或生产 rollout。deep-field recall partial 应作为 issue 记录和分流，而不是被隐藏。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.37 docs-only 路线规划。
- commit/tag if any: 无。

## 2026-04-30 12:46 Phase 2.36c Baseline
- goal: 执行 Phase 2.36c deep-field diagnostics semantic consistency Git baseline。
- changed_files:
  - `app/services/retrieval/tender_metadata.py`
  - `app/services/retrieval/service.py`
  - `tests/test_phase236_tender_deep_field_trace.py`
  - `docs/PHASE236_TENDER_DEEP_FIELD_RECALL_TAIL_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
- tests:
  - `UV_CACHE_DIR=.uv-cache uv run python -m py_compile app/services/retrieval/tender_metadata.py app/services/retrieval/service.py`：通过。
  - `UV_CACHE_DIR=.uv-cache uv run pytest tests/test_tender_metadata_retrieval.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_phase236_tender_deep_field_trace.py tests/test_retrieval_contract.py -q`：`33 passed`。
  - `git diff --check`：通过。
- validation: Codex B review 已通过；Codex C session `20260430_123308_6660a8` 已通过 Step 1 / Q1 / Q2 复验，diagnostics 与 Missing Evidence 语义一致。
- risks: deep-field recall 仍 partial；真实限价金额、具体资质等级 / 类别、业绩、人员数量仍为后续尾项。baseline 不代表自动审标或 rollout。
- next: 完成测试、白名单 staged、commit/tag/push 后停止。
- commit/tag if any: pending。

## 2026-04-30 15:02 Phase 2.37 Planning
- goal: 规划 MVP Pilot issue intake / triage，承接 Day-1 / Codex C / 用户真实试用反馈。
- changed_files:
  - `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - 本轮 docs-only planning，未运行 pytest。
  - 未运行真实 API / CLI smoke。
- validation: 已评审 A-E 候选方向，推荐 Phase 2.37a 先做 local issue intake schema / template / dry-run validator or summary generator；deep-field recall partial 尾项进入 issue 分流，不直接盲修。
- risks: intake 本身不修复 retrieval recall；若后续缺少样本记录纪律，P1/P2 仍可能变成口头反馈。仍禁止 DB 写入、repair、rollout、自动审标。
- next: Codex B review Phase 2.37 规划；通过后再决定是否进入 Phase 2.37a 最小实现。
- commit/tag if any: 无。

## 2026-05-01 00:00 Phase 2.37 Codex B Review
- goal: 审核 Phase 2.37 Pilot Issue Intake / Triage planning，并写入 planning baseline 任务入口。
- changed_files:
  - `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B review / handoff，未运行 pytest；`git diff --check` 通过。
- validation: Codex B review 通过。规划优先 issue intake / triage，schema、issue_type、P0/P1/P2/P3 与 Go / Pause 规则清晰；未要求自动修复、DB 写入、索引变更、自动审标或 rollout。
- risks: issue intake 本身不修复 retrieval recall；后续 Phase 2.37a 应只做 local schema / template / dry-run validator or summary generator。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.37 planning Git baseline；baseline 后停止。
- commit/tag if any: pending。

## 2026-05-01 00:10 Phase 2.37 Drift Check Follow-up
- goal: 吸收 Codex D drift audit 中对夜间队列与 TODO 当前状态的有效提醒，做最小文档同步。
- changed_files:
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/HANDOFF_LOG.md`
- tests: docs-only drift follow-up，未运行 pytest；`git diff --check` 待 baseline 前复核。
- validation: `NEXT_CODEX_A_PROMPT.md` 当前已包含 Phase 2.37 规划文件；Codex D 该条 WARN 属旧状态。`NIGHTLY_SPRINT_QUEUE.md` 确实停留在 Phase 2.35c，已改为 Phase 2.37 planning baseline，并归档 2.36c / 2.35c 旧队列。
- risks: 不处理更大范围历史 TODO / PRD 漂移，避免打断主线；仅修正会影响自动推进安全的当前队列入口。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.37 planning docs baseline。
- commit/tag if any: pending。

## 2026-05-01 09:30 Phase 2.37a Prompt Handoff
- goal: 核实 Phase 2.37 planning baseline，并写入 Phase 2.37a local issue intake dry-run 最小实现入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff，未运行 pytest；已核实 HEAD `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`，baseline 状态 clean。
- validation: Phase 2.37 planning baseline 已完成。下一步推荐 Phase 2.37a 仅做 local issue schema / template / dry-run validator + summary generator，不写 DB、不自动创建 Linear/GitHub issue、不 repair、不 rollout。
- risks: issue intake 只做分流和留痕，不修复 retrieval recall；若 Codex A 越界写 DB / repair / rollout 必须停止。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.37a 最小实现后停止等待 Codex B review。
- commit/tag if any: 无。

## 2026-05-01 23:36 Phase 2.37a Pilot Issue Intake Dry-run
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，实现本地 issue intake schema / template / dry-run validator + summary generator。
- changed_files:
  - `scripts/phase237a_pilot_issue_intake.py`
  - `tests/test_phase237a_pilot_issue_intake.py`
  - `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase237a_pilot_issue_intake.py` passed.
  - `uv run pytest tests/test_phase237a_pilot_issue_intake.py -q` passed: `9 passed`.
- validation: 临时目录 dry-run smoke 通过：template 输出、单文件 input、目录 input、strict invalid exit 均正常；未运行真实 API / CLI smoke。
- risks: issue intake 不修复 retrieval recall；后续外部 issue 创建、DB 写入、repair 或 rollout 都必须单独规划。
- next: Codex B review；通过后执行 Phase 2.37a Git baseline。
- commit/tag if any: 无。

## 2026-05-01 23:50 Phase 2.37a Codex B Review
- goal: 审核 Phase 2.37a local issue intake dry-run 实现，并决定是否可 baseline。
- changed_files:
  - `scripts/phase237a_pilot_issue_intake.py`
  - `tests/test_phase237a_pilot_issue_intake.py`
  - `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check`：通过。
  - `uv run python -m py_compile scripts/phase237a_pilot_issue_intake.py`：通过。
  - `uv run pytest tests/test_phase237a_pilot_issue_intake.py -q`：`9 passed`。
- validation: Codex B review 通过。实现限定为本地 JSON issue schema / template / validator / summary dry-run；输出保留 `dry_run=true`、`destructive_actions=[]`、`writes_db=false`、`creates_external_issue=false`、`repairs_issue=false`。未发现 DB、OpenSearch、Qdrant、facts、document_versions、repair、rollout 或外部 issue 创建越界。
- risks: intake 只做分流与留痕，不修复 retrieval recall；后续外部 issue creation、repair 或 rollout 必须单独规划。
- next: 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.37a Git baseline；baseline 后停止，不进入 Phase 2.38。
- commit/tag if any: pending。

## 2026-05-02 21:55 Phase 2.37b Pilot Issue Intake Runbook
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，建立 MVP Pilot issue intake runbook 与本地 issue records ignored 存储约定。
- changed_files:
  - `docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md`
  - `reports/pilot_issues/.gitignore`
  - `reports/pilot_issues/README.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check` passed.
  - `uv run python scripts/phase237a_pilot_issue_intake.py --print-template >/tmp/phase237b_issue_template.json` passed.
  - `uv run python scripts/phase237a_pilot_issue_intake.py --input /tmp/phase237b_issue_template.json --strict` passed.
  - `git check-ignore -v reports/pilot_issues/example.json` passed.
- validation: Runbook covers purpose, non-goals, local storage, sanitized JSON example, validation commands, P0/P1/P2/P3 rules, Go / Pause meaning, PRD evidence boundary, and BIM as a later planning line.
- risks: Runbook does not fix retrieval recall or assign owners; real Pilot issue records may be sensitive and must remain ignored. External issue creation, repair, DB writes, rollout, and BIM asset catalog remain out of scope.
- next: Codex B review; if approved, execute Phase 2.37b docs baseline.
- commit/tag if any: 无。

## 2026-05-02 22:12 Phase 2.37c Pilot Issue Triage Summary Planning
- goal: 执行 `docs/NEXT_CODEX_A_PROMPT.md`，规划首批 Pilot issue 分诊 / daily triage summary。
- changed_files:
  - `docs/PHASE237C_PILOT_ISSUE_TRIAGE_SUMMARY_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check` passed.
  - No pytest run; no script or test files changed.
- validation: Planning document defines daily / per-round triage summary target, local ignored summary outputs, P0/P1/P2/P3 routing, known first-batch issue candidates, Go / Pause meaning, PRD evidence boundary, and BIM later-line boundary.
- risks: Planning does not create real issue records, generate summaries, assign owners, or fix P1/P2 items. External issue creation, repair, DB writes, rollout, and BIM asset catalog remain out of scope.
- next: Codex B review; if approved, execute Phase 2.37c docs baseline.
- commit/tag if any: 无。

## 2026-05-02 22:05 Phase 2.37b Codex B Review
- goal: 审核 MVP Pilot issue intake runbook 与 `reports/pilot_issues` ignored 存储约定。
- changed_files:
  - `docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md`
  - `reports/pilot_issues/.gitignore`
  - `reports/pilot_issues/README.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check`：通过。
  - `uv run python scripts/phase237a_pilot_issue_intake.py --print-template >/tmp/phase237b_issue_template.json`：通过。
  - `uv run python scripts/phase237a_pilot_issue_intake.py --input /tmp/phase237b_issue_template.json --strict`：通过。
  - `git check-ignore -v reports/pilot_issues/example.json`：通过。
- validation: Codex B review 通过。Runbook 覆盖 purpose、non-goals、storage convention、脱敏 JSON 样例、校验命令、P0/P1/P2/P3、Go/Pause、PRD evidence 边界与 BIM 后置关系；`reports/pilot_issues/*.json` / `*.md` 默认 ignored。
- risks: runbook 只规范 issue 记录方式，不自动修复、分配 owner、创建外部 issue、写 DB 或 rollout；真实 issue 记录可能包含敏感试用反馈，必须继续 ignored。
- next: 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.37b docs baseline；baseline 后停止，不进入下一阶段。
- commit/tag if any: pending。

## 2026-05-03 Phase 2.37c Codex B Review
- goal: 审核 Phase 2.37c Pilot issue triage summary planning，并决定是否可执行 docs baseline。
- changed_files:
  - `docs/PHASE237C_PILOT_ISSUE_TRIAGE_SUMMARY_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check`：通过。
- validation: Codex B review 通过。规划限定为本地 Pilot issue records 的 daily / per-round triage summary 规则，不创建真实 issue records，不生成真实 summary，不修复 P1/P2，不写 DB / facts / document_versions / OpenSearch / Qdrant，不创建外部 issue，不进入 repair 或 rollout；BIM 数据管家仍保持后置规划线。
- risks: Phase 2.37c baseline 仅固化规划；后续 Phase 2.37d 若实现 generator，必须保持输出 ignored、本地、只读，不得自动创建外部 issue 或执行 repair。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.37c docs baseline；baseline 后停止，不进入 Phase 2.37d。
- commit/tag if any: pending。

## 2026-05-03 Phase 2.37d Codex B Prompt Handoff
- goal: 检查 Phase 2.37c baseline 状态，并写入 Phase 2.37d local triage summary generator 的下一轮 Codex A 提示词。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff，未运行 pytest；已确认 HEAD `4aa6bd4`，tag `phase-2.37c-pilot-issue-triage-summary-plan-baseline`，baseline 状态 clean。
- validation: Phase 2.37c baseline 已完成。下一步推荐 Phase 2.37d 只做 local triage summary generator，读取本地 ignored Pilot issue records 并生成 ignored summary JSON / Markdown；不创建真实 issue records，不创建外部 issue，不写 DB，不 repair，不 rollout。
- risks: summary generator 只能服务人工审阅，不能被解释为 repair result、rollout approval 或自动审标结论；真实 summary 产物必须继续 ignored。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.37d 最小实现后停止等待 Codex B review。
- commit/tag if any: 无。
## 2026-05-03 12:38 Phase 2.37d
- goal: Implement local Pilot issue triage summary generator from `docs/NEXT_CODEX_A_PROMPT.md`.
- changed_files: `scripts/phase237d_pilot_triage_summary.py`, `tests/test_phase237d_pilot_triage_summary.py`, `reports/pilot_triage/.gitignore`, `reports/pilot_triage/README.md`, `docs/PHASE237C_PILOT_ISSUE_TRIAGE_SUMMARY_PLAN.md`, `docs/ACTIVE_PHASE.md`, `docs/HANDOFF_LOG.md`, `docs/PHASE_BACKLOG.md`, `docs/TODO.md`, `docs/DEV_LOG.md`, `docs/NEXT_CODEX_A_PROMPT.md`, `reports/agent_runs/latest.json` (ignored).
- tests: `uv run python -m py_compile scripts/phase237d_pilot_triage_summary.py`; `uv run pytest tests/test_phase237d_pilot_triage_summary.py -q` => 9 passed; `git diff --check`.
- validation: No real Pilot issue records or real triage summary artifacts were created; `reports/pilot_triage/*.json/*.md` are ignored.
- risks: Summary is triage only, not repair, rollout approval, or external issue creation; P1 items still require human review before bounded fix planning.
- next: Codex B review, then Phase 2.37d Git baseline only if approved.
- commit/tag if any: none.


## 2026-05-03 Phase 2.37d Codex B Review
- goal: 审核 Phase 2.37d local Pilot issue triage summary generator，并决定是否可执行 Git baseline。
- changed_files:
  - `scripts/phase237d_pilot_triage_summary.py`
  - `tests/test_phase237d_pilot_triage_summary.py`
  - `reports/pilot_triage/.gitignore`
  - `reports/pilot_triage/README.md`
  - `docs/PHASE237C_PILOT_ISSUE_TRIAGE_SUMMARY_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase237d_pilot_triage_summary.py`：通过。
  - `uv run pytest tests/test_phase237d_pilot_triage_summary.py -q`：`9 passed`。
  - `git diff --check`：通过。
  - `git check-ignore -v reports/pilot_triage/example.json reports/pilot_triage/example.md`：命中 ignore。
- validation: Codex B review 通过。实现限定为读取本地 `reports/pilot_issues/*.json` 并生成本地 ignored triage summary；summary 保留 `dry_run=true`、`destructive_actions=[]`、`writes_db=false`、`creates_external_issue=false`、`repairs_issue=false`、`rollout_approved=false`。未发现业务代码、DB、facts、document_versions、OpenSearch、Qdrant、repair、rollout、外部 issue 创建或真实运行产物越界。
- risks: summary 只能作为人工 triage 辅助，不能视为 repair result、rollout approval 或自动审标结论；P1 retrieval recall 仍需后续 bounded fix planning。
- next: 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.37d Git baseline；baseline 后停止，不进入 P1 fix 或 Phase 2.38。
- commit/tag if any: pending。

## 2026-05-03 Phase 2.38a Codex B Prompt Handoff
- goal: 检查 Phase 2.37d baseline 状态，并写入 Phase 2.38a tender P1 source availability audit 的下一轮 Codex A 提示词。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff，未运行 pytest；已确认 HEAD `d97a67c`，tag `phase-2.37d-pilot-triage-summary-baseline`，baseline 状态 clean。
- validation: Phase 2.37d baseline 已完成。下一步推荐 Phase 2.38a 只做主标书 P1 deep-field source availability read-only audit，先判断限价、具体资质等级 / 类别、项目经理等级、业绩、人员要求是源文档缺失、索引/解析缺失，还是 retrieval 召回缺口；不修 retrieval，不写 DB，不改索引，不 rollout。
- risks: audit 只能作为 bounded fix planning 前置诊断，不能被解释为审标结论、repair result 或 rollout approval；真实 audit report 必须 ignored。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.38a 最小实现后停止等待 Codex B review。
- commit/tag if any: 无。
## 2026-05-03 21:04 Phase 2.38a
- goal: Implement read-only source availability audit for main tender P1 fields from `docs/NEXT_CODEX_A_PROMPT.md`.
- changed_files: `scripts/phase238a_tender_p1_source_audit.py`, `tests/test_phase238a_tender_p1_source_audit.py`, `reports/tender_p1_audit/.gitignore`, `reports/tender_p1_audit/README.md`, `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`, `docs/ACTIVE_PHASE.md`, `docs/HANDOFF_LOG.md`, `docs/PHASE_BACKLOG.md`, `docs/TODO.md`, `docs/DEV_LOG.md`, `docs/NEXT_CODEX_A_PROMPT.md`, `reports/agent_runs/latest.json` (ignored).
- tests: `uv run python -m py_compile scripts/phase238a_tender_p1_source_audit.py`; `uv run pytest tests/test_phase238a_tender_p1_source_audit.py -q` => 10 passed; `git diff --check`.
- validation: Target document/version live dry-run attempted; local `.env` host `postgres` was not resolvable, so all fields returned `skipped_live_unavailable`; no report file was written.
- risks: Source availability for the real main tender remains unverified until local DB is reachable; no retrieval fix should start from this run alone.
- next: Codex B review, then Phase 2.38a Git baseline or rerun live read-only audit with reachable DB.
- commit/tag if any: none.


## 2026-05-03 Phase 2.38a Codex B Review
- goal: 审核 Phase 2.38a tender P1 source availability audit，并决定是否可执行 Git baseline。
- changed_files:
  - `scripts/phase238a_tender_p1_source_audit.py`
  - `tests/test_phase238a_tender_p1_source_audit.py`
  - `reports/tender_p1_audit/.gitignore`
  - `reports/tender_p1_audit/README.md`
  - `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase238a_tender_p1_source_audit.py`：通过。
  - `uv run pytest tests/test_phase238a_tender_p1_source_audit.py -q`：`10 passed`。
  - `git diff --check`：通过。
  - `git check-ignore -v reports/tender_p1_audit/example.json reports/tender_p1_audit/example.md`：命中 ignore。
- validation: Codex B review 通过。实现限定为 read-only source availability audit；输出保留 `dry_run=true`、`read_only=true`、`destructive_actions=[]`、`writes_db=false`、`mutates_index=false`、`repairs_issue=false`、`rollout_approved=false`。live dry-run 因本机 `.env` 的 `postgres` 主机名不可解析返回 `skipped_live_unavailable`，未写报告、未写 DB、未改 OpenSearch / Qdrant / facts / document_versions。
- risks: 当前仍未完成真实主标书字段 source availability 判断；不能基于 skipped 结果进入 retrieval fix。后续可在服务可用时重跑 read-only audit，或先 baseline 工具。
- next: 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.38a Git baseline；baseline 后停止，不进入 retrieval fix 或 Phase 2.38b。
- commit/tag if any: pending。

## 2026-05-03 Phase 2.38b Codex B Handoff
- goal: 检查 Phase 2.38a baseline，并写入 Phase 2.38b concrete source recall diagnostics 任务入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff；未运行 pytest。已确认 HEAD `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。
- validation: 使用 localhost 覆写执行 read-only live audit preview，未写报告、未写 DB、未修改 OpenSearch / Qdrant / facts / document_versions。结果：`price_ceiling=anchor_only`，`qualification_grade_category=concrete_source_found`，`project_manager_level=ambiguous`，`performance_requirement=concrete_source_found`，`personnel_requirement=concrete_source_found`。
- risks: 限价不得盲修，项目经理等级不得推断；Phase 2.38b 只能诊断 concrete candidate chunks 的 retrieval 可见性，不能直接修改 retrieval ranking。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.38b read-only diagnostics 后停止等待 Codex B review。
- commit/tag if any: 无。

## 2026-05-03 21:32 Phase 2.38b
- goal: 实现 Tender P1 concrete source recall diagnostics，只诊断 candidate chunk 可见性，不修 retrieval ranking。
- changed_files: `scripts/phase238b_tender_concrete_recall_diagnostics.py`, `tests/test_phase238b_tender_concrete_recall_diagnostics.py`, `reports/tender_recall_diagnostics/.gitignore`, `reports/tender_recall_diagnostics/README.md`, `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`, `docs/ACTIVE_PHASE.md`, `docs/HANDOFF_LOG.md`, `docs/PHASE_BACKLOG.md`, `docs/TODO.md`, `docs/DEV_LOG.md`, `docs/NEXT_CODEX_A_PROMPT.md`, `reports/agent_runs/latest.json`。
- tests: `uv run python -m py_compile scripts/phase238b_tender_concrete_recall_diagnostics.py` passed; `uv run pytest tests/test_phase238b_tender_concrete_recall_diagnostics.py -q` => `9 passed`; `git diff --check` passed。
- validation: localhost read-only preview 未写报告；资质 `candidate_in_top_k`，业绩 `candidate_in_top_k`，人员 `candidate_present_but_low_rank`；限价继续 Missing Evidence，项目经理等级继续人工复核。
- risks: 人员要求仍需 bounded query/profile 诊断；限价 anchor-only 不能隐藏 Missing Evidence；项目经理 ambiguous 不能推断等级。
- next: Codex B review；通过后只做 Phase 2.38b Git baseline，或规划 Phase 2.38c personnel recall tail diagnostics。
- commit/tag if any: none。

## 2026-05-03 Phase 2.38b Codex B Review
- goal: 审核 Phase 2.38b tender concrete source recall diagnostics，并决定是否可执行 Git baseline。
- changed_files:
  - `scripts/phase238b_tender_concrete_recall_diagnostics.py`
  - `tests/test_phase238b_tender_concrete_recall_diagnostics.py`
  - `reports/tender_recall_diagnostics/.gitignore`
  - `reports/tender_recall_diagnostics/README.md`
  - `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
  - `uv run pytest tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`9 passed`。
  - `git diff --check`：通过。
  - `git check-ignore -v reports/tender_recall_diagnostics/example.json reports/tender_recall_diagnostics/example.md reports/agent_runs/latest.json`：命中 ignore。
- validation: Codex B review 通过。实现限定为 read-only recall diagnostics；输出保留 `dry_run=true`、`read_only=true`、`destructive_actions=[]`、`writes_db=false`、`mutates_index=false`、`repairs_issue=false`、`rollout_approved=false`。localhost preview 未写报告，未写 DB，未改 OpenSearch / Qdrant / facts / document_versions。
- risks: `personnel_requirement` candidate 低排名只说明后续可做 bounded query/profile diagnostics；不得直接进入 broad retrieval tuning。`price_ceiling` 继续 Missing Evidence，`project_manager_level` 继续人工复核。
- next: 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.38b Git baseline；baseline 后停止，不进入 Phase 2.38c。
- commit/tag if any: pending。

## 2026-05-03 Phase 2.38c Codex B Prompt Handoff
- goal: 检查 Phase 2.38b baseline 状态，并写入 Phase 2.38c personnel recall tail planning 的下一轮 Codex A 提示词。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff；未运行 pytest。已确认 HEAD `a8c93f1`，tag `phase-2.38b-tender-recall-diagnostics-baseline`，baseline 状态 clean。
- validation: Phase 2.38b baseline 已完成。下一步推荐 Phase 2.38c 只做 docs-only personnel recall tail planning，围绕 `personnel_requirement=candidate_present_but_low_rank` 分清 query wording、section hints、candidate pool 与后续 bounded implementation 选择。
- risks: 不得顺手修 retrieval ranking；限价继续 Missing Evidence / 人工补源，项目经理等级继续人工复核；不进入 broad retrieval tuning、repair、reindex、rollout 或自动审标。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.38c planning 后停止等待 Codex B review。
- commit/tag if any: 无。

## 2026-05-03 22:27 Phase 2.38c
- goal: 完成人员要求召回低排名尾项规划，不写功能代码。
- changed_files: `docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`, `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`, `docs/ACTIVE_PHASE.md`, `docs/HANDOFF_LOG.md`, `docs/PHASE_BACKLOG.md`, `docs/TODO.md`, `docs/DEV_LOG.md`, `docs/NEXT_CODEX_A_PROMPT.md`, `reports/agent_runs/latest.json`。
- tests: docs-only planning，未运行 pytest；`git diff --check` passed。
- validation: 规划确认 `personnel_requirement` candidate present but low-rank，不是 source missing；推荐后续仅做 personnel-only aliases / section hints / candidate-pool diagnostics。
- risks: 不得扩大为 broad retrieval tuning；不得顺手处理限价或项目经理等级；后续若改 retrieval 输出需 Codex C 定向复验。
- next: Codex B review；通过后只做 Phase 2.38c docs baseline，或写入 Phase 2.38d personnel-only bounded implementation prompt。
- commit/tag if any: none。

## 2026-05-03 Phase 2.38c Codex B Review
- goal: 审核 Phase 2.38c personnel recall tail planning，并决定是否可执行 docs baseline。
- changed_files:
  - `docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`
  - `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check`：通过。
  - `reports/agent_runs/latest.json`：JSON 合法，且为 ignored 本地状态。
- validation: Codex B review 通过。规划限定为 docs-only；未写代码，未改 retrieval ranking / contract，未写 DB / facts / document_versions，未修改 OpenSearch / Qdrant，未执行 repair / backfill / reindex / cleanup / delete，未进入 rollout。
- risks: Phase 2.38d 若执行必须保持 personnel-only；不得顺手处理限价、项目经理等级、broad retrieval tuning、repair、reindex 或 rollout。
- next: 执行 `docs/NEXT_CODEX_A_PROMPT.md` 中 Phase 2.38c docs baseline；baseline 后停止，不进入 Phase 2.38d。
- commit/tag if any: pending。

## 2026-05-03 Phase 2.38c
- goal: 执行 Phase 2.38c docs-only Git baseline。
- changed_files:
  - `docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`
  - `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests: docs-only baseline，未运行 pytest；`git diff --check` 通过。
- validation: 仅处理 Phase 2.38c 规划与交接文档；未写代码、未改 retrieval ranking / contract、未写 DB / facts / document_versions、未修改 OpenSearch / Qdrant、未执行 repair / backfill / reindex / cleanup / delete、未进入 rollout。
- risks: Phase 2.38d 必须保持 personnel-only；`price_ceiling` 继续 Missing Evidence / 人工补源；`project_manager_level` 继续 human-review-only；任何后续 retrieval 输出变化都需 Codex C 定向复验。
- next: Codex B 检查 Phase 2.38c baseline，并决定是否写入 Phase 2.38d prompt。
- commit/tag if any: 由本轮 Git baseline 结果记录。

## 2026-05-04 02:50 Phase 2.38d
- goal: 执行 Phase 2.38d personnel-only bounded recall implementation。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `scripts/phase238b_tender_concrete_recall_diagnostics.py`
  - `tests/test_phase238d_personnel_recall_tail.py`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
  - `uv run pytest tests/test_phase238d_personnel_recall_tail.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_tender_metadata_retrieval.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`28 passed`。
  - `uv run pytest tests/test_phase238d_personnel_recall_tail.py -q`：`6 passed`。
  - `git diff --check`：通过。
- validation: `personnel_requirement` 现在有 `personnel_scope`、人员 aliases / section hints / boosted phrases 与 diagnostics expanded query；broad qualification query 未被 personnel scope 劫持；`price_ceiling` 与 `project_manager_level` 后置边界保持。
- risks: 未跑 DB-backed live preview，因为当前 diagnostics path 可能写 retrieval log；真实 answer / candidate rank 改善仍需 Codex C 定向复验。
- next: Codex B review；通过后决定 Codex C 复验或 Phase 2.38d Git baseline。
- commit/tag if any: 无。

## 2026-05-04 Phase 2.38d Codex B Prompt Handoff
- goal: 检查 Phase 2.38c baseline，并写入 Phase 2.38d personnel-only bounded recall implementation 的 Codex A 执行入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff；未运行 pytest。已确认 HEAD `ff49941`，tag `phase-2.38c-personnel-recall-tail-plan-baseline`，`main...origin/main` 对齐。
- validation: Phase 2.38c baseline 已完成，worktree 检查前干净；下一步仅授权 `personnel_requirement` 低排名 bounded implementation。
- risks: 不得扩大为 broad retrieval tuning；不得处理限价或项目经理等级；不得写 DB / facts / document_versions / OpenSearch / Qdrant；不得 repair / backfill / reindex / rollout。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；完成 Phase 2.38d implementation 后停止等待 Codex B review。若 retrieval 输出变化，后续建议 Codex C 定向复验。
- commit/tag if any: 无。

## 2026-05-04 Phase 2.38d Codex B Review
- goal: 审核 Phase 2.38d personnel-only bounded recall implementation 首轮实现，并决定是否可进入 Codex C 复验或 baseline。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: `git diff --check` 通过；Codex B 未运行 pytest。
- validation: 首轮实现方向基本正确，`personnel_scope`、personnel aliases / section hints / diagnostics 已出现；但 review 发现 `人员要求是什么？` 与 `项目人员数量、专业、职称或资质要求是什么？` 仍混入 broad qualification aliases / sections，例如 `项目经理`、`联合体投标`、`类似工程业绩`、`资信标`。
- risks: 该问题会把 personnel-only fix 扩大成 broad qualification retrieval；不能 baseline。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只修 personnel-focused query 混入 broad aliases / sections 的问题；修复后停止等待 Codex B review。
- commit/tag if any: 无。

## 2026-05-04 03:11 Phase 2.38d
- goal: 修复 personnel-focused query 混入 broad qualification aliases / sections 的 Codex B review finding。
- changed_files:
  - `app/services/retrieval/service.py`
  - `tests/test_phase238d_personnel_recall_tail.py`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
  - `uv run pytest tests/test_phase238d_personnel_recall_tail.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_tender_metadata_retrieval.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`28 passed`。
  - `git diff --check`：通过。
- validation: `人员要求是什么？` 与 `项目人员数量、专业、职称或资质要求是什么？` 均为 `personnel_scope`，且不再包含 `项目经理`、`项目负责人`、`注册建造师`、`安全考核证`、`联合体投标`、`类似工程业绩`、`资信标` 等 broad 信号；broad qualification query 仍保持 `qualification_scope`。
- risks: 未做 DB-backed live smoke，真实 answer / rank 改善仍待 Codex C 定向复验；限价与项目经理等级继续按既定后置边界处理。
- next: 等待 Codex B 复审；通过后再决定 Codex C Q2 人员要求定向复验或 Phase 2.38d Git baseline。
- commit/tag if any: 无。

## 2026-05-04 Phase 2.38d Codex B Review Passed
- goal: 复审 Phase 2.38d review-fix，确认是否可进入 Codex C 定向终端复验。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check`：通过。
  - `uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
  - `uv run pytest tests/test_phase238d_personnel_recall_tail.py -q`：`6 passed`。
  - `uv run pytest tests/test_phase235_tender_deep_field_retrieval.py tests/test_tender_metadata_retrieval.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`22 passed`。
- validation: `人员要求是什么？` 与 `项目人员数量、专业、职称或资质要求是什么？` 均为 `personnel_scope`，不再混入 `项目经理`、`项目负责人`、`注册建造师`、`安全考核证`、`联合体投标`、`类似工程业绩`、`资信标`；broad query `投标资质、项目经理、联合体、业绩、人员要求分别是什么？` 仍为 `qualification_scope`。
- risks: 未做 DB-backed live smoke，真实 answer / rank 改善仍待 Codex C 定向复验；限价与项目经理等级继续按既定后置边界处理。
- next: Codex C 执行 Q2 人员要求定向真实终端复验；通过后 Codex B 再写 Phase 2.38d Git baseline prompt。
- commit/tag if any: 无。

## 2026-05-04 Phase 2.38d Codex C Follow-up Handoff
- goal: 吸收 Codex C 定向终端复验结果，并写入 Q1 intent parsing 的最小修复入口。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 本轮为 Codex B handoff；未运行 pytest。本地复现显示 Q1 带否定/排除句时仍落到 `qualification_scope`，且 metadata fields 包含 qualification / project manager / consortium / performance。
- validation: Codex C 报告可信。Q2 人员要求通过，Q3 broad query 通过；剩余阻塞是 Q1 中 `不要回答投标资质、项目经理、联合体、业绩` 被误判为 broad qualification intent。
- risks: 不得扩大成 broad retrieval tuning；不得处理限价或项目经理等级；不得写 DB / facts / document_versions / OpenSearch / Qdrant。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只修 Q1 否定/排除句 intent parsing；修复后停止等待 Codex B review。
- commit/tag if any: 无。

## 2026-05-04 03:49 Phase 2.38d
- goal: 修复 Q1 中否定/排除说明误触发 broad qualification intent 的问题。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `tests/test_phase238d_personnel_recall_tail.py`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
  - `uv run pytest tests/test_phase238d_personnel_recall_tail.py tests/test_phase235_tender_deep_field_retrieval.py tests/test_tender_metadata_retrieval.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`30 passed`。
- validation: Q1 `项目人员数量、专业、职称或资质要求是什么？请只回答人员要求，不要回答投标资质、项目经理、联合体、业绩。` 现在为 `personnel_scope`，metadata fields 仅 `personnel_requirement`；Q2 personnel-only 仍通过；Q3 broad query 仍为 `qualification_scope`。
- risks: 未做 DB-backed live smoke，真实 Hermes CLI 输出仍需 Codex C 定向复验；限价与项目经理等级继续后置。
- next: 等待 Codex B review；通过后建议 Codex C 重新复验 Q1/Q2/Q3。
- commit/tag if any: 无。

## 2026-05-04 Phase 2.38d Codex C Answer Boundary Follow-up
- goal: 吸收 Codex C 真实终端复验结果，修复 personnel-only 最终回答边界。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py -q`：`11 passed`。
- validation: `personnel_scope` context block 现在明确人员-only 回答不得混入项目经理 / 项目负责人 / 注册建造师 / B证，且不得从角色列表推断“每类1人”；数量、专业、职称或资质未明确时应输出 Missing Evidence。
- risks: 未跑真实 Hermes CLI；模型是否完全遵守回答边界仍需 Codex C 复验。未写 DB / facts / versions / OpenSearch / Qdrant。
- next: Codex B review；通过后 Codex C 重跑 Q1/Q2/Q3。
- commit/tag if any: 无。

## 2026-05-04 Phase 2.38d Q1 Intent Fix Codex B Review Passed
- goal: 复审 Q1 否定/排除句 intent fix，确认是否可进入 Codex C 定向终端复验。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `git diff --check`：通过。
  - `uv run python -m py_compile app/services/retrieval/service.py app/services/retrieval/tender_metadata.py scripts/phase238b_tender_concrete_recall_diagnostics.py`：通过。
  - `uv run pytest tests/test_phase238d_personnel_recall_tail.py -q`：`8 passed`。
  - `uv run pytest tests/test_phase235_tender_deep_field_retrieval.py tests/test_tender_metadata_retrieval.py tests/test_phase238b_tender_concrete_recall_diagnostics.py -q`：`22 passed`。
- validation: Q1 带“不要回答投标资质、项目经理、联合体、业绩”的人员 query 现在为 `personnel_scope`，metadata fields 仅 `personnel_requirement`；Q2 personnel-only 仍为 `personnel_scope`；Q3 broad query 仍为 `qualification_scope`。
- risks: 未做 DB-backed live smoke，真实 Hermes CLI 输出仍需 Codex C 定向复验；限价与项目经理等级继续后置。
- next: Codex C 重跑 Q1/Q2/Q3 定向真实终端复验；通过后 Codex B 再写 Phase 2.38d Git baseline prompt。
- commit/tag if any: 无。

## 2026-05-04 18:32 Phase 2.38d
- goal: 补齐 Codex C 复验后的 answer-boundary 状态交接，确保下一轮不误判为可 baseline。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py -q`：`11 passed`。
- validation: 本轮未跑真实 Hermes CLI；answer-boundary 只在 context 层新增约束，需 Codex B review 后交 Codex C 重跑 Q1/Q2/Q3。
- risks: 真实模型是否完全遵守人员-only 边界仍未复验；限价金额与项目经理等级继续后置；不得直接 baseline。
- next: Codex B review；通过后 Codex C 定向终端复验。
- commit/tag if any: 无。

## 2026-05-04 19:15 Phase 2.38d
- goal: 第二轮最小修复 personnel-only final answer guard，吸收 Codex C 复验中 Q1/Q2/Q3 仍有过度表述的问题。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py -q`：`12 passed`。
- validation: 未跑真实 Hermes CLI；本轮仅加强 context guard 并补 broad qualification 不误套 personnel boundary 的单测。
- risks: 模型是否遵守 strict guard 仍需 Codex C 终端复验；不得直接 baseline；不得修 retrieval / 限价 / 项目经理等级。
- next: Codex B review；通过后 Codex C 重跑 Q1/Q2/Q3。
- commit/tag if any: 无。

## 2026-05-04 20:31 Phase 2.38d
- goal: 第三轮最小修复 personnel-only structured answer guard，吸收 Codex C 最新复验中 `项目经理` 与 `每个项目限1人` 仍外溢的问题。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py -q`：`12 passed`。
- validation: `personnel_scope` context 现在输出 `personnel_forbidden_answer_terms`、`personnel_count_inference_forbidden=true`、`ignore_non_personnel_content_in_mixed_chunks=true`；broad `qualification_scope` 不输出这些 lines。
- risks: 未跑真实 Hermes CLI；模型是否遵守 structured guard 仍需 Codex C 复验。未写 DB / facts / versions / OpenSearch / Qdrant。
- next: Codex B review；通过后 Codex C 重跑 Q1/Q2/Q3。
- commit/tag if any: 无。

## 2026-05-05 01:56 Phase 2.38d
- goal: 第四轮最小修复 personnel-only safe fallback contract，在不改 retrieval / contract / 主架构的前提下继续压制人员-only 最终回答外溢。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py -q`：`12 passed`。
- validation: `personnel_scope` context 现在输出 violation flags 与 safe fallback template；broad `qualification_scope` 仍不输出 personnel-only guard。
- risks: 当前白名单未允许修改 `run_agent.py`，未实现真正 post-answer retry / replacement；仍需 Codex C 真实终端复验。未写 DB / facts / versions / OpenSearch / Qdrant。
- next: Codex B review；通过后 Codex C 重跑 Q1/Q2/Q3。
- commit/tag if any: 无。

## 2026-05-05 20:36 Phase 2.38d
- goal: 执行第五轮 runtime post-answer guard，将 personnel-only fallback 接入 Hermes 主仓真实输出路径。
- changed_files:
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests: 未执行；主仓代码未写入。
- validation: 已读取任务文件并定位修改点；已准备 `/private/tmp/phase238d_runtime_guard_patch.py`，但未能执行。
- risks: Hermes 主仓位于当前 sandbox writable roots 外；两次 `require_escalated` 执行补丁脚本均因 automatic permission approval review 超时未获批准。runtime post-answer guard 未实现，不能 baseline。
- next: 用户显式批准主仓写入后，重新执行 `NEXT_CODEX_A_PROMPT.md`，优先修改 `run_agent.py`、`kernel.py` 与目标测试。
- commit/tag if any: 无。

## 2026-05-05 20:42 Phase 2.38d
- goal: 第五轮最小修复 personnel-only runtime post-answer guard，在 Hermes 主仓真实输出路径压制 personnel-only 禁词和隐式数量推断。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/run_agent.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile run_agent.py agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py tests/agent/test_session_document_scope.py -q`：`65 passed`。
- validation: 已接入 `apply_personnel_answer_guard()`；`personnel_scope` + personnel-only query 命中禁词或数量推断时替换为 safe fallback；broad `qualification_scope` 不触发。
- risks: 未做真实 CLI 复验；需 Codex B review 与 Codex C Q1/Q2/Q3 终端复验。未写 DB / facts / versions / OpenSearch / Qdrant。
- next: Codex B review；通过后 Codex C 重跑 Q1/Q2/Q3，确认 Q1/Q2 无禁词 / 数量推断，Q3 broad query 未被误压扁。
- commit/tag if any: 无。

## 2026-05-05 21:09 Phase 2.38d
- goal: 执行 `NEXT_CODEX_A_PROMPT.md` 的 review / validation handoff 任务，复核 runtime guard 状态并准备交给 Codex B / Codex C。
- changed_files:
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`
- tests:
  - `.venv/bin/python -m py_compile run_agent.py agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py`：通过。
  - `.venv/bin/python -m pytest -o addopts='' tests/agent/test_structured_citation_context.py tests/agent/test_session_document_scope.py -q`：`65 passed`。
- validation: 本轮未新增功能；确认当前入口要求仅做 review / validation handoff。Phase 2.38d runtime guard 仍需 Codex B review 与 Codex C Q1/Q2/Q3 真实终端复验。
- risks: 未跑真实 CLI；不能 baseline；不得扩大到限价、项目经理等级、broad retrieval tuning、DB / 索引变更。
- next: Codex B review；通过后 Codex C 按 `NEXT_CODEX_A_PROMPT.md` 中三条 query 复验。
- commit/tag if any: 无。

## 2026-05-05 22:24 Phase 2.38d
- goal: Phase 2.38d personnel runtime guard Git baseline。
- changed_files:
  - `app/services/retrieval/service.py`
  - `app/services/retrieval/tender_metadata.py`
  - `scripts/phase238b_tender_concrete_recall_diagnostics.py`
  - `tests/test_phase238d_personnel_recall_tail.py`
  - `docs/PHASE238D_PERSONNEL_RECALL_IMPLEMENTATION.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/run_agent.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/context_builder.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/kernel.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_structured_citation_context.py`
  - Phase 2.38d docs / handoff hunk only
- tests:
  - Hermes 主仓 py_compile：通过。
  - Hermes 主仓 `tests/agent/test_structured_citation_context.py tests/agent/test_session_document_scope.py`：`65 passed`。
  - Hermes 主仓 `git diff --check`：通过。
  - Hermes_memory py_compile：通过。
  - Hermes_memory `tests/test_phase238d_personnel_recall_tail.py tests/test_phase238b_tender_concrete_recall_diagnostics.py`：`17 passed`。
  - Hermes_memory `git diff --check`：通过。
- validation: Codex C session `20260505_211355_d19af3` 已通过：Q1/Q2 personnel-only safe fallback 触发且无禁词 / 数量推断；Q3 broad query 未被压扁；无 facts / transcript / 第三文件污染。
- risks: 本 baseline 不处理 Data Steward / Phase 2.39，不处理限价、项目经理等级或 broad retrieval tuning。Data Steward docs dirty 必须单独 baseline。
- next: baseline 后停止；下一轮单独处理 Phase 2.39 Data Steward docs-only baseline 或由 Codex B 写新 prompt。
- commit/tag if any: tag `phase-2.38d-personnel-runtime-guard-baseline`，commit 由本轮 Git baseline 生成。

## 2026-05-05 22:44 Phase 2.39
- goal: Data Steward / BIM 数据管家后置产品线 docs-only baseline。
- changed_files:
  - `docs/PRD.md`
  - `docs/ROADMAP.md`
  - `docs/TECHNICAL_DESIGN.md`
  - `docs/PHASE239_DATA_STEWARD_PRODUCT_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Data Steward / Phase 2.39 关键词与边界 `rg` 复核：通过。
- validation: PRD / Roadmap / Technical Design / Phase 2.39 计划已明确 Data Steward 是后置产品线；当前不新增 DB schema、Neo4j、PostGIS、空间索引代码、生产级 scheduler，不解析 TB 级 BIM 原始模型，不直接进入 LLM 上下文。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是 Phase 2.38 遗留 dirty，已排除本轮 stage。Data Steward 仍不得直接进入实现。
- next: baseline 后停止；下一轮建议做 PRD Acceptance Matrix / MVP Evidence Pack docs-only planning。
- commit/tag if any: tag `phase-2.39-data-steward-product-plan-baseline`，commit 由本轮 Git baseline 生成。

## 2026-05-05 22:59 Phase 2.40
- goal: PRD Acceptance Matrix / MVP Evidence Pack docs-only planning。
- changed_files:
  - `docs/PHASE240_PRD_ACCEPTANCE_MATRIX_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.40 关键词与边界 `rg` 复核：通过。
- validation: 新规划定义 PRD acceptance matrix 字段、能力域、evidence pack 优先级和 `not_claimable` 清单；明确下一步应补证据包，不直接扩展新能力。
- risks: 本轮未形成正式 matrix records 或 evidence pack artifact；`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 与 `docs/NEXT_CODEX_A_PROMPT.md` 仍为既有 dirty，其中 Phase 2.38 文件不属于本轮范围。
- next: Codex B review；通过后可规划 Phase 2.40a 只读 matrix / evidence pack artifact。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-05 23:28 Phase 2.40a
- goal: PRD Acceptance Matrix / MVP Evidence Pack docs-only artifact。
- changed_files:
  - `docs/PRD_ACCEPTANCE_MATRIX.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.40a artifact 关键词与边界 `rg` 复核：通过。
- validation: Matrix 已覆盖 PRD item、capability area、status、evidence、known gap、next phase candidate 与 not claimable；明确当前可内部受控 MVP Pilot，但不是 production rollout。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是无关 Phase 2.38 dirty；`docs/NEXT_CODEX_A_PROMPT.md` 是既有 prompt dirty，本轮未修改。Matrix 仍需后续人工维护 evidence refs。
- next: Codex B review；通过后只做 Phase 2.40a docs-only baseline，不直接进入新能力开发。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 00:05 Phase 2.41
- goal: MVP Pilot Evidence Review / Go-No-Go docs-only planning。
- changed_files:
  - `docs/PHASE241_MVP_PILOT_EVIDENCE_REVIEW_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：待最终复核。
  - Phase 2.41 关键词与边界 `rg`：待最终复核。
- validation: 规划定义 Go / Pause / No-Go、P0/P1/P2/P3 handling、人工复核要求与 not-claimable checklist；明确 Go 只代表内部受控 MVP Pilot 可继续，不代表 production rollout。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是无关遗留 dirty；`docs/NEXT_CODEX_A_PROMPT.md` 是本轮入口文件 dirty，本轮未修改。不得把 planning 写成 rollout approval。
- next: Codex B review；通过后只做 Phase 2.41 docs-only baseline，后续再决定是否做 Phase 2.41a checklist artifact 或 dry-run report。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 01:51 Phase 2.41a
- goal: MVP Pilot Evidence Review Checklist docs-only artifact。
- changed_files:
  - `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：待最终复核。
  - Phase 2.41a checklist 关键词与边界 `rg`：待最终复核。
- validation: Checklist 已覆盖人工填写字段、P0/P1、evidence policy、citation、governance、human review、not-claimable 与 Go / Pause / No-Go 模板；明确不是 production rollout approval、自动审标批准或 repair 授权。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 与 `docs/NEXT_CODEX_A_PROMPT.md` 仍为既有 dirty；本轮不得提交 Git，不得进入新能力开发、rollout、repair、Data Steward 实现或 API/CLI smoke。
- next: Codex B review；通过后若满足 Baseline Gate，再做 Phase 2.41a docs-only baseline。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 02:21 Phase 2.42
- goal: Codex B review Phase 2.41a baseline and write next Codex A prompt for MVP Pilot review dry-run report planning。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag 检查：Phase 2.41a baseline 已完成，HEAD `a2e1042`，tag `phase-2.41a-mvp-pilot-evidence-review-checklist-baseline`。
- validation: Phase 2.41a baseline review 通过；下一步已收缩为 Phase 2.42 docs-only planning，不写代码、不新增脚本、不生成真实 report、不运行 API / CLI、不进入 rollout。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，Phase 2.42 不得 stage / commit。Phase 2.42 仍不是 Go 结论或 production approval。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，生成 `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md` 并同步状态；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 prompt handoff，不提交 Git。

## 2026-05-06 05:15 Phase 2.42
- goal: MVP Pilot Review Dry-run Report docs-only planning。
- changed_files:
  - `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.42 dry-run report 关键词与边界 `rg`：通过。
  - `git status --short`：已复核，未发现业务代码变更；`docs/NEXT_CODEX_A_PROMPT.md` 与 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 为既有 dirty。
- validation: 规划已覆盖 report 输入、输出、Go / Pause / No-Go decision logic、P0/P1/P2/P3 aggregation、evidence policy、citation summary、Missing Evidence summary 与 ignored storage policy。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 与 `docs/NEXT_CODEX_A_PROMPT.md` 仍为既有 dirty；本轮不得提交 Git，不得生成真实 report，不得进入 rollout、repair、Data Steward 实现或 API/CLI smoke。
- next: Codex B review；通过后再决定是否进入 Phase 2.42a local ignored report artifact 或 dry-run generator。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 09:59 Phase 2.42
- goal: Codex B review Phase 2.42 planning and Codex D drift report；写入 docs sync review-fix prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.42 关键词与边界 `rg`：通过。
  - `git status --short` / HEAD / tag 检查：无业务代码变更，HEAD `a2e1042`。
- validation: Phase 2.42 planning 内容通过 Codex B review；Codex D WARN 基本成立，属于 TODO 当前口径与 Nightly queue 过时，不是主线越界。
- risks: Baseline Gate 的“文档状态已同步”尚未完全满足；`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，下一轮不得触碰。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 TODO / Nightly queue / 状态文件 docs sync review-fix；完成后停止等待 Codex B review，不自动 baseline。
- commit/tag if any: 无；本轮只是 Codex B prompt handoff，不提交 Git。

## 2026-05-06 10:02 Phase 2.42
- goal: Phase 2.42 docs sync review-fix：同步 TODO 当前状态与 Nightly queue，避免旧 Phase 2.39 / Phase 2.37 口径误导 baseline 前状态。
- changed_files:
  - `docs/TODO.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.42 / Nightly queue 关键词与边界 `rg`：通过。
  - `git status --short`：已复核；无业务代码变更。
- validation: TODO 当前状态已从 Phase 2.39 正在收口改为已完成 baseline；Nightly Current Queue 已改为 Phase 2.42 docs sync review-fix Green Lane；旧 Phase 2.37 baseline 已归档为 stale archived；明确小修不 baseline。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 与 `docs/NEXT_CODEX_A_PROMPT.md` 仍为既有 dirty；`docs/DEV_LOG.md` 与 `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md` 为 Phase 2.42 planning 既有 dirty；本轮不得提交 Git、不得写代码、不得进入 rollout / repair / Data Steward 实现。
- next: Codex B review docs sync review-fix；通过后再决定是否写入 Phase 2.42 docs-only baseline prompt。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 10:12 Phase 2.42
- goal: Codex B review Phase 2.42 docs sync review-fix and write docs-only Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.42 / Nightly queue 关键词与边界 `rg`：通过。
  - `git status --short`：已复核；无业务代码变更。
- validation: Phase 2.42 planning 与 docs sync review-fix 均通过 Codex B review；Baseline Gate 已满足，允许单独执行 docs-only Git baseline。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，baseline 必须排除；baseline 后不得自动进入 Phase 2.42a、rollout、repair 或 Data Steward 实现。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只 stage Phase 2.42 白名单文件，commit / tag / push 后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 10:23 Phase 2.42a
- goal: Codex B review Phase 2.42 baseline and write Phase 2.42a MVP Pilot review dry-run generator prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag 检查：Phase 2.42 baseline 已完成，HEAD `0e0d208`，tag `phase-2.42-mvp-pilot-review-dry-run-plan-baseline`。
  - `git diff-tree --no-commit-id --name-only -r HEAD`：确认只包含 Phase 2.42 docs-only 白名单文件。
- validation: Phase 2.42 baseline 通过 Codex B review；下一步收缩为 Phase 2.42a local dry-run generator，只读取显式 JSON 输入，输出 ignored report，不默认扫描真实 reports / reviews。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得触碰；Phase 2.42a 不得生成 rollout approval、repair authorization、真实 DB 写入或 Data Steward 实现。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；完成 Phase 2.42a 后停止等待 Codex B review，不自动 baseline。
- commit/tag if any: 无；本轮只是 Phase 2.42a prompt handoff，不提交 Git。

## 2026-05-06 10:32 Phase 2.42a
- goal: MVP Pilot Review Dry-run Report Generator 最小实现。
- changed_files:
  - `scripts/phase242a_mvp_pilot_review_dry_run.py`
  - `tests/test_phase242a_mvp_pilot_review_dry_run.py`
  - `reports/mvp_pilot_reviews/.gitignore`
  - `reports/mvp_pilot_reviews/README.md`
  - `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `uv run python -m py_compile scripts/phase242a_mvp_pilot_review_dry_run.py`：通过。
  - `uv run pytest tests/test_phase242a_mvp_pilot_review_dry_run.py -q`：`7 passed`。
  - `git diff --check`：通过。
  - `git check-ignore -v reports/mvp_pilot_reviews/example.json reports/mvp_pilot_reviews/example.md`：通过。
  - `git status --short`：已复核；无业务代码变更。
- validation: generator 仅读取显式 `--input` JSON，输出 dry-run JSON；`--output-dir` 仅显式写入 JSON / Markdown；固定保留 no rollout / no repair / no destructive action / no data mutation / facts-transcript-snapshot not answer。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍为无关遗留 dirty；`docs/NEXT_CODEX_A_PROMPT.md` 与 `docs/NIGHTLY_SPRINT_QUEUE.md` 为既有 dirty，本轮未修改；本轮不提交 Git、不运行 API / CLI smoke、不生成真实 report。
- next: Codex B review Phase 2.42a；通过后再单独决定是否 Git baseline。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 10:43 Phase 2.42a
- goal: Codex B review Phase 2.42a MVP Pilot review dry-run generator and write Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `uv run python -m py_compile scripts/phase242a_mvp_pilot_review_dry_run.py`：通过。
  - `uv run pytest tests/test_phase242a_mvp_pilot_review_dry_run.py -q`：`7 passed`。
  - `git diff --check`：通过。
  - `git check-ignore -v reports/mvp_pilot_reviews/example.json reports/mvp_pilot_reviews/example.md reports/agent_runs/latest.json`：通过。
- validation: Phase 2.42a generator 只读取显式 `--input`，不默认扫描真实 reports / reviews；输出固定 dry-run / no rollout / no repair / no destructive action / no data mutation / facts-transcript-snapshot not answer；Markdown disclaimer 与 ignored report storage 均符合规划。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍为遗留无关 dirty，baseline 必须排除；baseline 不得生成真实 report、运行 API / CLI、写 DB、repair、rollout 或进入 Data Steward。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.42a Git baseline；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 10:44 Phase 2.42b
- goal: Codex B review Phase 2.42a baseline and write Phase 2.42b input template / runbook artifact prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag 检查：Phase 2.42a baseline 已完成，HEAD `4c60b28`，tag `phase-2.42a-mvp-pilot-review-dry-run-generator-baseline`。
  - `git diff-tree --no-commit-id --name-only -r HEAD`：确认只包含 Phase 2.42a 白名单文件。
  - `origin/main` 对齐检查：通过。
- validation: Phase 2.42a baseline 通过 Codex B review；下一步收缩为 Phase 2.42b sanitized input template + runbook artifact，不运行 API / CLI，不生成真实 report。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得触碰；Phase 2.42b 不得生成真实 MVP Pilot report、rollout approval、repair authorization、DB 写入或 Data Steward 实现。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；完成 Phase 2.42b 后停止等待 Codex B review，不自动 baseline。
- commit/tag if any: 无；本轮只是 Phase 2.42b prompt handoff，不提交 Git。

## 2026-05-06 10:50 Phase 2.42b
- goal: MVP Pilot Review Dry-run Input Template / Runbook artifact。
- changed_files:
  - `docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json`
  - `docs/MVP_PILOT_REVIEW_DRY_RUN_RUNBOOK.md`
  - `docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `python -m json.tool ...`：本机裸 `python` 不存在，改用 `uv run python`。
  - `uv run python -m json.tool docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json`：通过。
  - `uv run python scripts/phase242a_mvp_pilot_review_dry_run.py --input docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json --json`：通过。
  - safety assertions：通过，template 输出 decision 为 `pause`。
  - `git diff --check`：通过。
- validation: Template 只含 sanitized placeholders，runbook 覆盖人工输入整理、ignored report output、Go/Pause/No-Go 解读与非目标；未生成真实 MVP Pilot report。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty；`docs/NEXT_CODEX_A_PROMPT.md` 与 `docs/NIGHTLY_SPRINT_QUEUE.md` 为既有 prompt / queue dirty，本轮按要求未修改 NEXT。Phase 2.42b 不得被解释为 rollout、repair、Data Steward 或真实 Pilot approval。
- next: Codex B review Phase 2.42b；通过后再单独决定是否 Git baseline。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 10:56 Phase 2.42b
- goal: Codex B review Phase 2.42b template / runbook artifact and write Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `uv run python -m json.tool docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json`：通过。
  - `uv run python scripts/phase242a_mvp_pilot_review_dry_run.py --input docs/MVP_PILOT_REVIEW_DRY_RUN_INPUT_TEMPLATE.json --json`：通过。
  - safety assertions：通过，template 输出 decision 为 `pause`。
  - `git diff --check`：通过。
- validation: Template 是 sanitized JSON，无真实客户数据 / session_id / document_id / fact_id / 人名 / 金额；runbook 覆盖人工输入整理、ignored report output、Go/Pause/No-Go 解读与非目标；Phase 2.42b 未生成真实 MVP Pilot report。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍为遗留无关 dirty，baseline 必须排除；baseline 不得生成真实 report、运行 API / CLI、写 DB、repair、rollout 或进入 Data Steward。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.42b Git baseline；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 11:06 Phase 2.43
- goal: Codex B review Phase 2.42b baseline and write Phase 2.43 Internal MVP Pilot Launch Candidate Planning prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag / `origin/main` 检查：Phase 2.42b baseline 已完成，HEAD `edd0e08`，tag `phase-2.42b-mvp-pilot-review-dry-run-template-baseline`。
  - `git diff-tree --no-commit-id --name-only -r HEAD`：确认 Phase 2.42b baseline 只包含 template / runbook / Phase 2.42 docs / handoff 文件。
  - 本轮不运行 API / CLI smoke，不运行 pytest，不生成真实 MVP Pilot report。
- validation: Phase 2.42b baseline 通过 Codex B 状态复核；下一步收缩为 Phase 2.43 launch candidate planning，只做 docs-only planning，不启动真实 Pilot。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得触碰；Phase 2.43 不得生成真实 MVP Pilot report、rollout approval、repair authorization、DB 写入或 Data Steward 实现。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；完成 Phase 2.43 planning 后停止等待 Codex B review，不自动 baseline。
- commit/tag if any: 无；本轮只是 Phase 2.43 prompt handoff，不提交 Git。

## 2026-05-06 11:12 Phase 2.43
- goal: Internal MVP Pilot Launch Candidate docs-only planning。
- changed_files:
  - `docs/PHASE243_MVP_PILOT_LAUNCH_CANDIDATE_PLAN.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：待最终复核。
  - Phase 2.43 keyword boundary `rg`：待最终复核。
  - `git status --short`：待最终复核。
- validation: 规划串联 Pilot runbook、user guide、Day-1 run sheet、feedback template、evidence review checklist、dry-run report runbook / template 与 PRD acceptance matrix；明确 Go / Pause / No-Go、启动前置条件、Pilot Day flow、记录字段和后置项。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty；Phase 2.43 不得被解释为真实 Pilot 启动、production rollout、repair authorization、Data Steward implementation 或自动审标 / 自动经营决策。
- next: Codex B review Phase 2.43 planning；通过后再单独决定是否 Git baseline 或进入 Phase 2.43a。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 11:17 Phase 2.43
- goal: Codex B review Phase 2.43 launch candidate planning and write Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.43 keyword boundary `rg`：通过。
  - `git status --short`：已复核；仅 Phase 2.43 白名单文件、baseline prompt 与遗留 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty。
- validation: Phase 2.43 planning artifact 通过 Codex B review。规划覆盖 launch candidate 目标、非目标、前置条件、Go / Pause / No-Go、Pilot Day flow、记录字段与后置项；未启动真实 Pilot，未生成真实 report，未写 DB，未进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，baseline 必须排除；Phase 2.43 baseline 只固化 planning，不得自动进入 2.43a / 2.43b / 2.43c。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.43 Git baseline；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 11:24 Phase 2.43a
- goal: Codex B review Phase 2.43 baseline and write Phase 2.43a MVP Pilot Launch Packet / Operator Checklist artifact prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag / `origin/main` 检查：Phase 2.43 baseline 已完成，HEAD `5141bb5`，tag `phase-2.43-mvp-pilot-launch-candidate-plan-baseline`。
  - `git diff-tree --no-commit-id --name-only -r HEAD`：确认 Phase 2.43 baseline 只包含 launch candidate planning 与 handoff docs。
  - 本轮不运行 API / CLI smoke，不运行 pytest，不生成真实 MVP Pilot report。
- validation: Phase 2.43 baseline 通过 Codex B 状态复核；下一步收缩为 Phase 2.43a launch packet / operator checklist artifact，只做 docs-only artifact，不启动真实 Pilot。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得触碰；Phase 2.43a 不得生成真实 MVP Pilot report、rollout approval、repair authorization、DB 写入或 Data Steward 实现。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；完成 Phase 2.43a artifact 后停止等待 Codex B review，不自动 baseline。
- commit/tag if any: 无；本轮只是 Phase 2.43a prompt handoff，不提交 Git。

## 2026-05-06 11:33 Phase 2.43a
- goal: MVP Pilot Launch Packet / Operator Checklist docs-only artifact。
- changed_files:
  - `docs/MVP_PILOT_LAUNCH_PACKET.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.43a keyword boundary `rg`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
  - `git status --short`：已复核。
- validation: 新增 launch packet，覆盖角色、启动前 checklist、session execution、evidence review、Go / Pause / No-Go、输出归档、人工决策声明、停止条件与后续流转；未启动真实 Pilot、未生成真实 report、未运行 API / CLI、未写 DB、未进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得 stage / commit；`docs/NEXT_CODEX_A_PROMPT.md` 是既有 prompt handoff dirty，本轮未修改；Phase 2.43a 需 Codex B review 后才能 baseline。
- next: Codex B review Phase 2.43a launch packet；通过后单独授权 docs baseline 或规划 Phase 2.43b。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 11:43 Phase 2.43a
- goal: Codex B review Phase 2.43a launch packet artifact and write Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.43a keyword boundary `rg`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
  - `git status --short`：已复核；仅 Phase 2.43a 白名单文件、baseline prompt 与遗留 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty。
- validation: Phase 2.43a launch packet artifact 通过 Codex B review。文档覆盖角色、启动前 checklist、session execution、evidence review、Go / Pause / No-Go、输出归档、人工决策声明、停止条件与后续流转；未启动真实 Pilot，未生成真实 report，未写 DB，未进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，baseline 必须排除；Phase 2.43a baseline 只固化 launch packet artifact，不得自动进入 2.43b / 2.43c。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.43a Git baseline；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 12:06 Phase 2.43b
- goal: Codex B review Phase 2.43a baseline and write Phase 2.43b MVP Pilot pre-flight smoke prompt artifact handoff。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag / `origin/main` 检查：Phase 2.43a baseline 已完成，HEAD `5423497`，tag `phase-2.43a-mvp-pilot-launch-packet-baseline`。
  - `git diff-tree --no-commit-id --name-only -r HEAD`：确认 Phase 2.43a baseline 只包含 launch packet 与交接文档白名单。
  - 本轮不运行 API / CLI smoke，不运行 pytest，不生成真实 MVP Pilot report。
- validation: Phase 2.43a baseline 通过 Codex B 状态复核；下一步收缩为 Phase 2.43b pre-flight smoke prompt / runbook artifact，只做 docs-only artifact，不启动真实 Pilot。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得触碰；Phase 2.43b 不得运行真实 API / CLI smoke、生成真实 report、rollout approval、repair authorization、DB 写入或 Data Steward 实现。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；完成 Phase 2.43b artifact 后停止等待 Codex B review，不自动 baseline，不自动发起 Codex C。
- commit/tag if any: 无；本轮只是 Phase 2.43b prompt handoff，不提交 Git。

## 2026-05-06 12:09 Phase 2.43b
- goal: Create MVP Pilot pre-flight smoke prompt / runbook artifact for Codex C。
- changed_files:
  - `docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - 新增 prompt `git diff --check --no-index /dev/null docs/MVP_PILOT_PREFLIGHT_SMOKE_PROMPT.md`：通过。
  - Phase 2.43b keyword boundary `rg`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
  - `git status --short`：已复核。
- validation: 新增 pre-flight smoke prompt，覆盖 API / CLI、fresh session、alias、citation、evidence policy、Missing Evidence、facts/transcript/snapshot boundary、No-Go / Pause / Go 与人工决策声明；本轮不运行真实 API / CLI，不生成真实 report。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得 stage / commit；`docs/NEXT_CODEX_A_PROMPT.md` 是既有 handoff dirty，本轮不修改；Phase 2.43b 不得被解释为 Pilot 启动、production rollout、repair、Data Steward 实现、自动审标或自动经营决策。
- next: Codex B review Phase 2.43b artifact；通过后再决定是否交给 Codex C 做真实 pre-flight smoke。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 12:18 Phase 2.43b
- goal: Codex B review Phase 2.43b pre-flight smoke prompt artifact and write Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - Phase 2.43b keyword boundary `rg`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
  - `git status --short`：已复核；仅 Phase 2.43b 白名单文件、baseline prompt 与遗留 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty。
- validation: Phase 2.43b pre-flight smoke prompt artifact 通过 Codex B review。Prompt 覆盖 API / CLI、fresh session、alias、query subset、evidence policy flags、Missing Evidence、No-Go / Pause / Go 与 no-data-write 边界；未运行真实 API / CLI，未生成真实 report，未写 DB，未进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，baseline 必须排除；Phase 2.43b baseline 只固化 Codex C pre-flight prompt，不得自动启动 Codex C 或真实 Pilot。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.43b Git baseline；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 13:05 Phase 2.43c
- goal: Codex B review Codex C pre-flight smoke result and hand off internal controlled MVP Pilot Day-1 execution。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git status --short` / HEAD / tag / `origin/main` 检查：Phase 2.43b baseline 已完成，HEAD `ef2e43f`，tag `phase-2.43b-mvp-pilot-preflight-smoke-prompt-baseline`。
  - Codex C pre-flight smoke：API `/health` pass，Hermes CLI pass，四个 alias pass，Q1-Q5 smoke pass，P0 为 0，决策 `Go`。
  - 本轮不运行额外 API / CLI，不运行 pytest，不生成真实 MVP Pilot report。
- validation: Codex C pre-flight 支持启动内部受控 MVP Pilot Day-1。P1 为主标书限价 Missing Evidence，P2 为部分 trace display；二者不阻塞 Go，但必须在 Day-1 review 中记录。
- risks: 本结论不是 production rollout、自动审标、自动投标、自动经营决策、repair、Data Steward 实现或数据写入授权。Day-1 必须保存 raw outputs 与人工复核。
- next: Codex C / Pilot Operator 执行 `docs/MVP_PILOT_DAY1_RUN_SHEET.md`，并按 `docs/MVP_PILOT_LAUNCH_PACKET.md` 与 `docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md` 保存结果；Codex A 当前无开发任务。
- commit/tag if any: 无；本轮只是状态 handoff，不提交 Git。

## 2026-05-06 13:45 Phase 2.43d
- goal: Codex B review Day-1 Pause report and write bounded `@主标书` alias/session fix prompt for Codex A。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - Codex C / Pilot Operator Day-1 report reviewed：API `/health` pass，Hermes CLI pass。
  - Day-1 session `20260506_132914_521b45`：`@主标书` bind 阶段 `alias_bind_failed`，正式 Q1 `alias_missing=true / retrieval_suppressed=true`，Q2-Q10 按 run sheet 暂停。
  - `@硬件清单`、`@C塔方案`、`@会议纪要`：alias bound 且 stable。
  - 本轮不运行 API / CLI smoke，不运行 pytest，不生成真实 report。
- validation: Day-1 Pause 成立，当前 blocker 是 P1 alias/session instability，不是限价 Missing Evidence、深层召回、Data Steward、repair 或 rollout。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍是遗留无关 dirty，不得 stage / commit；修复必须限定主仓 alias/session 路径，完成后需 Codex B review 与 Codex C 复验。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.43d `@主标书` alias/session bounded fix；不提交 Git，不 tag，不 push。
- commit/tag if any: 无；本轮只是 bounded fix prompt handoff，不提交 Git。

## 2026-05-06 14:19 Phase 2.43d
- goal: Execute bounded `@主标书` alias/session Pause fix from `docs/NEXT_CODEX_A_PROMPT.md`。
- changed_files:
  - `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_session_document_scope.py`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
  - `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - 主仓 `python -m py_compile ...`：未执行成功，本机主仓环境无 `python` 命令。
  - 主仓 `./.venv/bin/python -m py_compile agent/memory_kernel/session_document_scope.py agent/memory_kernel/kernel.py agent/memory_kernel/orchestrator.py agent/memory_kernel/context_builder.py agent/memory_kernel/adapters/hermes_memory_adapter.py`：通过。
  - 主仓 `./.venv/bin/python tests/agent/test_session_document_scope.py`：通过，退出码 0。
  - 主仓 `./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py -q`：`51 passed`。
- validation: pending current alias bind 现在在 retrieval 返回多个候选时采用首个 retrieval document 完成绑定，并记录 `alias_bind_ambiguous_retrieval_document_ids`；title bind 多候选仍保持 `ambiguous_title_retrieval` 失败，missing alias suppress 语义未放宽。
- risks: 需要 Codex B review 采用 top document 的 current alias fallback 是否可接受；需要 Codex C 重跑 Day-1 Q1 alias/session 抽样或完整 Day-1；遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 未触碰。
- next: Codex B review 本轮 bounded diff；通过后交 Codex C 复验。当前不 baseline、不 tag、不 push。
- commit/tag if any: 无；本轮按 NEXT 要求不提交 Git。

## 2026-05-06 14:35 Phase 2.43d
- goal: Codex B review Phase 2.43d bounded diff and prepare Codex C real terminal validation prompt。
- changed_files:
  - `docs/NEXT_CODEX_C_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - 主仓 `./.venv/bin/python -m py_compile ...`：通过。
  - 主仓 `./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py -q`：`51 passed`。
  - Hermes_memory `git diff --check`：通过。
  - Hermes_memory `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - Hermes_memory `git check-ignore -v reports/agent_runs/latest.json`：通过。
- validation: Codex B review 通过。current alias fallback 只在 pending current alias bind 路径采用 top document，并保留 ambiguous diagnostics；title bind 多候选仍失败，missing alias suppress 语义未放宽。
- risks: 仍需 Codex C 真实终端复验确认 Day-1 Q1 不再 alias_missing / retrieval_suppressed；`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`、主仓 `uv.lock` 与若干既有 dirty 不属于本轮 baseline。
- next: Codex C 执行 `docs/NEXT_CODEX_C_PROMPT.md`；通过后再写 Phase 2.43d baseline prompt。
- commit/tag if any: 无；本轮只是 Codex C validation prompt handoff，不提交 Git。

## 2026-05-06 15:05 Phase 2.43d
- goal: Absorb Codex C Day-1 continuation `Go` result and write dual-repo Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - Codex C Day-1 continuation reviewed：API `/health` pass，Hermes CLI pass。
  - session `20260506_143354_d4ad05`：`@主标书` Q1-Q2 resolved，`alias_missing=false`，`retrieval_suppressed=false`。
  - Day-1 10 条 query：`6 pass / 4 partial / 0 fail`，P0 为 0，Decision 为 `Go`。
  - 本轮不运行额外 API / CLI，不运行 pytest，不提交 Git。
- validation: Baseline Gate 已满足：phase acceptance 明确、Codex B review 通过、Codex C 真实终端通过、文档已同步、下一步将恢复内部受控 MVP Pilot continuation / issue intake。
- risks: baseline 必须 selective staging；主仓 `agent/memory_kernel/adapters/hermes_memory_adapter.py`、`uv.lock`、PHASE211E 文档和 adapter reload 测试不属于本轮；Hermes_memory `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 不属于本轮。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.43d 双仓 Git baseline；完成后停止等待 Codex B review。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 15:40 Phase 2.44
- goal: Absorb Phase 2.43d baseline and prepare MVP Pilot continuation / issue intake planning prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - Phase 2.43d baseline state reviewed：Hermes_memory HEAD `d62852b`，tag `phase-2.43d-main-tender-alias-session-baseline`。
  - Codex C Day-1 continuation result reviewed：`6 pass / 4 partial / 0 fail`，P0 为 `0`，Decision 为 `Go`。
  - 本轮不运行 API / CLI，不运行 pytest，不生成真实 report 或 issue records。
- validation: 下一轮收缩为 docs-only planning，目标是把 Day-1 P1/P2 尾项纳入 issue intake / Pilot continuation 规则；不修 retrieval、不写 DB、不进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍为遗留无关 dirty，不得触碰；Phase 2.44 完成后需 Codex B review，不自动 baseline。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.44 docs-only planning。
- commit/tag if any: 无；本轮只是 next prompt handoff，不提交 Git。

## 2026-05-06 15:42 Phase 2.44
- goal: Plan internal MVP Pilot continuation / issue intake after Phase 2.43d baseline and Codex C Day-1 continuation Go.
- changed_files:
  - `docs/PHASE244_MVP_PILOT_CONTINUATION_ISSUE_INTAKE_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过，命中 `reports/agent_runs/.gitignore`。
  - `git status --short`：通过；显示 Phase 2.44 文档变更与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
- validation: docs-only plan records internal controlled Pilot continuation, Day-1 P1/P2 issue candidates, Go / Pause / No-Go rules, and human review boundaries; no real issue records/report/API/DB/index work.
- risks: P1/P2 tails are recorded, not fixed; inherited dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` remains out of scope; no rollout / repair / Data Steward.
- next: Codex B review Phase 2.44 planning; if approved, choose Phase 2.44 docs baseline or Phase 2.44a sanitized issue intake dry-run / recorder worksheet.
- commit/tag if any: 无；本轮不提交 Git。

## 2026-05-06 15:55 Phase 2.44
- goal: Codex B review Phase 2.44 planning and write docs-only Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - Phase 2.44 plan reviewed：`docs/PHASE244_MVP_PILOT_CONTINUATION_ISSUE_INTAKE_PLAN.md` 覆盖 Day-1 continuation Go、P1/P2 issue candidates、record-now vs fix-now、Go / Pause / No-Go 与人工复核责任。
  - `git diff --check`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
- validation: Codex B review 通过。Phase 2.44 是 docs-only planning，不写代码、不生成真实 report 或 issue records、不进入 repair / rollout / Data Steward。
- risks: baseline 必须 selective staging，排除遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`；baseline 后不得自动进入 Phase 2.44a。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.44 docs-only Git baseline。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 16:46 Phase 2.44a
- goal: Create MVP Pilot Day-1 issue intake worksheet and sanitized JSON template artifact.
- changed_files:
  - `docs/MVP_PILOT_DAY1_ISSUE_INTAKE_WORKSHEET.md`
  - `docs/MVP_PILOT_DAY1_ISSUE_INTAKE_TEMPLATE.json`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - `uv run python -m json.tool docs/MVP_PILOT_DAY1_ISSUE_INTAKE_TEMPLATE.json >/tmp/day1_issue_template_check.json`：通过。
  - `uv run python scripts/phase237a_pilot_issue_intake.py --print-template >/tmp/phase237a_issue_template.json`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过，命中 `reports/agent_runs/.gitignore`。
  - `git status --short`：通过；显示 Phase 2.44a 文档变更与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
- validation: worksheet and template are docs/template artifacts only; no real issue records, no Pilot report, no API/CLI, no DB/index writes.
- risks: current validator issue_type enum does not include every Day-1 label; worksheet maps Day-1 labels to validator-compatible issue_type values. Inherited dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` remains out of scope.
- next: Codex B review Phase 2.44a artifact; if approved, write Phase 2.44a docs-only baseline prompt.
- commit/tag if any: 无；本轮不提交 Git。

## 2026-05-06 16:10 Phase 2.44a
- goal: Confirm Phase 2.44 baseline and write next artifact prompt for MVP Pilot issue intake worksheet / sanitized template。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - Phase 2.44 baseline checked：HEAD `afb5a29`，tag `phase-2.44-pilot-continuation-issue-intake-plan-baseline`。
  - `reports/agent_runs/latest.json` indicates baseline / pushed true。
  - 本轮不运行 API / CLI，不运行 pytest，不生成真实 report 或 issue records。
- validation: 下一轮收缩为 docs/template artifact，目标是人工 recorder 可用的 issue intake worksheet 与 sanitized JSON template；不修 retrieval、不写 DB、不进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍为遗留无关 dirty，不得触碰；Phase 2.44a 完成后需 Codex B review，不自动 baseline。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.44a worksheet / template artifact。
- commit/tag if any: 无；本轮只是 next prompt handoff，不提交 Git。

## 2026-05-06 17:05 Phase 2.44a
- goal: Codex B review Phase 2.44a worksheet / sanitized template artifact and write docs-only Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - `uv run python -m json.tool docs/MVP_PILOT_DAY1_ISSUE_INTAKE_TEMPLATE.json >/tmp/day1_issue_template_check.json`：通过。
  - `uv run python scripts/phase237a_pilot_issue_intake.py --input docs/MVP_PILOT_DAY1_ISSUE_INTAKE_TEMPLATE.json --strict >/tmp/day1_issue_template_validate.json`：通过，`invalid_count=0`。
  - `uv run python scripts/phase237a_pilot_issue_intake.py --print-template >/tmp/phase237a_issue_template.json`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
- validation: Codex B review 通过。worksheet 覆盖必填字段、Day-1 quick-fill、priority、Go/Pause/No-Go 与禁止项；template 不含真实 document/version/citation/raw answer/session，且兼容现有 validator。
- risks: baseline 必须 selective staging，排除遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`；baseline 后不得自动进入 Phase 2.44b。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.44a docs-only Git baseline。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

## 2026-05-06 17:19 Phase 2.44b
- goal: Plan sanitized issue intake dry-run / recorder workflow for Day-1 continuation P1/P2 findings.
- changed_files:
  - `docs/PHASE244B_SANITIZED_ISSUE_INTAKE_DRY_RUN_PLAN.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过，命中 `reports/agent_runs/.gitignore`。
  - `git status --short`：通过；显示 Phase 2.44b 文档变更与遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
- validation: docs-only plan defines sanitized input workflow, strict validation commands, local ignored storage, review gate, and stop conditions; no real issue records/report/API/DB/index work.
- risks: P1/P2 findings remain issue intake candidates, not fixes; real issue records must stay ignored; inherited dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` remains out of scope.
- next: Codex B review Phase 2.44b planning; if approved, write Phase 2.44b docs-only baseline prompt or plan Phase 2.44c fake/temp-data dry-run.
- commit/tag if any: 无；本轮不提交 Git。

## 2026-05-06 17:10 Phase 2.44b
- goal: Confirm Phase 2.44a baseline and write next docs-only planning prompt for sanitized issue intake dry-run / recorder workflow。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - Phase 2.44a baseline checked：HEAD `14c5640`，tag `phase-2.44a-pilot-issue-intake-worksheet-baseline`。
  - `reports/agent_runs/latest.json` indicates baseline / pushed true。
  - 本轮不运行 API / CLI，不运行 pytest，不生成真实 Pilot report 或 issue records。
- validation: 下一轮收缩为 docs-only planning，目标是规划 sanitized issue intake dry-run / recorder workflow；不生成真实 issue records、不修 retrieval、不写 DB、不进入 rollout / repair / Data Steward。
- risks: `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 仍为遗留无关 dirty，不得触碰；Phase 2.44b 完成后需 Codex B review，不自动 baseline。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.44b planning。
- commit/tag if any: 无；本轮只是 next prompt handoff，不提交 Git。

## 2026-05-06 17:26 Phase 2.44b
- goal: Codex B review Phase 2.44b sanitized issue intake dry-run / recorder workflow planning and write docs-only Git baseline prompt。
- changed_files:
  - `docs/NEXT_CODEX_A_PROMPT.md`
  - `docs/ACTIVE_PHASE.md`
  - `docs/PHASE_BACKLOG.md`
  - `docs/HANDOFF_LOG.md`
  - `docs/NIGHTLY_SPRINT_QUEUE.md`
  - `docs/TODO.md`
  - `docs/DEV_LOG.md`
  - `reports/agent_runs/latest.json`（ignored，本地状态）
- tests:
  - `git diff --check`：通过。
  - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`：通过。
  - `git check-ignore -v reports/agent_runs/latest.json`：通过。
  - Phase 2.44b plan reviewed：覆盖 inputs / sanitization、recorder workflow、dry-run validation、issue type mapping、local storage、review gate、stop conditions 与 next recommendation。
- validation: Codex B review 通过。Phase 2.44b 是 docs-only planning，不生成真实 issue records / Pilot report，不写 DB / index，不进入 retrieval fix、repair、rollout 或 Data Steward。
- risks: baseline 必须 selective staging，排除遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`；baseline 后不得自动进入 Phase 2.44c。
- next: Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.44b docs-only Git baseline。
- commit/tag if any: 无；本轮只是 baseline prompt handoff，不提交 Git。

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

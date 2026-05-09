# NEXT_CODEX_A_PROMPT

## Phase 2.55a Codex B Review Passed - Selective Git Baseline

你是 Codex A。本轮只做 Phase 2.55a Internal MVP Real Upload Smoke 的 selective Git baseline。

Codex B 已审核 Codex A 交接、ignored run record 与本地状态，结论如下：

1. Phase 2.55a 单文件真实 upload / ingestion / retrieval smoke 通过。
2. API hybrid retrieval 与 Hermes CLI retrieval 均只返回新上传 document evidence。
3. `metadata_as_answer=false`、`facts_as_answer=false`、`snapshot_as_answer=false`、`requires_retrieval_evidence=true` 边界保持。
4. 未发现第三文件污染。
5. 不需要 Codex C targeted validation。
6. API 顶层 `citations=[]` 但 result-level / CLI citations 可见，记录为 P2 展示尾项，不阻塞 baseline。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`
8. `reports/agent_runs/latest.json`
9. `reports/internal_mvp_runs/phase255a_real_upload_smoke_20260509_102038.json`

## 白名单文件

只允许 stage / commit 以下 tracked 文件：

1. `docs/ACTIVE_PHASE.md`
2. `docs/PHASE_BACKLOG.md`
3. `docs/HANDOFF_LOG.md`
4. `docs/NIGHTLY_SPRINT_QUEUE.md`
5. `docs/NEXT_CODEX_A_PROMPT.md`
6. `docs/NEXT_CODEX_C_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

不得 stage：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. `reports/internal_mvp_runs/*.json`
6. 任何 app / scripts / tests / migrations 文件

## Baseline 步骤

1. 复核 `git status --short`，确认除白名单 tracked docs 外没有其他待 stage 文件被纳入。
2. 运行：
   - `git diff --check`
   - `uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json`
   - `uv run python -m json.tool reports/internal_mvp_runs/phase255a_real_upload_smoke_20260509_102038.json >/tmp/phase255a_run_record_check.json`
   - `git check-ignore -v reports/agent_runs/latest.json`
   - `git check-ignore -v reports/internal_mvp_runs/phase255a_real_upload_smoke_20260509_102038.json`
3. selective stage 白名单 8 个 tracked docs。
4. 复核 staged diff：不得包含 DB / NAS / Data Steward branch docs，不得包含 `PHASE238...`，不得包含 ignored run record。
5. commit：
   - `chore: baseline phase 2.55a internal mvp upload smoke`
6. tag：
   - `phase-2.55a-internal-mvp-upload-smoke-baseline`
7. push 当前分支到 origin，并 push tag。
8. 更新 ignored `reports/agent_runs/latest.json` 为 baseline 状态。
9. 停止等待 Codex B review；不得自动进入 Phase 2.56。

## 硬边界

1. 不执行 cleanup / delete / repair / backfill / reindex / migration。
2. 不再次上传文件。
3. 不读取或输出上传文件正文。
4. 不修改 app / scripts / tests / migrations / Hermes 主仓代码。
5. 不修改 retrieval contract。
6. 不修改 memory kernel 主架构。
7. 不进入 Data Steward / BIM asset catalog / Graph / Spatial Index / subagent scheduler。
8. 不进入 production rollout。

## 完成报告必须包含

1. commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`。
5. 明确说明 ignored run record 未入库。
6. 当前 P2 展示尾项：API 顶层 `citations=[]` 但 result-level / CLI citations 可见。

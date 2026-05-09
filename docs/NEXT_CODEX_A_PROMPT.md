# NEXT_CODEX_A_PROMPT

## Phase 2.56b Codex B Review Passed - Docs-only Git Baseline

你是 Codex A。本轮只做 Phase 2.56b Natural Import Real Smoke Planning 的 docs-only Git baseline。

Codex B 已 review Phase 2.56b planning，结论如下：

1. 规划覆盖授权门槛、样本要求、执行步骤、验收字段、stop conditions、run record 和非目标。
2. 明确 Phase 2.56b 不执行真实 upload、不运行 API / CLI smoke、不写 DB / OpenSearch / Qdrant。
3. 明确 Phase 2.56c 才可在用户显式授权后执行真实自然语言导入 smoke。
4. Data Steward / DB / NAS / BIM 继续后置且独立。
5. 文档检查通过：`git diff --check`、latest JSON 校验、latest ignore 检查。

## 白名单文件

只允许 stage / commit：

1. `docs/PHASE256B_NATURAL_IMPORT_REAL_SMOKE_PLAN.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/NIGHTLY_SPRINT_QUEUE.md`
6. `docs/NEXT_CODEX_A_PROMPT.md`
7. `docs/NEXT_CODEX_C_PROMPT.md`
8. `docs/TODO.md`
9. `docs/DEV_LOG.md`

不得 stage：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. 任何 app / scripts / tests / migrations 文件。

## 验证

运行：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
```

## Git 操作

1. selective stage 白名单文件。
2. 复核 staged diff 不包含禁止文件。
3. commit message：
   - `docs: plan phase 2.56b natural import real smoke`
4. tag：
   - `phase-2.56b-natural-import-real-smoke-plan-baseline`
5. push 当前分支到 `origin`。
6. push tag 到 `origin`。

## 完成后更新

更新 ignored `reports/agent_runs/latest.json`：

1. `status=baseline`
2. 写入 commit hash。
3. 写入 tag。
4. 写入 push 结果。
5. `needs_codex_b_review=true`
6. `needs_codex_c_validation=false`

不要 stage `latest.json`。

## 硬边界

1. 不调用真实 Hermes_memory upload API。
2. 不上传文件。
3. 不启动 API / CLI smoke。
4. 不写 DB / facts / document_versions / audit_logs。
5. 不写 OpenSearch / Qdrant。
6. 不 cleanup / delete / repair / backfill / reindex / migration。
7. 不修改 retrieval contract。
8. 不修改 memory kernel 主架构。
9. 不进入 Data Steward / DB / NAS / BIM 分支实现。
10. 不进入 production rollout。
11. baseline 后停止，不进入 Phase 2.56c。

## 完成报告必须包含

1. staged 文件。
2. 检查结果。
3. commit hash。
4. tag。
5. push 结果。
6. 最终 `git status --short`。
7. 明确说明未执行真实 upload / API / CLI smoke。

# NEXT_CODEX_A_PROMPT

## Phase 2.59 Git Baseline Prompt

你是 Hermes_memory 主线开发 agent。本轮只执行 Phase 2.59 Natural Import Second Smoke Planning 的 docs-only Git baseline。

Codex B 已审核 Phase 2.59 规划：方向正确，边界清楚，可以 baseline。不要进入真实 smoke，不要进入 Phase 2.60，不要上传文件。

## 本轮目标

Phase 2.59 Natural Import Second Smoke / Operator Authorization Planning 收口与 Git baseline。

## 必读文件

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/HANDOFF_LOG.md`
5. `docs/PHASE259_NATURAL_IMPORT_SECOND_SMOKE_PLAN.md`
6. `docs/NEXT_CODEX_C_PROMPT.md`
7. `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
8. `docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`
11. `reports/agent_runs/latest.json`

## 允许提交的白名单文件

只允许 stage / commit 下列 Phase 2.59 相关文件：

1. `docs/PHASE259_NATURAL_IMPORT_SECOND_SMOKE_PLAN.md`
2. `docs/NEXT_CODEX_C_PROMPT.md`
3. `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`
4. `docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`
5. `docs/ACTIVE_PHASE.md`
6. `docs/PHASE_BACKLOG.md`
7. `docs/HANDOFF_LOG.md`
8. `docs/NIGHTLY_SPRINT_QUEUE.md`
9. `docs/NEXT_CODEX_A_PROMPT.md`
10. `docs/TODO.md`
11. `docs/DEV_LOG.md`

## 必须排除的文件

不要 stage / commit 下列文件：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
3. `docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
4. `reports/agent_runs/latest.json`
5. 任何 `reports/**/*.json`
6. 任何真实源文件、上传文件、smoke evidence JSON
7. 任何代码、测试、migration、schema、OpenSearch/Qdrant/DB 相关文件

## 验证步骤

只运行轻量静态检查：

```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_phase259_baseline_check.json
git status --short
```

不运行 pytest；本轮 docs-only baseline。

## Git baseline 步骤

1. 确认 dirty 中除白名单外只有历史无关 dirty / DB 分支草稿，且不得 stage。
2. selective stage 白名单文件。
3. 运行：

```bash
git diff --cached --check
git diff --cached --name-only
```

4. commit：

```bash
git commit -m "docs: plan phase 2.59 natural import second smoke"
```

5. tag：

```bash
git tag phase-2.59-natural-import-second-smoke-plan-baseline
```

6. push 当前分支与 tag：

```bash
git push origin HEAD
git push origin phase-2.59-natural-import-second-smoke-plan-baseline
```

7. 更新 ignored `reports/agent_runs/latest.json`：
   - `phase`: `Phase 2.59 Natural Import Second Smoke Planning`
   - `status`: `baseline`
   - `git.commit`: 当前 commit hash
   - `git.tag`: `phase-2.59-natural-import-second-smoke-plan-baseline`
   - `git.pushed`: `true`
   - `needs_codex_b_review`: `false`
   - `needs_codex_c_validation`: `false`
   - `next_recommendation`: 等用户提供第二个小型非敏感文件路径并显式授权后，Codex C 才执行 `docs/NEXT_CODEX_C_PROMPT.md`；否则继续主线 planning / usability。

8. 最终确认：

```bash
git status --short
git check-ignore -q reports/agent_runs/latest.json && echo ignored
```

## 硬边界

本轮禁止：

1. 不上传文件。
2. 不执行 Hermes_memory API smoke。
3. 不执行 Hermes CLI smoke。
4. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
5. 不 cleanup / delete / repair / backfill / reindex / migration。
6. 不进入 DB / NAS / Data Steward 实现。
7. 不进入 production rollout。
8. 不自动执行 `docs/NEXT_CODEX_C_PROMPT.md`。
9. 不自动选择第二个真实文件。
10. 不 stage 历史无关 dirty 或 DB 分支草稿。

## 完成后停止

完成 baseline 后立即停止，输出：

1. commit hash
2. tag
3. push 结果
4. final `git status --short`
5. 是否确认未上传文件 / 未写 DB / 未执行 API/CLI smoke
6. 下一步：等待用户提供授权文件后再让 Codex C 执行 `docs/NEXT_CODEX_C_PROMPT.md`

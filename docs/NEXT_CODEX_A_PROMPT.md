# NEXT_CODEX_A_PROMPT

这是 Codex A 的下一轮文件化执行入口。Codex B 已 review Phase 2.50c Sanitized Internal MVP Evidence Pack Template，结论：通过。下一轮只允许做 docs-only Git baseline。

## 本轮目标

Phase 2.50c Sanitized Internal MVP Evidence Pack Template Git Baseline。

只做 selective staging / commit / tag / push；不生成真实 evidence pack，不进入 Phase 2.50d / 2.53、真实 Mac Mini deployment、API / CLI smoke、repair、rollout 或 Data Steward。

## Codex B Review 结论

通过，理由：

1. `docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.json` 是 valid JSON。
2. JSON / Markdown template 只含 placeholder / sanitized 字段，未发现真实 UUID、客户内容、本机路径、secret、raw model output。
3. JSON template 覆盖 `source_files`、P0/P1/P2/P3、citation coverage、Missing Evidence、facts/transcript/snapshot flags、third-document contamination、decision、PRD linkage、not_claimable、redaction_confirmed。
4. 固定安全字段存在：`template_only=true`、`production_rollout=false`、`repair_authorized=false`、`data_mutation=false`、`destructive_actions=[]`。
5. Markdown template 覆盖 operator / reviewer metadata、source artifact checklist、severity summary、citation / Missing Evidence / evidence policy checklist、PRD linkage、Go / Pause / No-Go、not-claimable、redaction / ignored storage。
6. `docs/PHASE250C_INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md` 明确模板不是 rollout / customer delivery / automatic tender review / automatic bid / automatic business decision / repair authorization。
7. 文档明确未来真实 evidence pack 需要另开 phase、显式授权，并写入 ignored path。
8. 未生成真实 evidence pack、未读取真实 reports、未运行 API / CLI、未写 DB / index、未进入 rollout。

## 必须先复核

```bash
cd /Users/Weishengsu/Hermes_memory
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
python3 -m json.tool docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.json >/tmp/internal_mvp_evidence_pack_template_check.json
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
git check-ignore -v reports/agent_runs/latest.json
git check-ignore -v reports/internal_mvp_runs/example.json
git check-ignore -v reports/internal_mvp_runs/example.md
git check-ignore -v reports/internal_mvp_runs/latest.json
git check-ignore -v reports/deployment_records/example.json
git check-ignore -v reports/deployment_records/example.md
```

## 允许 stage 的文件

只允许 stage 以下文件：

1. `docs/PHASE250C_INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md`
2. `docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.json`
3. `docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md`
4. `docs/ACTIVE_PHASE.md`
5. `docs/PHASE_BACKLOG.md`
6. `docs/HANDOFF_LOG.md`
7. `docs/NIGHTLY_SPRINT_QUEUE.md`
8. `docs/NEXT_CODEX_A_PROMPT.md`
9. `docs/TODO.md`
10. `docs/DEV_LOG.md`

## 必须排除 / 不得 stage

以下文件不得 stage / commit：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`
4. `reports/agent_runs/latest.json`
5. 任何真实 `reports/internal_mvp_runs/**`
6. 任何真实 `reports/deployment_records/**`
7. 任何真实 reports / reviews / run records。

## Baseline 操作

只在 staged 文件完全等于白名单时继续。

```bash
cd /Users/Weishengsu/Hermes_memory
git add docs/PHASE250C_INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md \
  docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.json \
  docs/INTERNAL_MVP_EVIDENCE_PACK_TEMPLATE.md \
  docs/ACTIVE_PHASE.md \
  docs/PHASE_BACKLOG.md \
  docs/HANDOFF_LOG.md \
  docs/NIGHTLY_SPRINT_QUEUE.md \
  docs/NEXT_CODEX_A_PROMPT.md \
  docs/TODO.md \
  docs/DEV_LOG.md

git diff --cached --name-only
```

确认 staged 仅上述 10 个文件后：

```bash
git commit -m "docs: baseline phase 2.50c internal mvp evidence pack template"
git tag phase-2.50c-internal-mvp-evidence-pack-template-baseline
git push origin main
git push origin phase-2.50c-internal-mvp-evidence-pack-template-baseline
```

## Baseline 后复核

```bash
git status --short
git rev-parse --short HEAD
git tag --points-at HEAD
```

允许最终仍显示 out-of-scope dirty / untracked only if 它们是：

1. `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
2. `docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`
3. `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`

如果出现其他 dirty，停止并写交接。

## 硬禁止

1. 不写功能代码。
2. 不新增 / 修改 scripts 或 tests。
3. 不生成真实 evidence pack。
4. 不执行真实 Mac Mini deployment。
5. 不启动 / 停止服务。
6. 不运行 API / CLI smoke。
7. 不读取真实 reports / run records。
8. 不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
9. 不执行 repair / backfill / reindex / cleanup / delete / migration。
10. 不进入 production rollout。
11. 不进入 Data Steward / BIM 实现。
12. 不修改 retrieval contract。
13. 不修改 memory kernel 主架构。
14. baseline 后不得自动进入 Phase 2.50d / 2.53。

## 完成后状态

更新 `reports/agent_runs/latest.json`（ignored）：

1. `phase=Phase 2.50c Sanitized Internal MVP Evidence Pack Template Git Baseline`
2. `status=baseline`
3. 记录 commit hash、tag、push 结果。
4. `needs_codex_b_review=false`
5. `needs_codex_c_validation=false`
6. 下一步建议：进入下一阶段规划，优先考虑 Phase 2.50d evidence pack generator dry-run、Phase 2.53 natural language file import planning，或继续内部 MVP operator evidence work；仍不进入真实 evidence generation / deployment / rollout。

完成后停止，等待 Codex B / 用户检查。

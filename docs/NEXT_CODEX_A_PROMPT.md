# NEXT_CODEX_A_PROMPT

本轮目标
Phase 2.56e Natural Import Real Upload Client + Real Smoke 双仓 selective Git baseline。

Codex B review 结论
1. 已复核 Codex A Phase 2.56e 交接与 ignored run record。
2. 已复跑验证：
   - Hermes 主仓 py_compile：通过。
   - Hermes 主仓 targeted pytest：`34 passed`。
   - Hermes_memory `git diff --check`：通过。
   - `reports/agent_runs/latest.json` 与 `reports/internal_mvp_runs/phase256e_natural_import_real_upload_smoke_20260509_142027.json` JSON 校验：通过。
   - 两个 run record 均被 `.gitignore` 命中。
3. 真实 smoke 确认自然语言导入 path 已调用真实 upload client：`natural_import_path_used=true`、`plain_upload_bypass_used=false`、`alias_persisted=true`、`retrieval_smoke_passed=true`。
4. Codex C 不需要额外复验；不要再次上传该文件，避免重复产生 document/version/chunk/index。

必须先执行的轻量验证
Hermes 主仓 `/Users/Weishengsu/.hermes/hermes-agent`：
```bash
./.venv/bin/python -m py_compile run_agent.py agent/memory_kernel/natural_file_import.py agent/memory_kernel/natural_file_import_flow.py agent/memory_kernel/natural_file_upload_adapter.py agent/memory_kernel/natural_file_import_runtime.py agent/memory_kernel/hermes_memory_upload_client.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py tests/agent/test_hermes_memory_upload_client.py -q
```
Hermes_memory `/Users/Weishengsu/Hermes_memory`：
```bash
git diff --check
uv run python -m json.tool reports/agent_runs/latest.json >/tmp/latest_agent_run_check.json
uv run python -m json.tool reports/internal_mvp_runs/phase256e_natural_import_real_upload_smoke_20260509_142027.json >/tmp/phase256e_run_record_check.json
git check-ignore -v reports/agent_runs/latest.json reports/internal_mvp_runs/phase256e_natural_import_real_upload_smoke_20260509_142027.json
```

Hermes 主仓 selective staging 白名单
只允许 stage：
- `/Users/Weishengsu/.hermes/hermes-agent/run_agent.py`
- `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/hermes_memory_upload_client.py`
- `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_hermes_memory_upload_client.py`
- `/Users/Weishengsu/.hermes/hermes-agent/docs/TODO.md`
- `/Users/Weishengsu/.hermes/hermes-agent/docs/DEV_LOG.md`

Hermes 主仓禁止 stage
- `/Users/Weishengsu/.hermes/hermes-agent/agent/memory_kernel/adapters/hermes_memory_adapter.py`
- `/Users/Weishengsu/.hermes/hermes-agent/uv.lock`
- `/Users/Weishengsu/.hermes/hermes-agent/docs/PHASE211E_REPO_HYGIENE_AND_TRACE_POLISH.md`
- `/Users/Weishengsu/.hermes/hermes-agent/tests/agent/test_memory_kernel_adapter_reload.py`
- 任何未列入白名单的文件。

Hermes_memory selective staging 白名单
只允许 stage：
- `/Users/Weishengsu/Hermes_memory/docs/ACTIVE_PHASE.md`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE_BACKLOG.md`
- `/Users/Weishengsu/Hermes_memory/docs/HANDOFF_LOG.md`
- `/Users/Weishengsu/Hermes_memory/docs/NIGHTLY_SPRINT_QUEUE.md`
- `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_A_PROMPT.md`
- `/Users/Weishengsu/Hermes_memory/docs/NEXT_CODEX_C_PROMPT.md`
- `/Users/Weishengsu/Hermes_memory/docs/TODO.md`
- `/Users/Weishengsu/Hermes_memory/docs/DEV_LOG.md`

Hermes_memory 禁止 stage
- `/Users/Weishengsu/Hermes_memory/docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`
- `/Users/Weishengsu/Hermes_memory/docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
- `/Users/Weishengsu/Hermes_memory/docs/DB_TEAM_AGENT_INTEGRATION_ALIGNMENT.md`
- `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`
- `/Users/Weishengsu/Hermes_memory/reports/internal_mvp_runs/phase256e_natural_import_real_upload_smoke_20260509_142027.json`
- 任何未列入白名单的文件。

提交与 tag
1. Hermes 主仓提交信息：`feat: add natural import real upload client`
2. Hermes_memory 提交信息：`docs: baseline phase 2.56e natural import real upload smoke`
3. tag：`phase-2.56e-natural-import-real-upload-smoke-baseline`
4. Hermes 主仓推送到既有可写远端/分支：`backup2 codex/phase-2.11d-context-regression-baseline`，并推送 tag。
5. Hermes_memory 推送当前分支到 `origin`，并推送 tag。

完成后更新 ignored 状态
更新 `/Users/Weishengsu/Hermes_memory/reports/agent_runs/latest.json`：
- `status=baseline`
- 写入两个仓库 commit hash、tag、pushed=true
- `needs_codex_b_review=false`
- `needs_codex_c_validation=false`
- 下一步建议：Phase 2.57 planning，围绕自然语言导入可用性 evidence pack / Mac mini MVP operator runbook，不进入 DB/NAS/Data Steward 实现。

硬边界
1. 不再次执行真实 upload，不重复上传同一文件。
2. 不 cleanup/delete/repair/backfill/reindex。
3. 不写 DB/facts/document_versions/audit_logs/OpenSearch/Qdrant。
4. 不进入 production rollout。
5. 不进入 DB/NAS/Data Steward 分支实现。
6. baseline 后停止，不自动进入 Phase 2.57。

返回要求
输出：
1. 两仓 commit hash。
2. tag。
3. push 结果。
4. 最终 `git status --short`，明确哪些无关 dirty 仍保留。
5. 确认 ignored run records 未被提交。

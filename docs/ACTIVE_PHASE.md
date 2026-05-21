# Active Phase

- 当前 phase：Phase 2.112 Natural Import Workspace Retrieval Fix Prompt。
- 背景：用户通过 OpenWebUI -> 8642 Hermes backend 完成真实自然语言导入链路验证：`natural_import_detected=true`、`real_upload_enabled=true`、`upload_adapter_status=executed`、`ingestion_status=upload_succeeded`、`document_id=2baf5527-42c9-4467-8856-573e54c97121`、`version_id=b2efc465-cde8-4aef-a113-5c8615929719`、`chunk_count=6`、`indexed_count=6`。
- 当前阻塞：alias 表面绑定为整份文档，但 same-session retrieval 仍返回 `retrieval_evidence_document_ids=[]`、citation=`Missing Evidence`；一次手动 alias memory 写入还触发普通 memory quota，说明文件 workspace / alias state 不应写入 ordinary long-term memory。
- 本轮目标：新增 Phase 2.112 修复计划并写入 Codex A 执行 prompt，要求修复 natural import 成功后的 session alias / active document / scoped retrieval / citation 链路，并加入自动别名与模糊文件发现的最小体验边界。
- 修改文件：`docs/PHASE2112_NATURAL_IMPORT_WORKSPACE_RETRIEVAL_FIX_PLAN.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 当前结论：natural import real upload / ingestion / index 已有真实证据，但 full natural import usability 仍是 partial；Phase 2 closeout 继续 blocked，直到 Codex A 修复 same-session retrieval / citation 并经真实验收通过。
- 是否建议进入 Phase 3：否。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 的 Phase 2.112 bounded fix；完成后交 Codex B review，再由用户/测试机做真实 OpenWebUI / 8642 验收。
- 当前仍禁止：production rollout、NAS scan、DB CRUD/SQL、Gateway/平台 contract 修改、direct API upload 替代证据、import diagnostics 当 retrieval evidence、raw path/secret/file content 输出、repair/backfill/reindex/delete/migration。

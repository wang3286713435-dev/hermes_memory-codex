# NEXT_CODEX_A_PROMPT

## 当前状态

Phase 2.116b Natural Import Response Polish No-Go Fix 已完成 Codex B review，并已推送 runtime candidate。

已修复：
1. fuzzy discovery 默认候选显示不再暴露 `title/source_name/display_path` 的绝对路径 fallback。
2. same-session alias retrieval 会用实际 returned evidence 覆盖 stale `third_document_contamination`。

已验证：
1. targeted raw-path / contamination regression：`2 passed`
2. Hermes main py_compile：通过
3. Hermes main natural import / flow / session scope / structured citation / file steward regression：`132 passed`

未完成：
1. Codex C / 测试机 Phase 2.116 live validation rerun。
2. Stable closeout baseline。

Runtime candidate:

1. Hermes main commit: `f887d12bf`
2. tag: `phase-2.116b-natural-import-response-polish-fix-runtime-candidate`

## 下一轮目标

Phase 2.116b Codex C live validation gate。

## Codex A 边界

除非用户明确要求继续修改，否则不要继续写代码。

如被要求执行本文件：
1. 读取 `AGENT_OPERATING_PROTOCOL.md`、`ACTIVE_PHASE.md`、`PHASE_BACKLOG.md`、`TODO.md`、`DEV_LOG.md`。
2. 只做状态复核、diff/test 复核或按 Codex B review 反馈做最小修复。
3. 不提交 Git。
4. 不进入下一阶段。
5. 不改 upload adapter、ingestion/indexing、retrieval contract、workspace inference、Gateway、NAS、DWG/RVT/BIM、repair、rollout。

## Codex B review result

Review passed. The raw path sanitizer is display-only, human category slash is preserved, and contamination diagnostics are recomputed from returned evidence instead of stale trace fields.

## Codex C rerun requirement

Codex C 使用同一 Phase 2.116 live validation prompt 复验：
1. Case 1 import success default reply product-facing。
2. Case 2 alias retrieval has `third_document_contamination=false`。
3. Case 3 failure default reply human-readable。
4. Case 4 fuzzy discovery has `raw_path_hidden=true` and no raw `/Users/...` path.

## Hard boundaries

1. 不上传新文件。
2. 不写 DB / facts / versions / OpenSearch / Qdrant。
3. 不执行 repair / backfill / reindex / delete / cleanup。
4. 不进入 rollout。
5. 不提交 Git，除非用户明确给出 baseline prompt。

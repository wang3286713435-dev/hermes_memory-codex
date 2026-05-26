# NEXT_CODEX_A_PROMPT

## 当前状态

Phase 2.116c Natural Import Live No-Go Root Cause Fix 已完成 Codex B review，并已推送 runtime candidate。

已修复：
1. nested `retrieval_trace` / `context_scope` 中的 stale `third_document_contamination` 会随实际 returned evidence 被同步覆盖。
2. fuzzy discovery / active document / evidence / citation display 会对 `file://`、`nas://`、`smb://`、`/Users`、`/Volumes` 等 raw path / URI 只渲染安全 basename。
3. human category slash 保留，例如 `人力配置 / 成本测算`。
4. 真实 out-of-scope returned evidence 仍会触发 `third_document_contamination=true`，未隐藏真实污染。

已验证：
1. live-shape targeted tests：`4 passed`
2. py_compile：通过
3. natural import / flow / session scope / structured citation / file steward regression：`135 passed`

未完成：
1. Codex C / 测试机 Phase 2.116 live validation rerun。
2. Stable closeout baseline。

Runtime candidate:

1. Hermes main commit: `ff11f177c`
2. tag: `phase-2.116c-live-no-go-root-cause-runtime-candidate`

## 下一轮目标

Phase 2.116c Codex C live validation gate。

## Codex A 边界

除非用户明确要求继续修改，否则不要继续写代码。

如被要求执行本文件：
1. 读取 `AGENT_OPERATING_PROTOCOL.md`、`ACTIVE_PHASE.md`、`PHASE_BACKLOG.md`、`TODO.md`、`DEV_LOG.md`。
2. 只做状态复核、diff/test 复核或按 Codex B review 反馈做最小修复。
3. 不提交 Git。
4. 不进入下一阶段。
5. 不改 upload adapter、ingestion/indexing、retrieval contract、workspace inference、Gateway、NAS、DWG/RVT/BIM、repair、rollout。

## Codex B review result

Review passed. Nested contamination cleanup only normalizes stale false positives against actual returned evidence; real unexpected evidence remains flagged. Raw path sanitization covers candidate, active document, evidence, citation, and file metadata display sources while preserving human category labels.

## Codex C rerun requirement

Codex C 使用同一 Phase 2.116 live validation prompt 复验：
1. Case 1 import success default reply product-facing。
2. Case 2 alias retrieval has `third_document_contamination=false`。
3. Case 3 failure default reply human-readable。
4. Case 4 fuzzy discovery has `safe_candidates_present=true` and `raw_path_hidden=true` with no `/Users/`、`/Volumes/`、`file://`、`nas://`、`smb://` output.

## Hard boundaries

1. 不上传新文件。
2. 不写 DB / facts / versions / OpenSearch / Qdrant。
3. 不执行 repair / backfill / reindex / delete / cleanup。
4. 不进入 rollout。
5. 不提交 Git，除非用户明确给出 baseline prompt。

# NEXT_CODEX_A_PROMPT

## Phase 2.116d Codex C Live Validation Gate

当前 Phase 2.116d 已完成 Codex B review，并已推送 runtime candidate。

## 当前状态

1. Hermes main runtime candidate：
   - commit: `6e6232ff1`
   - tag: `phase-2.116d-live-no-go-followup-runtime-candidate`
2. Codex B review 结论：通过。
3. Stable closeout：未批准，必须等待 Codex C / 测试机 live validation。

## 已修复范围

1. Case 2 alias diagnostics：
   - 当 returned evidence document ids 确认落在 alias scope allowed ids 内，外显 alias diagnostics 同步恢复为 `alias_missing=false` / resolved alias。
   - 当 evidence 不在 scope 内，保留 mismatch diagnostics，不隐藏真实第三文件污染。
2. Case 3 import failure raw path：
   - 默认失败回复不再输出 `/Users/`、`/Volumes/`、`file://`、`nas://`、`smb://` 或完整 source path。
3. Case 4 fuzzy discovery：
   - 增加 owner-scoped natural import continuity candidate lookup。
   - 文件候选只暴露 safe alias / workspace / category / basename，不用“删除候选”来规避 raw path。

## 验证结果

1. Targeted fix tests：`4 passed`
2. py_compile touched files：通过
3. Natural import / flow / session scope / structured citation / file steward regression：`138 passed`
4. `git diff --check`：通过

## 下一步

不要继续写代码。下一步应由 Codex C / 测试机更新到：

1. Hermes_memory：`phase-2.116d-live-no-go-followup-review-baseline`
2. Hermes main：`phase-2.116d-live-no-go-followup-runtime-candidate`

然后重跑 Phase 2.116 live validation Case 1-4。

## Codex C 重点验收

1. Case 1：导入成功默认回复仍 product-facing。
2. Case 2：alias retrieval 外显 `alias_missing=false` / resolved alias diagnostics，citation 存在，真实第三文件污染仍可检出。
3. Case 3：import failure default response 不输出 `/Users/`、`/Volumes/`、`file://`、`nas://`、`smb://` 或完整 source path。
4. Case 4：fuzzy discovery 输出 safe candidates，并且不输出 raw path。

## 禁止事项

1. 不继续实现新功能。
2. 不修改 upload adapter / ingestion / indexing。
3. 不修改 retrieval contract。
4. 不修改 memory kernel 主架构。
5. 不写 DB / facts / versions / OpenSearch / Qdrant。
6. 不执行 repair / backfill / reindex / delete / cleanup。
7. 不进入 rollout。
8. 不做 stable closeout，除非 Codex C live validation 返回 Go。

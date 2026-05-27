# NEXT_CODEX_A_PROMPT

## Phase 2.116d Live Validation Go / Phase 2 Final Freeze Checklist

当前 Phase 2.116d 已完成：

1. Codex B review：通过。
2. Hermes main runtime candidate：`6e6232ff1` / `phase-2.116d-live-no-go-followup-runtime-candidate`。
3. Hermes_memory review baseline：`4dd58b2` / `phase-2.116d-live-no-go-followup-review-baseline`。
4. Codex C / 测试机 live validation：`Go`。

## 已通过的 live gate

1. Case 1 import success：pass，默认回复 product-facing。
2. Case 2 alias retrieval diagnostics：pass，`alias_resolved=true`、`alias_missing=false`、evidence/citation 存在、contamination=false。
3. Case 3 import failure raw path：pass，无 raw path / URI / traceback。
4. Case 4 fuzzy discovery safe candidate：pass，有 safe candidate，要求确认，无 raw path。

## 下一步

不要继续写 runtime 代码。

下一步只允许做 Phase 2 final freeze checklist / closeout decision review：

1. 读取 PRD / ROADMAP / TECHNICAL_DESIGN / Phase 2 closeout docs。
2. 对照 Phase 2 原始验收项，列出：
   - 已满足；
   - 已满足但有 scope 限定；
   - 必须进入 Phase 3 的已知缺口；
   - 仍阻塞 Phase 2 stable closeout 的 P0/P1。
3. 如果没有 P0/P1 阻塞，再准备 stable closeout baseline prompt。
4. 不得因为 2.116d Go 就自动进入 Phase 3。

## 禁止事项

1. 不继续新增功能。
2. 不修改 upload adapter / ingestion / indexing。
3. 不修改 retrieval contract。
4. 不写 DB / facts / versions / OpenSearch / Qdrant。
5. 不执行 repair / backfill / reindex / delete / cleanup。
6. 不进入 rollout。
7. 不宣布 production-ready。

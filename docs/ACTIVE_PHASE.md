# Active Phase

- 当前 phase：Phase 2.87b Evidence-only Writer Service Implementation。
- 背景：Phase 2.87a baseline 已完成：commit `fb7baba`，tag `phase-2.87a-write-target-discovery-baseline`，pushed=true。
- 本轮目标：实现 dedicated evidence-only writer service 与测试，仅在 test-local DB/session 中验证 `Document`、`DocumentVersion`、`Chunk`、`CitationRecord` 写入边界。
- 修改文件：`app/services/asset_catalog/evidence_writer.py`、`app/services/asset_catalog/__init__.py`、`tests/test_data_steward_evidence_writer.py`、`docs/PHASE287B_EVIDENCE_ONLY_WRITER.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：新增 `EvidenceOnlyWriter`、`EvidenceWriteDecision`、`EvidenceWriteRollbackPlan` 与 `build_evidence_write_result()`；实现 fail-closed gates、test-local SQLAlchemy session 写入、idempotency duplicate / conflict 判定、run-scoped rollback dry-run planning。
- 测试结果：TDD RED 已观察；目标测试 `7 passed`；`py_compile` 通过；Data Steward regression `133 passed`。
- live smoke 结果：不适用；本轮未运行 API / CLI / real DB / NAS / parser / index / object-store / Agent answer smoke。
- 当前结论：Phase 2.87b implementation 已完成，Codex B review 通过；这不授权真实 evidence write。
- 阻塞点 / 风险点：writer 仍未接 API / CLI runtime；真实 smoke 仍需单独 test-machine operator approval、runtime plan 与 Codex B review；不得把 test-local SQLite/session 写入等同于真实 Hermes DB smoke。
- 是否建议 baseline：是，建议执行 Phase 2.87b selective Git baseline。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.87c 或真实 runtime smoke。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.87b selective Git baseline 后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：否；本阶段不涉及 API / CLI runtime 行为。
- 当前仍禁止：真实 DB 写入、API / CLI runtime wiring、parser、真实文件复制、raw content 读取、NAS scan、OpenSearch / Qdrant / MinIO 写入、audit table write、Agent answer integration、repair、reindex、rollout。

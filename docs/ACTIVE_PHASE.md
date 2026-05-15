# Active Phase

- 当前 phase：Phase 2.87a Exact Write Target Discovery / Implementation Gate。
- 本轮目标：只做 docs-only / read-only discovery，定位未来真实 Hermes evidence write smoke 会触碰的 exact SQLAlchemy models、tables、repository/service methods、transaction boundary 与 rollback / invalidation path。
- 修改文件：`docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：识别候选 evidence tables：`documents`、`document_versions`、`chunks`、`citations`，可选 bookkeeping `ingestion_jobs`；确认现有 `DocumentIngestionService.ingest_uploaded_file()` 不适合直接复用，因为耦合 file bytes、parser/chunker、OpenSearch 与 Qdrant。
- 测试结果：docs-only；已运行 `git diff --check`、latest JSON 校验、latest ignore 校验与 `git status --short`。
- live smoke 结果：不适用；本轮未启动 API / CLI / DB / NAS / parser / index / object-store / Agent answer smoke。
- 当前结论：Phase 2.87a discovery 已完成，Codex B review 通过；direct real write 仍为 `Pause`，后续必须先规划/实现 dedicated evidence-only writer service 与 run-scoped rollback dry-run。
- 阻塞点 / 风险点：缺 dedicated evidence-only service、缺 committed-smoke rollback / invalidation method、缺固定 idempotency metadata location；直接复用 ingestion path 为 `No-Go`。
- 是否建议 baseline：是，建议执行 Phase 2.87a selective docs baseline。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.87b。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.87a selective docs baseline 后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：否；本阶段不涉及 runtime 行为。
- 当前仍禁止：writer implementation、真实 `documents/chunks/document_versions` / audit table 写入、OpenSearch / Qdrant / MinIO 写入、platform DB / Hermes DB 写入、parser、真实文件复制、raw content 读取、NAS scan、Agent answer integration、repair、reindex、rollout。

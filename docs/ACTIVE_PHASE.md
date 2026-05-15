# Active Phase

- 当前 phase：Phase 2.87 First Real Hermes Evidence Write Smoke Planning。
- 本轮目标：只做 docs-only planning，定义未来 Mac mini / 测试机第一次真实 Hermes evidence write smoke 的安全门槛。
- 修改文件：`docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、ignored `reports/agent_runs/latest.json`。
- 完成内容：新增 Phase 2.87 规划，固定 tiny scope、operator approval JSON、feature flags default off、exact write target gate、rollback boundary、sanitized report boundary、Go / Pause / No-Go、DB platform handoff 与 2.87a / 2.88 / 2.89 follow-up split。
- 测试结果：docs-only；已运行 `git diff --check`、latest JSON 校验、latest ignore 校验与 `git status --short`。
- live smoke 结果：不适用；本轮未启动 API / CLI / DB / NAS / parser / index / object-store / Agent answer smoke。
- 当前结论：Phase 2.87 规划已完成，Codex B review 通过；它不是 Phase 2.87a 授权，不允许执行真实写入。
- 阻塞点 / 风险点：真实 evidence write 仍必须等待 Codex B review、用户显式授权、operator approval JSON、exact write target / repository method 命名与 test-machine-only gate。
- 是否建议 baseline：是，建议执行 Phase 2.87 selective docs baseline。
- 是否建议进入下一阶段：否；不得自动进入 Phase 2.87a。
- 下一轮建议：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成 Phase 2.87 selective docs baseline 后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：否；本阶段不涉及 runtime 行为。
- 当前仍禁止：真实 `documents/chunks/document_versions` / audit table 写入、OpenSearch / Qdrant / MinIO 写入、platform DB / Hermes DB 写入、parser、真实文件复制、raw content 读取、NAS scan、Agent answer integration、repair、reindex、rollout。

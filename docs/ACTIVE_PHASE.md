# Active Phase

- 当前 phase：Phase 2.60 Internal MVP Launch Readiness Pack。
- 本轮目标：实现 Mac mini 内部 MVP 使用前的只读 readiness runner、目标测试与 operator 文档闭环。
- 背景：Phase 2.59 baseline 已完成：commit `2603a87`，tag `phase-2.59-natural-import-second-smoke-plan-baseline`。
- 修改文件：`scripts/phase260_mvp_local_readiness_pack.py`、`tests/test_phase260_mvp_local_readiness_pack.py`、`docs/PHASE260_INTERNAL_MVP_LAUNCH_READINESS_PLAN.md`、`docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`、`docs/ACTIVE_PHASE.md`、`docs/PHASE_BACKLOG.md`、`docs/HANDOFF_LOG.md`、`docs/NIGHTLY_SPRINT_QUEUE.md`、`docs/NEXT_CODEX_A_PROMPT.md`、`docs/TODO.md`、`docs/DEV_LOG.md`、`reports/agent_runs/latest.json`。
- 完成内容：新增只读 readiness runner；检查 Git / latest.json / operator docs / second-smoke gate / run_local_api helper / optional API health / dangerous env flags / Data Steward not active；新增目标测试；同步 operator checklist 与 Phase 2.60 文档。
- 测试结果：`uv run pytest tests/test_phase260_mvp_local_readiness_pack.py -q` 已通过；完整验证命令见 `reports/agent_runs/latest.json`。
- live smoke 结果：仅执行离线 dry-run `--skip-api-health`；未运行 API health smoke、未运行 Hermes CLI smoke、未上传文件。
- 当前结论：Phase 2.60 最小实现已通过 Codex B review，等待 selective Git baseline；这不是 production rollout approval。
- 阻塞点 / 风险点：readiness `go` 仅代表内部受控 MVP 使用可由人工 operator 继续；第二真实文件 smoke 仍需单独授权；历史无关 dirty 和 DB/NAS 草稿必须继续排除。
- 是否建议 baseline：是，已写入 `docs/NEXT_CODEX_A_PROMPT.md`。
- 是否建议进入下一阶段：不建议直接进入真实 upload / rollout；先 baseline。
- 下一轮建议：Codex A 执行 Phase 2.60 selective baseline，然后停止。
- 是否需要 Codex B 审核：已完成。
- 是否需要 Codex C 真实终端验收：暂不需要；2.60 可由目标测试与离线 dry-run 验收。
- 禁止：真实上传、第二文件 smoke、Hermes CLI query smoke、自动启动服务、DB/facts/document_versions/audit_logs/OpenSearch/Qdrant 写入、cleanup/delete/repair/backfill/reindex/migration、DB/NAS/Data Steward/BIM/TB 文件池、production rollout。

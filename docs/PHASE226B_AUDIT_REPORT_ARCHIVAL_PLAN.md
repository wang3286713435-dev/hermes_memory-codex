# Phase 2.26b Audit Report Archival Plan

## 1. 本轮目标

Phase 2.26b 规划 readiness audit 定期 smoke / 报告归档。

本阶段只让现有 dry-run 诊断结果可重复、可留痕、可对比；不执行 repair，不创建生产级定时任务，不进入 rollout。

## 2. 当前基线

Phase 2.26a 已收口：

1. commit：`108d080`。
2. tag：`phase-2.26a-repair-plan-dry-run-baseline`。
3. `scripts/phase226_repair_plan_dry_run.py` 已能输出不可执行 repair plan。
4. 当前唯一业务 warning：stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e`。

当前仍不允许自动 repair。

## 3. 规划结论

推荐进入：

**Phase 2.26b：readiness audit 定期 smoke / 报告归档。**

优先目标：

1. 归档 `phase225_readiness_audit.py` 输出。
2. 归档 `phase226_repair_plan_dry_run.py` 输出。
3. 生成轻量 manifest，便于查看最近一次报告和历史趋势。
4. 支持只读 trend diff，比较 warnings / critical / stale_facts 等数量变化。

不推荐现在进入 repair executor。当前更需要先沉淀可审阅的连续报告，避免一次性诊断无法形成运行期趋势。

## 4. Phase 2.26b 最小边界

建议最小实现包含：

1. 新增报告归档脚本或统一模式，例如 `scripts/phase226b_archive_audit_reports.py`。
2. 执行 readiness audit，并把 JSON 保存到 `reports/readiness/`。
3. 执行 repair plan dry-run，并把 JSON 保存到 `reports/repair_plan/`。
4. 每份报告文件名包含 timestamp、status、git commit。
5. 生成轻量 index manifest，记录报告路径、生成时间、status、summary。
6. 使用 `latest.json` 作为最新报告指针；不默认使用 symlink。
7. 支持只读 trend diff，对比最近两份 manifest 或报告。

推荐 CLI 参数：

1. `--json`：输出归档 summary。
2. `--output-dir`：默认 `reports/`。
3. `--document-id`：透传给 repair plan index 抽样。
4. `--include-index-checks`：透传给 repair plan。
5. `--run-readiness` / `--run-repair-plan`：控制执行项。
6. `--diff-latest`：只读比较最近两份报告。

## 5. Git / Report 归档策略

真实报告默认不入 Git。

建议规则：

1. `reports/**/*.json` 默认不提交。
2. `reports/**/latest.json` 默认不提交，因为它是本机运行产物。
3. 如需保留目录结构，只提交 `reports/README.md` 或 `.gitkeep`。
4. 若新增 `.gitignore`，应明确忽略：
   - `reports/readiness/*.json`
   - `reports/repair_plan/*.json`
   - `reports/**/latest.json`
5. 可提交报告模板，例如 `reports/examples/*.template.json`，但不得混入真实本机报告。

理由：

1. 报告可能包含 document_id、fact_id、服务状态和本机环境信息。
2. 报告随运行时间变化，不应污染代码基线。
3. 真正需要长期保存时，应进入专用归档存储或受控 artifact，而不是默认 Git。

## 6. Trend Diff 规划

只读 diff 输出建议包含：

1. `warnings_delta`。
2. `critical_delta`。
3. `stale_facts_delta`。
4. `missing_sources_delta`。
5. `index_inconsistencies_delta`。
6. 新增 / 消失的 entity_id 列表。

判定建议：

1. warning 数量下降：记录为 improved。
2. warning 数量持平：记录为 stable。
3. warning / critical 上升：记录为 regressed。
4. critical 新增：建议 fail 或至少 warn。

## 7. Scheduler / Cron 策略

本阶段只写 runbook 或脚本入口。

不做：

1. 不创建系统级 cron。
2. 不接生产 scheduler。
3. 不创建后台 daemon。
4. 不默认在 CI 中执行昂贵 full eval。

后续如要定期执行，建议先采用人工触发或本地命令：

```bash
uv run python scripts/phase226b_archive_audit_reports.py --json --run-readiness --run-repair-plan
```

## 8. CI / Local Smoke 策略

可规划 local smoke：

1. 编译归档脚本。
2. 单元测试 manifest / diff / Git ignore 策略。
3. dry-run 归档 fake report，不连接真实服务。

CI 默认不跑：

1. 昂贵 full eval。
2. 会写 fixture 的 eval。
3. 真实 OpenSearch / Qdrant / Postgres 依赖检查。

如后续需要 CI，只建议先跑纯单元测试和 fake report 归档测试。

## 9. 非目标

Phase 2.26b 不做：

1. 修改 facts。
2. 修改 document_versions。
3. 修改 OpenSearch。
4. 修改 Qdrant。
5. 执行 repair / backfill / reindex。
6. 创建系统 cron。
7. 进入 rollout。
8. 改 retrieval contract。
9. 改 memory kernel 主架构。
10. 提交真实 report JSON。

## 10. 风险点

1. 报告可能包含真实 document_id / fact_id，需要默认不入 Git。
2. `latest.json` 是本机状态，不应提交真实产物。
3. symlink 在跨平台和压缩包场景中不稳定，本阶段不默认使用。
4. trend diff 容易被误读为 repair 结果，必须明确只是诊断趋势。
5. 如果未来接 CI，需要避免触发会写 DB fixture 的 eval。

## 11. 是否建议进入实现

建议进入 Phase 2.26b 最小实现。

实施前提：

1. 只做报告归档和只读 diff。
2. 默认忽略真实 reports JSON。
3. 不执行 repair executor。
4. 不创建真实定时任务。

## 12. Phase 2.26b 实现结果

Phase 2.26b 最小实现已完成。

新增：

1. `scripts/phase226b_archive_audit_reports.py`。
2. `tests/test_phase226b_archive_audit_reports.py`。
3. `reports/.gitignore`。
4. `reports/README.md`。

已实现能力：

1. 归档 readiness audit JSON 到 `reports/readiness/`。
2. 归档 repair plan JSON 到 `reports/repair_plan/`。
3. 生成本机 `reports/manifest.json`。
4. 生成本机 `reports/latest.json`。
5. 支持 `--diff OLD_JSON NEW_JSON` 输出只读 trend diff。
6. 支持 `--dry-run-preview` 预览写入路径但不写文件。

CLI 边界：

1. 可用 `--readiness-file` / `--repair-plan-file` 归档已有 JSON。
2. 未提供输入文件时，可调用现有 `phase225_readiness_audit.py` / `phase226_repair_plan_dry_run.py` 并捕获 JSON。
3. 不默认执行 index check、repair、backfill、reindex。

## 13. 验证结果

已完成：

1. `uv run python -m py_compile scripts/phase226b_archive_audit_reports.py`：通过。
2. `uv run pytest tests/test_phase226b_archive_audit_reports.py -q`：`6 passed`。
3. 临时目录 live smoke：成功归档 fake readiness JSON 与 fake repair plan JSON。
4. 临时目录 live smoke：成功生成 `manifest.json` 与 `latest.json`。
5. 临时目录 live smoke：成功执行 trend diff，输出 `warnings_delta=1`、`stale_facts_delta=1`、`new_item_ids=["new-fact"]`。

未生成真实仓库 report JSON；live smoke 使用 `mktemp` 临时目录并已清理。

## 14. 当前结论

Phase 2.26b 最小实现已达到阶段目标。

当前仍不建议进入 repair executor。下一步应先做 Git baseline，再评估是否需要：

1. 定期 smoke runbook。
2. 报告归档人工审阅流程。
3. 只读报告历史对比增强。

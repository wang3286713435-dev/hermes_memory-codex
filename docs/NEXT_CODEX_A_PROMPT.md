# NEXT_CODEX_A_PROMPT

当前 DB-1a fake View fixtures / fake adapter contract tests 已完成，Codex A 暂停。

下一轮建议先由 Codex B review / baseline 本轮 DB-1a 改动，不自动进入 DB-2。review 重点如下：

1. 确认 fake fixtures 只覆盖 `ProjectAssetView` / `FileAssetView` / `ModelAssetView` / `AuditEventView`。
2. 确认 adapter 只读，不连接真实 MySQL / NAS / REST。
3. 确认不扫描 `/Volumes/zyzn/卓羽智能项目`。
4. 确认不写 `documents` / `chunks` / OpenSearch / Qdrant。
5. 确认不做正文解析，不改 retrieval contract，不改 memory kernel 主架构。
6. 确认 feature flags 默认 off。
7. 确认 `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md` 已明确 DB-1 / DB-2 / DB-3 验收与合回主线条件。
8. 确认当前不得进入 DB-2 mirror 实现、migration 或真实联调。
9. 复跑目标测试：`uv run --extra dev pytest tests/test_data_steward_fake_adapter.py -q`。
10. 复跑静态检查：`uv run --extra dev ruff check app/services/asset_catalog tests/test_data_steward_fake_adapter.py app/core/config.py`。

DB-2 asset catalog mirror / migration / 真实联调仍需用户后续显式授权。

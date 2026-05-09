# NEXT_CODEX_A_PROMPT

当前 DB-3A Catalog Retrieval Guard 已进入实现 review 阶段。

已完成 baseline / review 事实：

1. DB-1a fake View fixtures / fake adapter contract tests 已 baseline：commit `e9d1556`，tag `phase-db1a-fake-view-adapter-baseline`。
2. DB-2 planning / Ralph Stop hook guard 已 baseline：commit `56f9e47`，tag `phase-db2-planning-ralph-guard-baseline`。
3. DB-1a contract review-fix 已 baseline：commit `e21a1c9`，tag `phase-db1a-contract-review-fix-baseline`。
4. DB-1a malformed cursor review-fix 已 baseline：commit `e16df1a`，tag `phase-db1a-malformed-cursor-review-fix-baseline`。
5. DB-2 dry-run preview 已 baseline：commit `6780d20`，tag `phase-db2-dry-run-preview-baseline`。
6. DB-2 temporary DB proof-of-contract 已 baseline：commit `53337fe`，tag `phase-db2-temp-db-proof-baseline`。
7. DB-2 schema contract freeze 已 baseline：commit `64e139a`，tag `phase-db2-schema-contract-freeze-baseline`。
8. DB-2 schema review response 已 baseline：commit `cffac1f`，tag `phase-db2-schema-review-response-baseline`。
9. DB-2 schema handoff freeze 已 baseline：commit `bd24284`，tag `phase-db2-schema-handoff-freeze-baseline`。

当前 DB-3A 允许范围：

1. fake preview only catalog retrieval guard。
2. 权限 / project scope fail-closed。
3. catalog metadata lookup 与 prompt-ready evidence 分层。
4. content answer 返回 Missing Evidence。

当前 DB-3A 禁止范围：

1. 不写 migration。
2. 不连接真实 MySQL / NAS / REST。
3. 不读真实文件正文。
4. 不写 `documents` / `chunks`。
5. 不写 OpenSearch / Qdrant。
6. 不创建 embedding。
7. 不改 memory kernel 主架构。
8. 不接真实权限系统。

本轮需要 review：

1. `app/services/asset_catalog/retrieval_guard.py`
2. `tests/test_data_steward_asset_catalog_retrieval_guard.py`
3. `docs/DB3_CATALOG_RETRIEVAL_GUARD.md`
4. `package.json`

验证命令：

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/core/config.py`
4. `git diff --check`

Review checklist：

1. `prompt_items` 必须始终为空。
2. `content_answer` 对 visible catalog-only asset 必须返回 `asset_catalog_only`。
3. 缺 `allowed_project_ids` 必须返回 `permission_scope_required`。
4. denied / moved / stale / missing / human-review rows 不得成为 catalog result。
5. 所有 write flags 必须为 false。
6. 不得新增真实 DB / NAS / REST / OpenSearch / Qdrant 代码路径。

若 review / validation 通过，建议做 DB-3A baseline。

下一步 DB-3B 候选：

1. temporary DB backed guard，只读 `external_asset_catalog_contract`。
2. Missing Evidence response DTO。
3. project scope 与 permission scope 组合测试。

DB-3B 仍不得接真实 MySQL；真实数据库接入需要用户单独授权。

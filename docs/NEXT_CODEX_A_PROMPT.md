# NEXT_CODEX_A_PROMPT

当前 DB-3D Temp DB Missing Evidence Response Smoke 已进入本地实现验证阶段，下一步建议 full validation、baseline、测试 agent 独立复测。

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
10. DB-3A catalog retrieval guard 已 baseline：commit `fda6c87`，tag `phase-db3a-catalog-retrieval-guard-baseline`。
11. DB-3B temporary DB backed guard 已 baseline：commit `8fd46a3`，tag `phase-db3b-temp-db-backed-guard-baseline`。
12. DB-3C Missing Evidence response baseline 已完成：commit `dcdb66f`，tag `phase-db3c-missing-evidence-response-baseline`。
13. DB-3C Missing Evidence response review-fix baseline 已完成：commit `84e718a`，tag `phase-db3c-missing-evidence-response-review-fix-baseline`。

当前 DB-3D 允许范围：

1. temporary DB backed guard + Missing Evidence response DTO 组合 smoke。
2. `AssetCatalogMissingEvidenceResponse.from_preview()` 只接收 preview DTO，不接真实 DB。
3. 覆盖 `asset_catalog_only`、`permission_scope_required`、catalog lookup 拒绝包装。
4. 固定空 `prompt_items`、false write flags。

当前 DB-3D 禁止范围：

1. 不写 migration。
2. 不连接真实 MySQL / NAS / REST。
3. 不读真实文件正文。
4. 不写 `documents` / `chunks`。
5. 不写 OpenSearch / Qdrant。
6. 不创建 embedding。
7. 不改 memory kernel 主架构。
8. 不接真实权限系统。

本轮需要 review：

1. `app/services/asset_catalog/response.py`
2. `tests/test_data_steward_asset_catalog_temp_db_missing_evidence_response.py`
3. `docs/DB3D_TEMP_DB_MISSING_EVIDENCE_RESPONSE_SMOKE.md`
4. `package.json`

验证命令：

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/services/asset_catalog/response.py app/core/config.py`
4. `git diff --check`

Review checklist：

1. `from_preview()` 必须只消费 preview DTO，不连接真实 DB。
2. temp DB backed content answer 必须返回 `asset_catalog_only` response。
3. 缺 scope 必须返回 `permission_scope_required` response。
4. `prompt_items` 必须始终为空。
5. 所有 write flags 必须为 false。
6. 不得新增真实 DB / NAS / REST / OpenSearch / Qdrant 代码路径。

若 review / validation 通过，建议做 DB-3D baseline，并请测试 agent 独立复测。

下一步 DB-4A 候选：

1. 真实数据库只读 staging preflight adapter。
2. 只读账号，只读取数据库团队确认的 View / mirror 表。
3. 输出 preview DTO，不写真实 DB、不写 documents/chunks/OpenSearch/Qdrant。

DB-4A 仍需要用户单独授权；production migration / mirror write / NAS scan / indexing 继续后置。

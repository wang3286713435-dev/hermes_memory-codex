# NEXT_CODEX_A_PROMPT

当前 DB-3C Missing Evidence Response DTO 已完成 QA review-fix，下一步建议执行 baseline 后交给测试 agent 独立复测。

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

当前 DB-3C 允许范围：

1. Missing Evidence response DTO。
2. 只包装 guard 的 Missing Evidence decision。
3. 固定 reason、空 `prompt_items`、false write flags。
4. 覆盖 `asset_catalog_only`、`permission_scope_required`、`no_authorized_catalog_metadata`。
5. QA review-fix：拒绝 `None`、空字符串、空白字符串 reason。

当前 DB-3C 禁止范围：

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
2. `tests/test_data_steward_asset_catalog_missing_evidence_response.py`
3. `docs/DB3C_MISSING_EVIDENCE_RESPONSE_DTO.md`
4. `package.json`

验证命令：

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/services/asset_catalog/response.py app/core/config.py`
4. `git diff --check`

Review checklist：

1. DTO 必须拒绝非 Missing Evidence decision。
2. DTO 必须拒绝缺 reason 的 Missing Evidence decision。
3. `to_dict()` 必须输出稳定字段。
4. `prompt_items` 必须始终为空。
5. 所有 write flags 必须为 false。
6. 不得新增真实 DB / NAS / REST / OpenSearch / Qdrant 代码路径。

若 review / validation 通过，建议做 DB-3C review-fix baseline，并请测试 agent 独立复测。

下一步 DB-3D 候选：

1. response DTO 与 temp DB backed guard 组合 smoke。
2. project scope / permission scope response case 扩展。
3. 用户可见 Missing Evidence 文案模板。

DB-3D 仍不得接真实 MySQL；真实数据库接入需要用户单独授权。

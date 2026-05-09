# NEXT_CODEX_A_PROMPT

当前 DB-2 Asset Catalog Mirror dry-run preview、temporary DB proof-of-contract、schema contract freeze、schema review response 均已 baseline。当前新增 DB-2 schema handoff freeze 文档。

已完成 baseline / review 事实：

1. DB-1a fake View fixtures / fake adapter contract tests 已 baseline：commit `e9d1556`，tag `phase-db1a-fake-view-adapter-baseline`。
2. DB-2 planning / Ralph Stop hook guard 已 baseline：commit `56f9e47`，tag `phase-db2-planning-ralph-guard-baseline`。
3. DB-1a contract review-fix 已 baseline：commit `e21a1c9`，tag `phase-db1a-contract-review-fix-baseline`。
4. DB-1a malformed cursor review-fix 已 baseline：commit `e16df1a`，tag `phase-db1a-malformed-cursor-review-fix-baseline`。
5. DB-2 dry-run preview 已 baseline：commit `6780d20`，tag `phase-db2-dry-run-preview-baseline`。
6. DB-2 temporary DB proof-of-contract 已 baseline：commit `53337fe`，tag `phase-db2-temp-db-proof-baseline`。
7. DB-2 schema contract freeze 已 baseline：commit `64e139a`，tag `phase-db2-schema-contract-freeze-baseline`。
8. DB-2 schema review response 已 baseline：commit `cffac1f`，tag `phase-db2-schema-review-response-baseline`。
9. 测试 Codex 已独立复测 dry-run preview 和 temporary DB proof 边界，均无 P0/P1/P2。

当前允许状态：

1. 只允许 DB-2 schema handoff freeze review / validation / baseline。
2. 不写 migration。
3. 不连接真实 MySQL / NAS / REST。
4. 不进入 DB-3 retrieval / selective indexing。

本轮需要阅读：

1. `docs/DB2_SCHEMA_CONTRACT.md`
2. `docs/DB2_VIEW_FIELD_MAPPING.md`
3. `docs/DB2_CHECKPOINT_AND_ROLLBACK_CONTRACT.md`
4. `docs/DB2_PERMISSION_DEFAULTS.md`
5. `docs/DB2_FAKE_FIXTURE_ACCEPTANCE_CASES.md`
6. `docs/DB2_DATABASE_TEAM_HANDOFF.md`
7. `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
8. `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
9. `.claude/ralph/PROMPT.md`

下一步建议：

1. 先做 Codex B review：检查 DB-2 handoff freeze 文档是否覆盖字段合同、View 映射、checkpoint / rollback、权限默认值和 fixture acceptance。
2. 运行验证：
   - `npm test`
   - `npm run lint`
   - `git diff --check`
3. 若无 P0/P1/P2，做 DB-2 schema handoff freeze baseline。
4. Baseline 后，再由用户单独授权是否进入 DB-3。

DB-3 不得自动启动。进入 DB-3 前必须再次确认：

1. DB-2 schema contract 已冻结。
2. View 字段映射已冻结。
3. checkpoint / rollback 合同已冻结。
4. fake fixture 通过。
5. temp DB proof-of-contract 通过。
6. 权限默认 `DENIED` 规则通过测试。
7. catalog-only 不进入 retrieval 通过测试。
8. 数据库 / NAS 团队单独授权真实平台对接。
9. 用户单独授权 DB-3 范围。

禁止：

1. 不自动进入新的功能代码。
2. 不进入 DB-2 migration。
3. 不连接真实 MySQL / NAS / REST。
4. 不扫描 `/Volumes/zyzn/卓羽智能项目`。
5. 不改 retrieval contract。
6. 不改 memory kernel 主架构。
7. 不写 OpenSearch / Qdrant。
8. 不自动 baseline，除非当前 review / validation 通过。

即使用户希望快速进入 DB-3，也必须先完成本轮 DB-2 handoff freeze review / baseline，然后由用户明确授权 DB-3 的第一片范围。

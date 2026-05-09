# NEXT_CODEX_A_PROMPT

当前 DB-2 Asset Catalog Mirror dry-run preview 与 temporary DB proof-of-contract 均已 baseline，当前新增 schema contract freeze。

已完成 baseline / review 事实：

1. DB-1a fake View fixtures / fake adapter contract tests 已 baseline：commit `e9d1556`，tag `phase-db1a-fake-view-adapter-baseline`。
2. DB-2 planning / Ralph Stop hook guard 已 baseline：commit `56f9e47`，tag `phase-db2-planning-ralph-guard-baseline`。
3. DB-1a contract review-fix 已 baseline：commit `e21a1c9`，tag `phase-db1a-contract-review-fix-baseline`。
4. DB-1a malformed cursor review-fix 已 baseline：commit `e16df1a`，tag `phase-db1a-malformed-cursor-review-fix-baseline`。
5. DB-2 dry-run preview 已 baseline：commit `6780d20`，tag `phase-db2-dry-run-preview-baseline`。
6. DB-2 temporary DB proof-of-contract 已 baseline：commit `53337fe`，tag `phase-db2-temp-db-proof-baseline`。
7. 测试 Codex 已独立复测 dry-run preview 和 temporary DB proof 边界，均无 P0/P1/P2。

当前允许状态：

1. DB-2 仅允许 docs-only schema contract freeze。
2. 不写 migration，不连接真实 MySQL / NAS / REST，不进入 DB-3 retrieval。

1. 阅读：
   - `docs/DB2_SCHEMA_CONTRACT.md`
   - `docs/DB2_ASSET_CATALOG_MIRROR_PLAN.md`
   - `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
   - `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
   - `.claude/ralph/PROMPT.md`
2. 如用户授权下一片 DB-2，先再次确认 DB-2 plan 是否仍保持：
   - no migration unless explicitly authorized
   - no real MySQL / NAS / REST
   - no `documents` / `chunks`
   - no OpenSearch / Qdrant
   - no catalog retrieval
   - no retrieval contract or memory kernel architecture change
3. schema contract freeze 后，下一步只可在新授权下选择其中一个：
   - database team / platform team review response
   - migration authorization decision document
   - mirror field DTO refinement without migration

禁止：

1. 不自动进入新的功能代码。
2. 不进入 DB-2 migration。
3. 不连接真实 MySQL / NAS / REST。
4. 不扫描 `/Volumes/zyzn/卓羽智能项目`。
5. 不改 retrieval contract。
6. 不改 memory kernel 主架构。
7. 不自动 baseline。

即使 DB-2 dry-run preview baseline 已完成，仍需用户显式授权才可进入下一片 DB-2。

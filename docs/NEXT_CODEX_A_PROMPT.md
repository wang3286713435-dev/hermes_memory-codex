# NEXT_CODEX_A_PROMPT

当前 DB-1a fake View fixtures / fake adapter contract tests 已 baseline。

baseline:

1. commit：`e9d1556`
2. tag：`phase-db1a-fake-view-adapter-baseline`

DB-2 Asset Catalog Mirror planning 与 Ralph Stop hook guard 已通过 Codex B review，并进入 baseline。

本 baseline 后，下一轮只允许在用户显式授权时进入一个极窄 DB-2 implementation slice；未授权前继续停在 planning / review 状态。

1. 阅读：
   - `docs/DB2_ASSET_CATALOG_MIRROR_PLAN.md`
   - `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
   - `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
   - `docs/DB2_ASSET_CATALOG_MIRROR_PLANNING_PROMPT.md`
   - `.claude/ralph/PROMPT.md`
2. 如用户授权 implementation，先再次确认 DB-2 plan 是否仍保持：
   - docs-only
   - no migration unless explicitly authorized
   - no real MySQL / NAS / REST
   - no `documents` / `chunks`
   - no OpenSearch / Qdrant
   - no catalog retrieval
   - no retrieval contract or memory kernel architecture change
3. 下一步 implementation slice 如被授权，建议只做其中一个：
   - dry-run sync preview contract tests
   - temporary DB / fixture DB proof-of-contract tests
   - mirror field dataclass / DTO draft without migration
4. Review DB-2 plan 是否明确：
   - proposed mirror fields
   - sync preview contract
   - checkpoint policy
   - permission / evidence boundary
   - testing plan
   - implementation gate
   - hard stop conditions
   - future implementation prompt remains unauthorized

禁止：

1. 不写功能代码。
2. 不进入 DB-2 implementation。
3. 不连接真实 MySQL / NAS / REST。
4. 不扫描 `/Volumes/zyzn/卓羽智能项目`。
5. 不改 retrieval contract。
6. 不改 memory kernel 主架构。
7. 不自动 baseline。

即使 baseline 已完成，仍需用户显式授权才可进入 DB-2 implementation。

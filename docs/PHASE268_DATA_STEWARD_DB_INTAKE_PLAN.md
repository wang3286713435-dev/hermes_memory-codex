# Phase 2.68 Data Steward DB Branch Intake / Merge Readiness Plan

日期：2026-05-11
状态：Codex A intake review completed

## 0. 2026-05-11 接收评审结果

结论：`ready_for_mainline_acceptance`。

本轮只做只读接收评审，未连接真实 MySQL，未扫描 NAS，未启用 Data Steward runtime flags，未写 migration / `documents` / `chunks` / OpenSearch / Qdrant，未执行真实 DB smoke。

复核结果：

1. DB 支线目录 `/Users/Weishengsu/Hermes_memory_db0` 当前位于 branch `codex/data-steward-db0-contract`，HEAD `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
2. DB 支线仍存在 12 个未跟踪 QA probe 文件，但未被纳入 tracked baseline；主线接收时不得 raw merge 这些 probe。
3. 主线已包含 `app/services/asset_catalog/**`、Data Steward 目标测试与默认关闭的 feature flags。
4. `platform_asset_*` 与 readonly smoke flags 默认均为 `false`，readonly DB password 默认 `None`。
5. catalog-only 预览与 retrieval guard 不写 `documents` / `chunks` / OpenSearch / Qdrant。
6. Missing Evidence 支持 `asset_catalog_only` 与 `permission_scope_required`。
7. `permission_tags` / `project_scope` 缺失路径保持 fail-closed / deny。
8. fake adapter、temporary mirror proof、readonly connector shell 与真实 DB live smoke gate 分层清楚；当前未发现真实 DB secret、真实样本、真实 NAS scan output 或 QA probe 被纳入主线 tracked 文件。
9. 目标验证通过：`uv run pytest tests/test_data_steward_*.py -q` 为 `71 passed`；MVP runner regression target 为 `32 passed`；`git diff --check` 通过。

Go / Pause / No-Go：`Go`。建议下一阶段仅规划测试机真实 DB `structure_only` smoke；仍不授权 `LIMIT 30` 脱敏样本、mirror migration、DB CRUD、NAS scan、selective indexing 或 production rollout。

## 1. 定位

Phase 2.68 的目标是把已完成的 Data Steward DB 支线纳入主线接收评审，而不是立即连接真实数据库、扫描 NAS 或实现 Agent 直接增删改查。

当前判断：

1. 内部受控 MVP 已可在 Mac mini 上继续试用。
2. Data Steward / DB / NAS 是 Hermes 企业 Agent 的后续核心能力之一。
3. DB 支线已经完成 DB-0 到 DB-4D 的 contract、fake adapter、readonly connector shell、脱敏 smoke interface 与 closeout 文档。
4. 下一步应先做 merge readiness review，确认支线是否能无损进入主线。

## 2. 目标

Phase 2.68 只做接收评审与下一阶段计划：

1. 复核 DB 支线 closeout baseline：
   - branch：`codex/data-steward-db0-contract`
   - commit：`a272081`
   - tag：`phase-db-branch-closeout-merge-readiness-baseline`
2. 复核主线已选择性接入的 Data Steward 代码和默认关闭 feature flags。
3. 对照 `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md` 与 DB 支线 closeout 文档，确认合回主线后不会污染现有 retrieval / ingestion / evidence contract。
4. 输出 Codex B review 结论：
   - `ready_for_mainline_acceptance`
   - `needs_more_review`
   - `blocked`
5. 如果通过，下一阶段才允许规划测试机真实 DB `structure_only` smoke。

## 3. 当前不做

本阶段禁止：

1. 连接真实 MySQL。
2. 扫描真实 NAS。
3. 写 migration。
4. 写 `documents` / `chunks`。
5. 写 OpenSearch / Qdrant / MinIO。
6. 启用 Data Steward runtime feature flags。
7. 执行真实 retrieval / indexing。
8. 实现 DB CRUD。
9. 让 Agent 直接修改平台数据库或 NAS。
10. 进入 production rollout。

## 4. 接收评审清单

Codex A 执行 Phase 2.68 时应只做只读检查：

1. 检查主线 Git 状态，确认不会 stage 历史无关 dirty。
2. 读取并核对：
   - `docs/DB_NAS_HERMES_INTEGRATION_CONTRACT.md`
   - `docs/DB_BRANCH_CLOSEOUT_AND_MERGE_READINESS.md`
   - `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
   - `docs/DATA_STEWARD_BRANCH_ROADMAP.md`
   - `docs/TECHNICAL_DESIGN.md`
   - `docs/ACTIVE_PHASE.md`
   - `docs/PHASE_BACKLOG.md`
   - `docs/NEXT_CODEX_A_PROMPT.md`
3. 检查 `app/services/asset_catalog/**` 是否保持 catalog-only / readonly 语义。
4. 检查 config feature flags 是否默认关闭。
5. 检查 tests 是否覆盖：
   - fake adapter contract
   - permission missing deny
   - asset catalog only Missing Evidence
   - readonly preflight / smoke shell
6. 可运行目标测试，但不得连接真实 DB 或 NAS。

## 5. 未来真实数据库接入路线

如果 Phase 2.68 review 通过，后续路线应为：

1. Phase 2.69：测试机真实 DB `structure_only` smoke。
   - 只验证 View / REST contract 字段存在、类型、权限失败语义。
   - 不读取真实业务内容。
   - 不输出真实项目名、文件名、路径或 raw rows。
2. Phase 2.70：测试机真实 DB `LIMIT 30` 脱敏 smoke。
   - 只输出脱敏统计与字段覆盖。
   - 仍不写 mirror，不写 `documents/chunks`，不写 index。
3. Phase 2.71：asset catalog mirror planning。
   - 规划 `external_asset_catalog` / checkpoint / rollback。
   - migration 必须单独授权。
4. Phase 2.72+：catalog retrieval / selective indexing / operation plan。
   - 写操作必须通过平台 API、审批、审计与 operation plan。
   - Agent 不直接改 MySQL 或 NAS。

## 6. 数据库团队配合点

当前 Phase 2.68 不需要数据库团队提供密钥或真实连接信息。

进入 Phase 2.69 前，需要用户协调数据库团队确认：

1. 测试机 Hermes Memory 访问数据库的网络路径。
2. 只读账号或 REST API key 的安全传递方式。
3. 四个 View / REST contract 是否仍为 `delivery_platform.asset_views.v1`。
4. 是否允许 `structure_only` 检查。
5. 是否允许后续 `LIMIT 30` 脱敏 smoke。
6. 禁止输出真实项目名、文件名、NAS 路径、raw row、stderr 或 secret。

## 7. Go / Pause / No-Go

Go 条件：

1. DB 支线 closeout 文档齐全。
2. 主线 Data Steward feature flags 默认关闭。
3. catalog-only 不进入 existing document evidence。
4. permission 缺失默认 deny。
5. 目标测试可离线通过。
6. 无真实 DB / NAS / index 写入。

Pause 条件：

1. 支线或主线 Git 状态不清。
2. QA probe / secret / 真实样本疑似混入。
3. feature flag 默认开启。
4. 发现 catalog-only 资产可进入正文 answer evidence。

No-Go 条件：

1. 需要连接真实 DB 才能继续。
2. 需要扫描 NAS 才能继续。
3. 需要写 migration / index / documents / chunks 才能继续。
4. 发现会破坏现有 retrieval contract 或 memory kernel 主架构的改动。

## 8. 结论

Phase 2.68 是主线接收 Data Steward DB 支线的安全门，不是 DB CRUD 实现阶段。

本阶段通过后，才能把测试机真实数据库对接推进到 `structure_only` smoke。任何增删改查能力必须后置为 operation plan / approval / audit，而不是让 Agent 直接操作平台数据库。

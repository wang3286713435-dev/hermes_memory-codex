# Active Phase

- 当前 phase：DB Branch Closeout / Merge Readiness
- 当前分支：`codex/data-steward-db0-contract`
- 当前 baseline：
  - DB-4C readonly live smoke runner baseline：commit `444e562`，tag `phase-db4c-readonly-live-smoke-runner-baseline`
  - DB-4B readonly connector shell baseline：commit `afadb8d`，tag `phase-db4b-readonly-connector-shell-baseline`
  - DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`
  - DB-3D Temp DB Missing Evidence response baseline：commit `54fd3d0`，tag `phase-db3d-temp-db-missing-evidence-response-baseline`
- 本轮授权：DB-4D QA 无 open finding 后，进入 DB 支线 closeout / merge readiness。
- 本轮目标：停止扩功能，新增最终 closeout 文档，明确已完成范围、未做范围、合回条件和测试机后续真实 DB smoke 门槛。

## 本轮修改文件

1. `/Users/Weishengsu/Hermes_memory_db0/docs/DB_BRANCH_CLOSEOUT_AND_MERGE_READINESS.md`
2. `/Users/Weishengsu/Hermes_memory_db0/docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
3. phase handoff docs

## 完成内容

1. 明确 DB-0 到 DB-4D 已完成范围。
2. 明确 DB-5 / DB-6 后置，不在当前分支继续扩大。
3. 明确真实 DB smoke 等 Hermes Memory 安装到测试机后再执行。
4. 明确合回主线条件。
5. 明确 feature flags 默认安全态。
6. 明确临时 QA probe 不纳入提交。

## 当前验证状态

1. DB-4D QA：0 open findings，P0=0。
2. `npm test`：`71 passed`。
3. `npm run lint`：`All checks passed!`。
4. py_compile：passed。
5. `git diff --check`：passed。

## 当前结论

DB 支线不建议继续扩功能。下一步是 closeout validation、baseline，然后由用户选择合回主线 / 创建 PR / 保留分支。

## 继续禁止

1. 不自动连接真实 MySQL；仅在测试机上显式运行 DB-4D local smoke 命令时连接同机容器。
2. 不持久化真实样本。
3. 不使用应用主账号。
4. 不创建 production migration。
5. 不写 `external_asset_catalog`。
6. 不扫描真实 NAS。
7. 不读取真实文件正文。
8. 不触发真实 REST 动作。
9. 不写 `documents` / `chunks`。
10. 不写 OpenSearch / Qdrant。
11. 不进入真实 retrieval/indexing。

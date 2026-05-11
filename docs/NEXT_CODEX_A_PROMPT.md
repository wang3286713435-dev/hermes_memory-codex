# NEXT_CODEX_A_PROMPT

当前 DB-4D 已通过独立 QA，DB 支线进入 closeout / merge readiness。下一步建议只做 closeout validation 和 baseline，不再扩大 DB 功能。

## 已完成 baseline / review 事实

1. DB-4A readonly DB preflight skeleton baseline：commit `053affa`，tag `phase-db4a-readonly-db-preflight-skeleton-baseline`。
2. DB-4B readonly connector shell baseline：commit `afadb8d`，tag `phase-db4b-readonly-connector-shell-baseline`。
3. DB-4C readonly live smoke runner baseline：commit `444e562`，tag `phase-db4c-readonly-live-smoke-runner-baseline`。

## 当前 DB-4D 允许范围

1. 测试机同机 `delivery-mysql` / `hermes_agent_ro` 只读 smoke 接口。
2. `structure_only` 和显式授权 `LIMIT 30`。
3. 测试机同机 dev 授权门禁：`same_machine_local_dev_authorized=true`。
4. 真实 rows 只进入 DB-4A preflight validator。
5. 输出只允许脱敏 JSON summary。
6. 业务底表只允许做拒绝访问验证。

## 当前 closeout 允许范围

1. 新增 / 更新 closeout 文档。
2. 汇总 DB-0 到 DB-4D baseline。
3. 明确合回主线条件。
4. 明确测试机真实 DB smoke 后置门槛。

## 当前 DB-4D 禁止范围

1. 不使用应用主账号或 root 账号作为企业 Agent 连接账号。
2. 不输出项目名、文件名、NAS 路径、source id、asset uid、raw row、stderr 或密码。
3. 不写 migration。
4. 不写 `external_asset_catalog`。
5. 不扫描真实 NAS。
6. 不读取真实文件正文。
7. 不触发真实 REST。
8. 不写 `documents` / `chunks`。
9. 不写 OpenSearch / Qdrant。
10. 不创建 embedding。
11. 不进入真实 retrieval/indexing。

## 本轮需要 review

1. `docs/DB_BRANCH_CLOSEOUT_AND_MERGE_READINESS.md`
2. `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`
3. phase handoff docs

## 验证命令

1. `npm test`
2. `npm run lint`
3. `uv run python -m py_compile app/services/asset_catalog/contracts.py app/services/asset_catalog/fake_adapter.py app/services/asset_catalog/mirror_preview.py app/services/asset_catalog/temp_db.py app/services/asset_catalog/retrieval_guard.py app/services/asset_catalog/response.py app/services/asset_catalog/readonly_preflight.py app/services/asset_catalog/readonly_connector.py app/services/asset_catalog/readonly_live_smoke.py app/services/asset_catalog/readonly_local_live_smoke.py app/core/config.py`
4. `git diff --check`

## Review checklist

1. Docker command 不得把密码放入 argv。
2. 输出不得包含 raw rows、项目名、文件名、NAS 路径、source id、asset uid、stderr 或密码。
3. `limit` 模式必须要求显式真实样本授权，并要求主线更新或同机本地 dev 授权。
4. rows 只进入 DB-4A preflight，不进入 prompt / retrieval / indexing。
5. 业务底表 probe 只报告 denied/readable，不输出原始错误。
6. 不得出现 DML / DDL / NAS / REST / documents/chunks / OpenSearch/Qdrant 写入路径。

## 下一步候选

closeout baseline 后，由用户选择合回主线、创建 PR 或保留分支。真实 DB smoke 等 Hermes Memory 安装到测试机并拿到测试机连接信息后再执行；真实 migration、mirror 写入、NAS、OpenSearch/Qdrant、documents/chunks、真实 retrieval/indexing 仍需单独授权。

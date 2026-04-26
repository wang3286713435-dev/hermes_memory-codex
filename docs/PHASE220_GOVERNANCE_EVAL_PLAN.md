# Phase 2.20 治理类 Eval 扩展规划

## 1. 阶段目标

Phase 2.20 目标是把 Phase 2.18a、Phase 2.19a、Phase 2.19b 已完成的治理能力纳入可重复回归评测。

本阶段只做边界规划，不写功能代码，不改 retrieval contract，不改 memory kernel 主架构，不进入 rollout。

## 2. 当前输入

已具备的治理能力：

1. Phase 2.18a：access / audit 最小闭环，支持 `not_configured_allow`、`allow`、`deny`、`denied_document_ids` 与 audit log。
2. Phase 2.19a：version governance 最小闭环，默认 latest 检索、显式历史 `version_id` 查询、`stale_version` 与 `latest_version_id` trace。
3. Phase 2.19b：Hermes session alias stale version 联调，alias 指向旧版本时可在用户侧 trace / context 中暴露 stale 诊断。
4. Phase 2.14：API deterministic eval runner 已可复用，适合作为治理类 API 评测入口。
5. Phase 2.14b：Hermes CLI smoke 已可覆盖 session-layer 状态能力。

## 3. Eval 覆盖范围

### 3.1 Access Policy

API deterministic eval 应覆盖：

1. 无 ACL：`policy_decision=not_configured_allow`。
2. requester 命中：`policy_decision=allow`。
3. role 命中：`policy_decision=allow`。
4. tenant mismatch：`policy_decision=deny`。
5. deny 后 `returned_document_ids` 不含被拒 document。
6. deny 后 evidence / citation 不泄露被拒 document chunk。

### 3.2 Audit Log

API deterministic eval 应覆盖：

1. audit event 成功写入。
2. audit event 包含 `requester_id` / `tenant_id`。
3. audit event 包含 `returned_document_ids`。
4. audit event 包含 `evidence_chunk_ids`。
5. audit event 包含 `version_ids` / `evidence_version_ids`。
6. audit 写入失败仍不阻断 retrieval 的 fail-open 行为可作为独立单测，不强行纳入 live eval。

### 3.3 Version Governance

API deterministic eval 应覆盖：

1. 默认 latest 查询不返回 superseded version。
2. sparse / dense / hybrid 路径均不泄露旧版本。
3. 显式旧 `version_id` 可查历史版本。
4. 显式旧版本查询 trace 包含 `stale_version=true`。
5. trace 包含 `latest_version_id`。
6. audit 默认 latest 只记录 latest `evidence_version_ids`。

### 3.4 Alias Stale Version

Hermes CLI smoke 应覆盖：

1. 在同一 Hermes session 中绑定 `@版本测试` 到 v1。
2. 上传或准备 v2 后继续使用 `@版本测试`。
3. retrieval 仍按 alias 绑定的旧 `version_id` 查历史 evidence。
4. CLI trace / context 暴露 `alias_stale_version=true`。
5. CLI trace / context 暴露 `latest_version_id=<v2>`。
6. compare mode 中一侧 alias stale 时，stale 诊断仍可见，且不得混入第三文档。

## 4. API 与 CLI 划分

### 4.1 API deterministic eval

优先纳入：

1. access policy：no ACL / allow / deny。
2. audit log：event 写入与关键字段。
3. version filtering：默认 latest 与显式历史版本。
4. deny 不泄露 evidence。
5. audit `evidence_version_ids`。

原因：

1. 这些能力在 Hermes_memory 内完成，状态可控。
2. 可直接断言 trace、results、audit row 与 version metadata。
3. 不依赖 LLM 表述，适合 CI / 本地重复执行。

### 4.2 Hermes CLI smoke

优先纳入：

1. alias stale version 用户侧诊断。
2. compare mode 中 stale alias trace。

原因：

1. alias 是 Hermes session layer 能力，不属于 Hermes_memory stateless retrieval。
2. 需要验证 `session_id`、alias store、context block 与用户可见 trace。
3. 不适合强行塞进 API eval。

## 5. 指标设计

每条治理类 eval case 至少输出：

1. `case_id`
2. `pass/fail/skipped`
3. `policy_decision`
4. `denied_document_ids`
5. `audit_event_written`
6. `requester_id`
7. `returned_document_ids`
8. `evidence_chunk_ids`
9. `evidence_version_ids`
10. `stale_version`
11. `latest_version_id`
12. `contamination_flags`
13. `latency_ms`

失败诊断字段至少包括：

1. `unexpected_document_ids`
2. `missing_denied_document_ids`
3. `missing_audit_fields`
4. `missing_evidence_version_ids`
5. `missing_stale_trace`
6. `policy_decision_mismatch`

## 6. 最小实现建议

Phase 2.20a 建议分两步：

1. 扩展 `scripts/phase214_regression_eval.py`，新增 governance case group。
2. 在 Hermes 主仓库补少量 CLI smoke，覆盖 alias stale version session flow。

API eval 最小 case 建议：

1. `access_no_acl_not_configured_allow`
2. `access_requester_allow`
3. `access_tenant_mismatch_deny`
4. `access_deny_no_evidence_leak`
5. `audit_event_written_with_evidence`
6. `version_default_latest_only`
7. `version_explicit_old_version`
8. `version_stale_trace_latest_version_id`
9. `audit_evidence_version_ids`

CLI smoke 最小 case 建议：

1. `alias_stale_version_warning`
2. `compare_one_stale_alias`

## 7. 数据准备

API eval 可使用小型 fixture 文档，不默认污染真实标书池：

1. access / audit：使用最小测试文档并显式设置 ACL metadata。
2. version：使用小型 v1 / v2 文档。
3. alias stale：沿用 Phase 2.19b 的小型 v1 / v2 smoke 文档或重新创建隔离样本。

真实大文件池只作为后续扩展，不作为 Phase 2.20a 最小必需条件。

## 8. 非目标

Phase 2.20 不做：

1. 完整 RBAC / ABAC。
2. 企业 IAM / SSO。
3. 复杂版本 diff。
4. facts。
5. rollout。
6. retrieval contract 重构。
7. memory kernel 主架构重构。
8. rerank 策略调整。

## 9. 规划结论

建议开始 Phase 2.20a 最小实现。

优先把 access / audit / version filtering 纳入 Hermes_memory API deterministic eval；alias stale version 保持 Hermes CLI smoke。这样可以把已完成的治理能力纳入稳定回归，同时避免把 session-layer 状态硬塞进 stateless retrieval eval。

## 10. Phase 2.20a 最小实现结果

已完成：

1. 扩展 `scripts/phase214_regression_eval.py`，新增 `governance` case group。
2. 新增可控 Phase 2.20 fixture 文档，不触碰 6 文件真实池。
3. eval summary 增加 `groups` 统计。
4. 每个 case 输出 `policy_decision`、`denied_document_ids`、`audit_event_written`、`evidence_version_ids`、`stale_version`、`latest_version_id` 与 `returned_document_ids`。
5. 新增 `--group governance` 入口，可单独运行治理类 API eval。

治理类 API eval 覆盖：

1. `gov_access_no_acl_not_configured_allow`
2. `gov_access_requester_allow`
3. `gov_access_tenant_mismatch_deny`
4. `gov_version_default_latest_only`
5. `gov_version_explicit_old_version`

本地 live 结果：

1. `governance` group：`5 passed / 0 failed / 0 skipped`
2. latency `p50/p95 = 12.895 ms / 49.990 ms`
3. deny case 返回空 results，且 `denied_document_ids` 正确。
4. explicit old version case 返回旧 version，且 `stale_version=true`、`latest_version_id=phase220-gov-version-v2`。
5. audit event 均写入，并包含 requester / document_ids / chunk_ids / evidence_version_ids。

Hermes CLI smoke 扩展：

1. 主仓库 `phase214b_cli_smoke_eval.py` 新增 `alias_stale_version_warning`。
2. stale alias 通过 session state bootstrap 绑定旧 version。
3. live runner：`5 passed / 0 failed / 0 skipped`
4. stale alias case 输出旧 version evidence、`alias_stale_version=true` 与 `latest_version_id`。

收口验证结果：

1. `governance` group：`5 passed / 0 failed / 0 skipped`
2. Hermes CLI smoke：`5 passed / 0 failed / 0 skipped`
3. full Phase 2.14 eval：`16 passed / 0 failed / 1 skipped`
4. full eval latency：`p50/p95 = 11.146 ms / 539.376 ms`

环境注意事项：

1. 本地 / CI 执行 dense / hybrid eval 时，`QDRANT_COLLECTION` 必须指向 `hermes_chunks`。
2. 若本机 ignored `.env` 指向旧 `hermes_gate_chunks`，会造成 core dense 用例 `dense_returned=0` 的假失败。
3. 本轮已确认该问题不是代码回归、不是 Qdrant 数据缺失，也不需要回填或放宽 eval 断言。

限制与尾项：

1. alias stale version 仍只适合 CLI smoke，不纳入 Hermes_memory stateless API eval。
2. `missing_alias_suppress_cli_only` 保持 skipped，由 Hermes CLI smoke 覆盖。
3. Phase 2.20a 不评估完整 RBAC / ABAC、不做复杂版本 diff、不进入 rollout。

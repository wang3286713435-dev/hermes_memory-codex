# Phase 2.18 权限 / 审计 / facts / 增量更新 / 音频 ASR 路线裁决与最小闭环

## 1. 阶段目标

Phase 2.18 先完成下一阶段路线裁决，并在 Phase 2.18a 做权限与审计最小闭环。

本阶段不改 retrieval contract，不改 memory kernel 主架构，不进入 rollout。

## 2. 当前状态

Phase 2.10-2.17 已完成：

1. 文件作用域与上下文治理。
2. file alias。
3. tender metadata snapshot。
4. Excel / PPTX ingestion。
5. meeting transcript ingestion。
6. dense ingestion 与显式文件池 backfill。
7. rerank smoke。
8. API deterministic eval 与 CLI smoke。

当前 PRD 核心缺口仍集中在：

1. 权限治理。
2. 审计日志闭环。
3. 结构化 facts。
4. 增量更新 / 版本治理。
5. 原始音频 ASR。
6. 更大规模质量评测与 rollout 准入。

## 3. 候选方向评审

### A. 权限与审计最小闭环

企业落地价值：最高。企业真实使用前必须能证明“谁查了什么、返回了哪些 evidence、是否经过权限判断”。

技术风险：中等。可先做 placeholder 与审计事件，不需要一次性实现完整 RBAC / ABAC。

当前依赖：已具备。retrieval trace、document_id、chunk_id、citation、eval runner 已成熟，可以承载最小审计。

是否放大风险：较低。若严格限定为 trace / audit log / placeholder，不会扩大检索策略风险。

是否适合下一阶段：适合。

### B. 结构化 facts

企业落地价值：高。facts 是从检索助手走向企业长期记忆系统的关键。

技术风险：高。需要 schema、来源追溯、人工确认、版本更新、冲突处理和权限联动。

当前依赖：部分具备。metadata snapshot、meeting transcript 抽取和 citations 已有，但人工确认与事实生命周期尚未建立。

是否放大风险：较高。过早做 facts 可能把未经确认的抽取误当事实。

是否适合下一阶段：暂不优先，建议在权限 / 审计底座后推进。

### C. 增量更新 / 文档版本治理

企业落地价值：高。真实文档会频繁更新，旧 chunk 下线、版本差异和索引重建是长期必要能力。

技术风险：中高。涉及 PostgreSQL、OpenSearch、Qdrant 三套索引一致性。

当前依赖：部分具备。document_versions、chunks、dense metadata 已存在，但更新策略与旧版本下线仍不足。

是否放大风险：中等。若没有审计与权限，版本治理问题较难追溯。

是否适合下一阶段：适合排在权限 / 审计之后。

### D. 原始音频 ASR

企业落地价值：中高。会议音频是企业记忆的重要入口。

技术风险：高。涉及 ASR provider、说话人识别、时间戳、敏感音频权限与人工确认。

当前依赖：部分具备。会议纪要 / 转写文本 ingestion 已完成，但原始音频权限和审计缺口明显。

是否放大风险：高。音频内容更敏感，缺权限审计时不宜扩大入口。

是否适合下一阶段：不适合，建议后置。

### E. 专用 ALIYUN_RERANK_API_KEY smoke / rerank 质量评测

企业落地价值：中等。可补齐 rerank provider 专用 key 与排序收益评估。

技术风险：低到中。smoke 风险低，质量评测需要标注样本。

当前依赖：已具备。Phase 2.17 已有 runner。

是否放大风险：低。

是否适合下一阶段：适合作为尾项或质量评测阶段，不应优先于权限 / 审计。

## 4. 推荐路线

推荐下一阶段进入：

**Phase 2.18a：权限与审计最小闭环。**

理由：

1. PRD 与 Roadmap 均将 permission control、audit log 列为企业落地硬门槛。
2. 当前文档、上下文、多模态、dense、rerank、eval 已形成可用底座，下一步应补治理能力。
3. facts、版本治理、音频 ASR 都需要依赖权限与审计，否则会放大敏感数据和事实可信度风险。
4. 最小权限 / 审计可以先做 placeholder 与 trace，不需要一次性大改权限系统。

## 5. Phase 2.18a 最小边界

### 5.1 request / user identity placeholder

最小字段：

1. `requester_id`
2. `requester_role`
3. `department_id`
4. `project_ids`
5. `permission_tags`

当前只作为 request context / trace / audit 输入，不接完整企业 IAM。

### 5.2 document ACL metadata placeholder

最小字段：

1. `visibility`
2. `allowed_users`
3. `allowed_roles`
4. `allowed_departments`
5. `allowed_projects`
6. `confidentiality_level`
7. `permission_tags`

当前先作为 metadata placeholder 与 policy input，不要求已有文档全部补齐真实 ACL。

### 5.3 retrieval trace 增强

trace 至少记录：

1. `requester_id`
2. `requester_role`
3. `access_policy_mode`
4. `access_policy_decision`
5. `applied_filters`
6. `returned_document_ids`
7. `evidence_chunk_ids`
8. `denied_document_ids`
9. `permission_trace_missing`

### 5.4 audit log 最小事件

最小事件字段：

1. `event_id`
2. `timestamp`
3. `event_type=query`
4. `requester_id`
5. `query_hash`
6. `filters`
7. `returned_document_ids`
8. `evidence_chunk_ids`
9. `policy_decision`
10. `policy_reason`
11. `latency_ms`
12. `trace_id`

### 5.5 最小策略

1. `audit_only`：只记录，不拒绝；适合初期上线观察。
2. `deny_if_explicit_acl_mismatch`：仅当文档有明确 ACL 且 requester 不匹配时拒绝。
3. 缺失 ACL 默认不做强拒绝，但 trace 标记 `permission_trace_missing=true`。

### 5.6 最小评测

至少覆盖：

1. 无 requester 时 trace 可诊断。
2. requester 有权访问文档时返回 evidence。
3. requester 与明确 ACL 不匹配时不返回该文档。
4. audit log 记录 query / document_ids / chunk_ids / policy decision。
5. denied document 不进入 results / citations / prompt context。

## 6. 非目标

1. 不做完整 RBAC。
2. 不做完整 ABAC。
3. 不接企业 IAM / SSO。
4. 不做管理后台。
5. 不做权限配置 UI。
6. 不做 facts 主线开发。
7. 不做原始音频 ASR。
8. 不做生产级 rollout。
9. 不改 retrieval contract。
10. 不改 memory kernel 主架构。

## 7. 当前结论

Phase 2.18a 最小实现已完成。

已完成：

1. request/user identity placeholder：支持 request body `user_id`、filter metadata 与 API header `X-Requester-Id` / `X-Tenant-Id` / `X-Requester-Role`。
2. document ACL metadata placeholder：支持 `Document.metadata_json.allowed_requester_ids`、`allowed_roles`、`tenant_id`。
3. retrieval policy decision：支持 `allow`、`deny`、`not_configured_allow`；无 ACL 默认 allow，但 trace 标记。
4. deny 后过滤对应 document evidence，不进入 results / citations / prompt context。
5. audit log：复用现有 `audit_logs` 表，写入 query、filters、returned_document_ids、evidence_chunk_ids、policy_decision、denied_document_ids 与 trace_id。
6. audit 写入失败 fail-open，不阻断 retrieval。

测试已覆盖：

1. 无 ACL 本地默认 allow 且 trace 标明 `not_configured_allow`。
2. `allowed_requester_ids` 命中 allow。
3. `allowed_roles` 命中 allow。
4. tenant mismatch deny。
5. deny 后 results 不含被拒 document。
6. audit event 字段完整。
7. audit 写入失败不阻断 retrieval。

真实 API live smoke 已完成：

1. `/health` 返回 OK。
2. 测试文档：`402657e8-2ea8-48b7-8266-85aab45bbc41`（硬件清单）。
3. 默认无 ACL 查询通过：`policy_decision=not_configured_allow`，results 正常返回。
4. requester allow 查询通过：`policy_decision=allow`，audit 记录 `requester_id=smoke-user`。
5. tenant mismatch deny 查询通过：`policy_decision=deny`，results 不含该 document，`denied_document_ids` 包含目标 document_id。
6. `audit_logs` 三条均写入成功。
7. 测试后文档 `metadata_json` 已恢复为 `{"content_type": "application/octet-stream"}`。

当前仍不建议下一阶段直接进入 facts、增量更新、音频 ASR 或生产级 rollout；Phase 2.18a 已具备 Git baseline 条件。

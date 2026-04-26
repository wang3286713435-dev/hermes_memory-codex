# Phase 2.19 增量更新 / 文档版本治理 / facts 顺序裁决

## 1. 阶段目标

Phase 2.19 只做下一阶段路线裁决与边界规划。

本阶段不写功能代码，不改 retrieval contract，不改 memory kernel 主架构，不进入 rollout。

## 2. 当前状态

Phase 2.18a 已完成权限与审计最小闭环 baseline：

1. commit：`6d9de38`
2. tag：`phase-2.18a-access-audit-baseline`
3. 当前仍是 soft policy placeholder，不是完整 RBAC / ABAC。

当前已有真实文件池包含多份同类或近似文档：

1. 多份大型标书。
2. 两份数字化交付标准。
3. 答疑补遗文件。
4. Excel / PPTX 样本。
5. 会议纪要。

若不先治理版本与旧文档失效，后续 facts 可能建立在过期来源上。

## 3. 候选方向评审

### A. 增量更新 / 文档版本治理

企业落地价值：最高。真实企业文件会反复更新、替换、补遗、改名和重传；latest / historical / superseded 不清楚会直接污染检索和引用。

技术风险：中等。已有 `documents`、`document_versions`、`chunks`、`is_latest`、`status`、`content_hash`、`file_hash` 基础字段，可以做最小闭环。

当前依赖：已具备。dense/sparse ingestion、audit、document scope、alias、eval 都已能承接版本治理。

是否放大现有风险：较低。若严格限定为同名 / 近似名版本识别、latest 标记、superseded 下线和默认 latest 检索，不会大改主链路。

是否适合下一阶段：适合，推荐优先。

### B. 结构化 facts

企业落地价值：高。facts 是企业长期记忆系统的关键层。

技术风险：高。需要事实 schema、来源版本、人工确认、冲突处理、失效策略和权限联动。

当前依赖：部分具备。metadata snapshot、meeting transcript 与 citation 已有，但版本稳定性不足。

是否放大现有风险：高。若 facts 基于过期文件或旧 chunk，会形成难以纠偏的错误事实。

是否适合下一阶段：不建议优先，应排在版本治理之后。

### C. 审计 eval 纳入 Phase 2.14

企业落地价值：中高。可把 Phase 2.18a soft policy 与 audit 写入纳入回归。

技术风险：低。已有 API eval runner，可扩展 policy_decision / denied_document_ids / audit event 检查。

当前依赖：已具备。

是否放大现有风险：低。

是否适合下一阶段：适合作为 Phase 2.19 的配套尾项或后续小阶段，不应压过版本治理。

### D. 完整 RBAC / ABAC

企业落地价值：高。

技术风险：高。需要 IAM / SSO、组织架构、项目授权、文档密级、管理后台和策略配置。

当前依赖：部分具备。Phase 2.18a 只是 placeholder soft policy。

是否放大现有风险：高。过早做完整权限会把当前本地/单机验证复杂化。

是否适合下一阶段：不适合，建议在版本治理和 audit eval 后推进。

### E. 原始音频 ASR

企业落地价值：中高。会议音频是重要入口。

技术风险：高。音频更敏感，且需要 ASR provider、speaker diarization、人工确认、权限审计和事实边界。

当前依赖：部分具备。会议纪要 / 转写文本 ingestion 已完成，但原始音频不应早于版本、权限、审计进一步稳定。

是否放大现有风险：高。

是否适合下一阶段：不适合，建议后置。

## 4. 推荐路线

推荐下一阶段进入：

**Phase 2.19a：增量更新 / 文档版本治理最小闭环。**

理由：

1. PRD 与技术设计都要求支持版本管理、增量更新、latest 过滤和历史版本查询。
2. 当前已有多份同类文件和近似文件，版本混乱会直接影响检索、alias、audit 和 future facts。
3. facts 必须依赖稳定来源版本；否则会把旧文档里的内容固化为错误事实。
4. 最小版本治理可以复用现有字段，不需要先做复杂 diff 或后台。

## 5. Phase 2.19a 最小边界

### 5.1 同名 / 近似名版本识别

最小识别输入：

1. `title`
2. `source_uri`
3. 文件名 stem
4. `file_hash`
5. `content_hash`
6. 可选 `document_type` / `source_type`

最小目标：

1. 同名或高度近似文件上传时识别为同一 logical document 的新 version 候选。
2. 完全重复 hash 不重复建新版本。
3. 无法判断时保留新 document，但 trace / ingestion metadata 标记 `version_match_status=ambiguous`。

### 5.2 latest / active version 标记

最小规则：

1. 新版本确认后，将新 `document_versions.is_latest=true`。
2. 同一 document 的旧 version 标记 `is_latest=false`。
3. document 维持 `status=active`。
4. superseded version 不删除原始记录与 chunk。

### 5.3 superseded version 处理

最小规则：

1. 旧 version metadata 写入 `superseded_by_version_id`。
2. 旧 version `expired_at` 可写入当前时间。
3. 旧 chunks 保留，但默认 retrieval 不返回。
4. Qdrant / OpenSearch 旧索引可先通过 `is_latest=false` 与 status 过滤规避，不做物理删除。

### 5.4 retrieval 默认版本行为

最小规则：

1. 默认只命中 active/latest。
2. 显式查历史版本时才允许 `is_latest=false` 或指定 `version_id`。
3. trace 记录 `version_policy=latest_only` 或 `version_policy=explicit_history_version`。
4. audit 记录 `version_id` 与 `document_id`。

### 5.5 alias stale_version 诊断

最小规则：

1. alias 绑定 document_id / version_id 时保留绑定时间与 version_id。
2. 若该 version 后续被 superseded，alias 使用时 trace 标记 `alias_stale_version=true`。
3. 默认可继续解析到 document_id，但提示当前存在 newer version。
4. 不在本阶段实现复杂 alias 自动迁移策略。

### 5.6 audit 增强

最小记录：

1. `returned_document_ids`
2. `evidence_chunk_ids`
3. `version_ids`
4. `is_latest`
5. `version_policy`
6. `superseded_version_ids`

## 6. 最小测试计划

1. 重传同名不同 hash 文件，生成新 version。
2. 旧 version 被标记 `is_latest=false`。
3. 默认 retrieval 不返回旧 version chunk。
4. 显式历史版本查询可返回旧 version。
5. 完全重复 hash 不重复建版本。
6. alias 指向旧 version 时 trace 出现 `alias_stale_version=true`。
7. audit log 记录返回 evidence 的 `version_id`。

## 7. 非目标

1. 不做复杂文档 diff。
2. 不做完整文档生命周期后台。
3. 不做全库重建。
4. 不做物理删除旧 chunk。
5. 不做 facts 主线开发。
6. 不做完整 RBAC / ABAC。
7. 不做原始音频 ASR。
8. 不进入生产级 rollout。
9. 不改 retrieval contract。
10. 不改 memory kernel 主架构。

## 8. 当前结论

Phase 2.19a 最小实现已完成。

已完成：

1. 同名 / 同 source_type / 同 document_type 上传会复用同一 `document_id` 并创建新 `DocumentVersion`。
2. 新版本标记 `is_latest=true`、`metadata_json.version_status=active`。
3. 旧版本标记 `is_latest=false`、`metadata_json.version_status=superseded`、`superseded_by_version_id=<new_version_id>`。
4. `Document.metadata_json.current_version_id` 指向最新版本。
5. 默认 retrieval 保持 `is_latest=true`，只返回 latest chunks。
6. 显式 `version_id` 通过 filter extra 承载，允许查询历史版本，不改 retrieval contract。
7. 显式旧版本查询时 trace 输出 `version_scope.stale_version=true` 与 `latest_version_id`。
8. OpenSearch / Qdrant payload 已包含 `version_id`，并已补 `version_id` filter 支持。
9. audit log 记录 `version_ids` / `evidence_version_ids`。
10. 修复 live smoke 阻塞：supersede 旧版本时，OpenSearch 旧 `version_id` chunks 会按 `document_id + old_version_id` 限定更新 `is_latest=false`、`status=superseded`、`superseded_by_version_id=<new_version_id>`。

测试结果：

1. `tests/test_phase219_version_governance.py` 覆盖同名新版本、默认 latest retrieval、显式历史版本、stale trace、audit version_id、OpenSearch latest filter、OpenSearch superseded 限定更新、Qdrant version filter。
2. `tests/test_phase218_access_audit.py` 与 `tests/test_phase214_regression_eval.py` 同步回归通过。
3. 摄取相关回归 `tests/test_phase216_dense_ingestion.py`、`tests/test_structured_file_ingestion.py`、`tests/test_meeting_transcript_ingestion.py` 通过。
4. Phase 2.14 API eval 复跑 `11 passed / 0 failed / 1 skipped`。

Live smoke 复验：

1. 测试 document `120dbe44-4f7e-4266-97c2-c02118aff929` 的旧版 `896a19d7-2b01-4492-9672-bb4fdfbc7921` 已在 OpenSearch 中更新为 `is_latest=false`、`status=superseded`、`superseded_by_version_id=76ca95a1-393f-4278-b254-ab66295bb14f`。
2. 默认 sparse latest 查询只返回新版 `76ca95a1-393f-4278-b254-ab66295bb14f`，命中 `200 万元`，不再返回旧版 `100 万元`。
3. 显式旧 `version_id` sparse 查询只返回旧版 `896a19d7-2b01-4492-9672-bb4fdfbc7921`，命中 `100 万元`。
4. dense-only latest 查询只返回新版 `76ca95a1-393f-4278-b254-ab66295bb14f`。
5. hybrid latest 查询只返回新版 `76ca95a1-393f-4278-b254-ab66295bb14f`。
6. audit 默认 latest 只记录新版 `version_ids/evidence_version_ids=[76ca95a1-393f-4278-b254-ab66295bb14f]`。

降级项：

1. 当前不自动 merge 已存在但分属不同 `document_id` 的真实旧版 / 新版文件。
2. alias stale version 诊断依赖上层 alias 传入 `version_id`；Hermes 主仓库 alias store 的持久化升级可作为后续联调尾项。
3. 旧 Qdrant / OpenSearch payload 的 `is_latest` 更新采用 best-effort，失败不阻断 ingestion；若失败会导致 sparse 或 dense 旧版本泄露，当前列为高风险并需通过 live smoke 捕捉。

当前不建议下一阶段直接进入 facts、完整 RBAC/ABAC 或原始音频 ASR；建议先做 Phase 2.19a live smoke 与 baseline。

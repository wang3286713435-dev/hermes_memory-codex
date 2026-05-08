# Phase 2.54 Enterprise Memory Native UX Plan

## 1. 结论

Phase 2.54 正式采纳 `LOCAL_PR_ENTERPRISE_MEMORY_USABILITY_PROPOSAL.md` 的主线建议：后续 Hermes 不应只是“能检索企业文件的工具”，而应逐步变成把企业文件记忆视为原生能力的主 Agent。

这不是 production rollout、自动审标、Data Steward 实现、retrieval contract 大改或 memory kernel 主架构重写授权。它是内部 MVP 进入真实使用前必须补齐的 usability 主线。

## 2. 与 Phase 2.53 的关系

Phase 2.53 自然语言导入仍继续推进，但它不应被当成孤立功能。它属于更大的 File Steward UX 路线：

1. 文件导入更自然。
2. 文件发现更主动。
3. alias / active document 绑定更低摩擦。
4. 找不到文件时给候选和下一步建议。
5. 围绕文件回答时稳定显示标题、版本、路径 / 来源、citation 和 evidence scope。

因此后续推荐路线为：

1. Phase 2.53c：mocked natural import integration，验证 parser preflight、fake upload adapter、alias seed 和 import diagnostics 分离。
2. Phase 2.54a：file discovery / active document / alias failure UX planning or minimum implementation。
3. Phase 2.54b：operator feedback 和 file-answer ergonomics polish。
4. Phase 2.53d：仅在用户显式授权后做小型非敏感文件真实 upload smoke。

## 3. 目标体验

Hermes 应逐步具备以下默认心智：

1. 用户提到标书、纪要、清单、方案、合同或内部文件时，优先考虑企业记忆中的文件发现、锁定和文件问答。
2. 用户问“主标书在哪”时，优先返回候选标题、路径 / 来源、版本、document_id / version_id 和推荐下一步。
3. 用户说“继续看刚才那份文件”时，优先沿用 current document / active document，而不是要求重新输入咒语。
4. 绑定失败时，说明失败原因并给出下一步，例如当前 session 没有 active document、找到多个候选、建议使用更明确标题。
5. 文件内容回答必须保留 citation / evidence / Missing Evidence 边界。

## 4. 当前阶段允许的改进

当前可优先做低风险 UX / diagnostics / mocked integration：

1. import preflight diagnostics。
2. mocked upload success / failure diagnostics。
3. alias seed after mocked upload success。
4. import diagnostics 与 retrieval evidence 分离展示。
5. alias failure helper message。
6. active document continuation diagnostics。
7. file answer metadata display planning。

## 5. 当前阶段禁止事项

继续禁止：

1. production rollout。
2. 自动审标、自动投标、自动经营决策。
3. facts / transcript / snapshot 替代 retrieval evidence。
4. retrieval contract 大改。
5. memory kernel 主架构重写。
6. project-level alias 全量重构。
7. 真实 upload，除非进入单独授权的 Phase 2.53d。
8. 目录 / NAS / 网盘 / TB BIM 文件池导入。
9. Data Steward / 企业数据库 / BIM 模型管理实现。
10. DB / facts / document_versions / audit_logs / OpenSearch / Qdrant 写入，除非后续真实 upload smoke 明确授权并复用既有 upload path。

## 6. 减少人工干预的执行节奏

后续不再为每个小文档单独 baseline。推荐改为“大步长 bounded step”：

1. Green Lane 一轮可包含 planning、mocked implementation、target tests、docs sync。
2. 只有阶段完成、验收通过、切换范围或准备扩大风险时才 baseline。
3. Codex A 执行一轮较大的 bounded task 后停止给 Codex B review。
4. Codex B review 通过后，优先写下一轮实现 prompt，而不是频繁要求用户确认。
5. 遇到真实上传、真实 API / CLI smoke、DB / index 写入、repair、rollout、Data Steward、业务样本或权限密钥时必须停下等用户授权。

## 7. Phase 2.54 验收口径

Phase 2.54 系列不能宣称完整企业文件管家完成。它只证明：

1. Hermes 更像知道企业文件记忆是自己的原生能力。
2. 找文件、锁文件、继续问文件的路径更自然。
3. 失败时能给候选和下一步建议。
4. 文件回答仍保持 citation / evidence / Missing Evidence。
5. 员工使用门槛明显低于纯 alias / session 咒语。

## 8. Phase 2.53c Bridge Status

Phase 2.53c has implemented the first safe bridge into this route:

1. Natural import intent now has a mocked preflight flow.
2. No-import requests can continue normal retrieval flow.
3. Fail-closed import requests return import diagnostics without retrieval evidence.
4. Mocked upload success can return document / version / chunk counters and alias seed diagnostics.
5. Real upload remains out of scope until a separately authorized Phase 2.53d.

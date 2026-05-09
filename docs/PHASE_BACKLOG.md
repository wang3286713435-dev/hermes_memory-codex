# Phase Backlog

## 最新状态

1. Phase 2.56e 已通过 Codex B review，下一步执行 selective Git baseline。
2. 复核证据：主仓 py_compile 通过，natural import 目标测试 `34 passed`，Hermes_memory `git diff --check` 与 run record JSON / ignore 检查通过。
3. baseline 白名单限定 Phase 2.56e：真实 upload client、runtime wiring、upload client tests、交接文档。
4. 严禁 stage 历史无关 dirty、DB/NAS 草稿、ignored run records。
5. baseline 后停止，后续 Phase 2.57 再规划自然语言导入可用性 evidence pack / Mac mini MVP operator runbook。

## 最新状态

1. Phase 2.56e implementation + real smoke 已完成。
2. Hermes 主仓新增真实 Hermes_memory upload client，并在 feature flag 开启时由 natural import runtime 调用。
3. 用户授权 `.docx` 已通过自然语言 CLI 导入：`document_id=ee54b72c-b88b-4fad-be54-007240285356`，`version_id=950da5fe-dd7c-4eba-8764-916b556d14ce`，`chunk_count=1`，`indexed_count=1`。
4. `@C塔人力测算` 已在同 session 持久化，retrieval smoke 只返回新导入文档 citation/evidence。
5. 下一步必须先 Codex B review，再决定 Phase 2.56e selective baseline；不得自动 cleanup/delete/repair/backfill/reindex 或进入 rollout。

## 最新状态

1. Phase 2.56d baseline 已完成：
   - Hermes 主仓 `65089d5c8`
   - Hermes_memory `4773abe`
   - tag `phase-2.56d-natural-import-runtime-wiring-baseline`
2. 当前进入 Phase 2.56e Natural Import Real Upload Client + Real Smoke。
3. 2.56e 允许实现真实 Hermes_memory upload client，并复用用户授权 `.docx` 做自然语言导入真实 smoke。
4. 2.56e 不允许绕普通 upload path 声称成功，必须从 CLI 自然语言命令触发。
5. cleanup / delete / repair / backfill / reindex、Data Steward、production rollout 仍禁止。

## 最新状态

1. Phase 2.56d 已通过 Codex B review。
2. 当前已写入双仓 selective Git baseline prompt。
3. baseline 白名单仅包含 Phase 2.56d runtime wiring 代码、测试与交接文档。
4. baseline 后停止，不自动进入 Phase 2.56e。
5. Phase 2.56e 才可规划真实自然语言导入 smoke；当前不得上传真实文件或调用真实 upload API。

## 最新状态

1. Phase 2.56d Natural Import Runtime Wiring Minimum Implementation 已完成。
2. Hermes 主仓 runtime 现已在普通 retrieval / LLM answer 前调用 natural import preflight hook。
3. 默认真实 upload 仍关闭；明确导入 intent 会 fail-closed 返回 diagnostics，不进入普通 retrieval 乱答。
4. fake adapter success / failure / missing id 测试通过；runtime disabled-path CLI smoke 通过。
5. 下一步必须先由 Codex B review；通过后才可进入 Phase 2.56e 真实自然语言导入 smoke。

## 最新状态

1. Phase 2.56c blocked 结果已由 Codex B review：parser / adapter skeleton 可用，但 CLI runtime 尚未接入 natural import preflight / upload adapter。
2. 下一步进入 Phase 2.56d Natural Import Runtime Wiring Minimum Implementation。
3. 2.56d 只允许最小 runtime hook、fake / mocked adapter tests 与交接文档同步。
4. 2.56d 不执行真实 upload，不复用用户授权文件，不调用真实 Hermes_memory upload API。
5. 2.56d 完成后必须停给 Codex B review；通过后再规划 Phase 2.56e 真实自然语言导入 smoke。

## 最新状态

1. Phase 2.56c 用户授权单文件自然语言导入 smoke 已执行到 stop condition。
2. 文件 preflight、API health、Hermes CLI help、parser preflight 均通过。
3. 真实导入未执行，原因：Hermes 主仓 runtime 尚未调用 natural import preflight，也未配置真实 upload adapter。
4. 本轮未绕过为普通 `/api/v1/documents/upload`；未产生新的 document/version/chunk/OpenSearch/Qdrant 记录。
5. 下一步建议先由 Codex B review blocked 结果，再规划 Phase 2.56d runtime wiring 最小实现。

## 最新状态

1. 用户已授权 Phase 2.56c Natural Import Real Smoke。
2. 授权文件：`C塔项目人力配置及成本测算表0506.docx`，regular file，`16885 bytes`。
3. 下一步由 Codex A 执行自然语言导入真实 smoke，并生成 ignored sanitized run record。
4. 如果 runtime 尚未接入真实 upload adapter，必须报告 blocked，不得绕过成普通 upload 后声称自然语言导入通过。
5. cleanup / delete / repair / backfill / reindex、production rollout、Data Steward / DB / NAS / BIM 仍禁止。

## 最新状态

1. Phase 2.56b baseline 已完成：commit `683cf02`，tag `phase-2.56b-natural-import-real-smoke-plan-baseline`。
2. 当前处于 Phase 2.56c Natural Import Real Smoke Authorization Gate。
3. 真实自然语言导入 smoke 需要用户重新提供小型非敏感文件路径并明确授权。
4. 未授权前不得调用真实 upload API、不得上传文件、不得运行 API / CLI smoke。
5. Data Steward / DB / NAS / BIM 分支继续独立，不进入当前授权门槛。

## 最新状态

1. Phase 2.56b Natural Import Real Smoke docs-only planning 已通过 Codex B review。
2. 当前已写入 docs-only selective baseline prompt。
3. baseline 仅允许 Phase 2.56b planning 与交接文档。
4. 仍不得执行真实 upload、API / CLI smoke、DB / OpenSearch / Qdrant 写入。
5. baseline 后停止等待 Codex B review；不得自动进入 Phase 2.56c。

## 最新状态

1. Phase 2.56a Natural Import Real Adapter Skeleton 已通过 Codex B review。
2. Hermes 主仓 feature-flagged upload adapter skeleton 保持真实 upload 默认关闭。
3. Codex B 已复跑目标测试：py_compile 通过，natural import 三组测试 `25 passed`。
4. 当前已写入 dual-repo selective baseline prompt。
5. baseline 后停止等待 Codex B review；不得自动进入 Phase 2.56b。

## 最新状态

1. Phase 2.55a 单文件内部 MVP 真实 upload smoke 已通过 Codex B review。
2. 不需要 Codex C targeted validation；API 顶层 `citations=[]` 记录为 P2 展示尾项，不阻塞 baseline。
3. 当前已写入 Phase 2.55a selective Git baseline prompt。
4. baseline 白名单仅包含 8 个 Phase 2.55a 交接文档；不得纳入旧 dirty、DB / NAS 草稿或 ignored run records。
5. baseline 后停止等待 Codex B review；不得自动进入 Phase 2.56。

## 最新状态

1. Phase 2.55a 单文件内部 MVP 真实 upload smoke 已完成并通过。
2. 新上传文件：`document_id=06e59241-95e9-44ff-a73d-35d2f52a359b`，`version_id=7dc57676-c707-4f44-9688-0b77058f07a0`，`chunk_count=26`。
3. API hybrid retrieval 与 Hermes CLI alias / retrieval smoke 均只返回新上传文件 evidence；无第三文件污染，metadata/facts/snapshot 未替代 retrieval evidence。
4. 本轮已生成 ignored sanitized run record：`reports/internal_mvp_runs/phase255a_real_upload_smoke_20260509_102038.json`。
5. 当前下一步：等待 Codex B review；不自动 baseline，不进入 Phase 2.56，不执行 cleanup / delete / repair / backfill / reindex。

## 最新状态

1. 用户已提供并授权一个小型 `.docx` 文件用于 Phase 2.55a 内部 MVP 真实 upload smoke。
2. 授权文件：`/Users/Weishengsu/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_sn2cczdp4u2l12_c2fd/msg/file/2026-05/卓羽智能核心技术能力汇报 PPT 大纲V1.0.docx`，大小 `49894 bytes`。
3. Codex B 已写入 `docs/NEXT_CODEX_A_PROMPT.md`：只允许 Codex A 执行单文件 upload / ingestion / retrieval smoke 与 ignored sanitized run record。
4. 本轮不直接上传；不授权 cleanup / delete / repair / backfill / reindex / migration；Data Steward / BIM / NAS / TB 文件池继续后置。
5. 下一步：Codex A 执行 Phase 2.55a prompt，完成后停止等待 Codex B review。

## 最新状态

1. Phase 2.55 planning 已通过 Codex B review：规划文件明确单文件、小型、非敏感、用户显式授权、sanitized run record 与 stop conditions。
2. 当前进入 Phase 2.55 docs-only baseline prompt；baseline 后停止。
3. Phase 2.55a 真实 upload smoke 仍未授权，必须等待用户提供非敏感文件路径并明确授权。

## 最新状态

1. Phase 2.55 docs-only planning 已完成：新增 `docs/PHASE255_INTERNAL_MVP_REAL_UPLOAD_SMOKE_PLAN.md`。
2. 规划结论：后续 Phase 2.55a 只可在用户明确提供小型非敏感文件路径并授权后执行真实 upload smoke。
3. Phase 2.55a 可允许产生测试 document/version/chunk/index 数据，但不得 cleanup/delete/repair/reindex。
4. 当前仍不进入 Data Steward / BIM / NAS / TB 文件池，不进入 production rollout。

## 最新状态

1. Phase 2.54c baseline 已完成：Hermes 主仓 `6e2c6b2fe`，Hermes_memory `744bb9e`，tag `phase-2.54c-file-steward-display-tail-baseline`。
2. 当前进入 Phase 2.55 Internal MVP Real Upload Smoke Planning。
3. Phase 2.55 只规划小型非敏感文件真实导入 smoke；不执行 upload、不运行 API / CLI、不写 DB / index。
4. Phase 2.55a 真实 upload smoke 需要用户明确提供非敏感文件路径并授权。

## 最新状态

1. Phase 2.54c Codex C targeted re-smoke 已通过：Q3 file answer metadata 可见 required fields、echo required、title/source_name/source_type/citation_count 与四个 safety flags。
2. 可选 alias missing 快速回归通过；未出现 metadata / facts / transcript / snapshot 替代 evidence，未出现第三文件污染。
3. 当前进入 Phase 2.54c selective Git baseline prompt；baseline 后停止，不自动进入 Phase 2.55。

## 最新状态

1. Phase 2.54c display-tail fix 已通过 Codex B review：主仓 py_compile 通过，targeted pytest `74 passed`，Hermes_memory 静态检查通过。
2. 当前已写入 Codex C targeted re-smoke prompt，只重测 Q3 file answer metadata，不扩大为完整 Pilot smoke。
3. 通过前不得 baseline，不得进入 Phase 2.55。

## 最新状态

1. Phase 2.54c display-tail fix 已完成：`ContextBuilder` 的 file answer metadata diagnostics 现在明确要求回显 `document_id/version_id/title/source_name/source_type/citation_count` 与 safety flags。
2. 主仓目标测试通过：py_compile 通过，`tests/agent/test_file_steward_ux.py tests/agent/test_session_document_scope.py tests/agent/test_facts_agent_context.py` 为 `74 passed`。
3. 本轮仍未执行真实 CLI smoke、未上传文件、未写 DB / OpenSearch / Qdrant、未改 retrieval contract 或 memory kernel 主架构。
4. 下一步必须先由 Codex B review；通过后再由 Codex C 重跑 Q3 file answer metadata targeted smoke，不自动 baseline 或进入 Phase 2.55。

## 最新状态

1. Phase 2.54c Codex C targeted CLI smoke 已完成：Q1 alias missing 与 Q2 active document continuation 均通过，Q3 file answer metadata 为 partial。
2. 当前最小阻塞点不是 evidence 安全边界，而是最终 CLI 输出中 `source/title` 与 `metadata_as_answer=false` / `facts_as_answer=false` / `snapshot_as_answer=false` flags 未稳定透出。
3. 已写入 Phase 2.54c display tail fix prompt：下一步 Codex A 只允许做 `ContextBuilder` 展示层最小增强与目标测试。
4. 仍不允许真实 upload、DB / index 写入、retrieval contract 修改、Data Steward / BIM / NAS / TB 文件池或 rollout。

## 最新状态

1. Phase 2.54b baseline 已完成：Hermes 主仓 `5e824a884`，Hermes_memory `12dc641`，tag `phase-2.54b-file-steward-context-display-baseline`。
2. 当前进入 Phase 2.54c File Steward UX targeted CLI smoke。
3. 下一步由 Codex C 验证真实 CLI 是否能展示 alias failure、active document continuation、file answer metadata，并保持 evidence 边界。
4. 本轮不写新功能、不真实 upload、不进入 Data Steward 或 rollout。

## 最新状态

1. Phase 2.54b File Steward UX runtime display integration 已通过 Codex B review，下一步只做 selective Git baseline。
2. `ContextBuilder` 已新增 `File steward diagnostics:`，可展示 alias failure、active document continuation 与 file answer metadata。
3. 目标测试 `73 passed`；未运行 API / CLI smoke，未真实 upload，未写 DB / OpenSearch / Qdrant。
4. baseline 后再决定 Phase 2.54c planning；不自动进入 runtime upload 或 Data Steward。

## 最新状态

1. Phase 2.54a 双仓 baseline 已完成：Hermes 主仓 `a34954c85`，Hermes_memory `eadb3ff`，tag `phase-2.54a-file-steward-ux-helper-baseline`。
2. 当前进入 Phase 2.54b File Steward UX runtime display integration。
3. 2.54b 只接入 `ContextBuilder` 展示层：alias failure helper、active document continuation、file answer metadata diagnostics。
4. 当前仍不允许真实 upload、DB / index 写入、retrieval contract 修改、Data Steward 或 rollout。

## 最新状态

1. Phase 2.53c 双仓 baseline 已完成：Hermes 主仓 `1f4309abe`，Hermes_memory `4a06ef9`，tag `phase-2.53c-natural-import-mocked-integration-baseline`。
2. 当前进入 Phase 2.54a Enterprise Memory Native UX / File Steward UX minimum implementation。
3. Phase 2.54a 只做纯 helper + unit tests：alias failure helper、active document continuation hint、file answer metadata display structure。
4. Phase 2.53d 小型非敏感文件真实 upload smoke 继续后置，必须由用户显式授权。
5. Data Steward / BIM / NAS / TB 文件池仍是后置产品线，不进入当前 MVP 主线实现。

## 最新状态

1. 本地 PR `LOCAL_PR_ENTERPRISE_MEMORY_USABILITY_PROPOSAL.md` 已采纳为后续主线方向：Hermes 要从“能检索文件的系统”升级为“原生理解企业文件记忆能力的主 Agent”。
2. 新增 `docs/PHASE254_ENTERPRISE_MEMORY_NATIVE_UX_PLAN.md`，固化 File Steward UX 路线。
3. Phase 2.53c 下一步不是小修 alias，而是 mocked natural import integration + Enterprise Memory Native UX bridge。
4. 后续减少人工干预：Green Lane 一轮可包含 planning、mocked implementation、target tests、docs sync；只有真实 upload / DB / index / rollout / Data Steward 等风险扩大时才停。
5. Phase 2.54a 后续重点：file discovery first、active document continuation、alias failure helper、file-answer metadata display。

## 最新状态

1. Phase 2.53b planning 已通过 Codex B review，下一步只做 docs-only Git baseline。
2. Phase 2.53b baseline 白名单：`PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md` 与交接文档。
3. baseline 不得纳入 `PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`、Mac Mini untracked docs、Hermes 主仓 dirty 或任何代码。
4. baseline 后停止等待 Codex B review，再决定 Phase 2.53c mocked adapter / kernel integration。

## 最新状态

1. Phase 2.53b docs-only planning 已完成：新增 `docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md`。
2. 推荐 Phase 2.53c 只做 mocked adapter / kernel integration tests：parser preflight、fake upload adapter、alias seed、diagnostics separation。
3. Phase 2.53d 才可在用户显式授权后做小型非敏感文件真实 upload smoke。
4. 当前仍不允许真实 upload、API / CLI smoke、DB / index 写入、目录 / NAS / TB BIM 文件池或 Data Steward。

## 最新状态

1. Phase 2.53a Git baseline 已完成：Hermes 主仓 commit `f15a56de7`，Hermes_memory commit `c841104`，tag `phase-2.53a-natural-file-import-parser-baseline`。
2. 当前进入 Phase 2.53b Natural Language File Import Adapter / Kernel Integration Planning。
3. Phase 2.53b 只做 docs-only planning：规划 parser 调用位置、upload adapter 接口、alias seed、import diagnostics 与 fail-closed 边界。
4. Phase 2.53b 不写代码、不接真实 upload、不运行 API / CLI smoke、不上传真实文件。
5. Phase 2.53c 才可考虑 mocked adapter / kernel integration；Phase 2.53d 才可在用户显式授权后做小文件真实 upload smoke。

## 最新状态

1. Phase 2.53a Codex B review 已通过：自然语言导入 parser / dry-run planner 的否定 intent 已 fail closed。
2. 下一步只允许执行 Phase 2.53a selective Git baseline，不进入 Phase 2.53b。
3. 本轮 baseline 白名单：Hermes 主仓 `natural_file_import.py` / `test_natural_file_import.py`，Hermes_memory 交接文档；不得 stage 既有 out-of-scope dirty / untracked docs。
4. Phase 2.53b adapter / alias seed / kernel integration 后置；真实 upload smoke 仍需单独授权。

## 最新状态

1. Phase 2.53a Natural Language File Import Parser / Dry-run Planner review-fix 已完成，等待 Codex B review。
2. 否定导入 intent 已 fail closed：`不要导入 / 不要上传 / 不要收录` 等返回 `detected=false`。
3. Hermes_memory out-of-scope tracked docs deletion 已恢复：`docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`、`docs/MVP_PILOT_RUNBOOK.md`。
4. 主仓目标测试通过：py_compile passed，`tests/agent/test_natural_file_import.py` 为 `10 passed`。
5. adapter / alias seed / kernel integration 后置 Phase 2.53b；真实 upload smoke 需单独授权。

## 最新状态

1. Phase 2.50c Sanitized Internal MVP Evidence Pack Template 已完成，等待 Codex B review。
2. 新增 JSON / Markdown sanitized template 与 Phase 2.50c boundary artifact；未生成真实 evidence pack。
3. 2.50c 只创建 docs / sanitized template，不读取真实 reports，不运行 API / CLI，不进入 rollout。
4. 继续排除 out-of-scope dirty：`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`、`docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`、`docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`。


## 最新状态

1. Phase 2.50b internal MVP evidence pack planning 已完成，等待 Codex B review。
2. Evidence pack 被定义为内部受控 MVP 人工审阅证据包，不是 production rollout approval、customer delivery、automatic tender review、automatic bid、automatic business decision 或 repair authorization。
3. 本轮不生成真实 evidence pack、不读取真实 reports、不运行 API / CLI、不启动服务、不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant、不进入 rollout。
4. Phase 2.51a Git baseline 已完成：commit `1aa6807f38d5a9242640a6822d35aeacafc3dc22`，tag `phase-2.51a-fake-deployment-record-dry-run-baseline`。
5. 继续排除 out-of-scope dirty：`docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`、`docs/MAC_MINI_MINIMAL_MVP_DEPLOY_GUIDE.md`、`docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md`。


## 当前优先级

1. 当前第一优先级：Codex B review Phase 2.53a review-fix。
2. 如 review 通过，下一步可选择 Phase 2.53a baseline 或 Phase 2.53b adapter / kernel integration planning。
3. Phase 2.53b 前仍不得直接上传真实文件；真实 upload smoke 需单独授权。
4. 真实 upload smoke、真实文件导入、目录递归导入、NAS / TB BIM 文件池、Data Steward、rollout 均需单独授权。
5. Phase 2.50c evidence pack 后续只可作为内部受控 MVP review bundle，不能替代人工业务判断。
6. Phase 2.51a baseline 已完成：commit `1aa6807f38d5a9242640a6822d35aeacafc3dc22`，tag `phase-2.51a-fake-deployment-record-dry-run-baseline`。
7. Phase 2.51 / 2.51a / 2.51b 继续明确 Mac Mini 是内部受控 MVP 运行机，不是 production rollout / 客户交付 / 自动审标 / 自动投标 / 自动经营决策环境。
6. Phase 2.48b Meeting Transcript Boundary Trace Display Polish 已完成并通过 Codex B review。
2. Hermes 主仓 meeting transcript context 现在稳定显示：
   - `meeting_transcript_used=true`
   - `transcript_as_fact=false`
   - `evidence_required=true`
   - `meeting_transcript_as_confirmed_fact=false`
3. Phase 2.48b 不改 meeting ingestion contract / retrieval contract / memory kernel 主架构，不运行 smoke，不写 DB / index。
4. Phase 2.48a Excel Citation Display Polish 已完成，Codex B review 通过。
5. Hermes 主仓 Excel citation display 现在区分：
   - `citation_precision=cell_range`
   - `citation_precision=multi_row_range`
   - `row_range_fallback=true`
   - `citation_precision=row_range_fallback`
6. 当前落地判断：内部受控 MVP 可以继续；production rollout / 客户交付 / 自动审标 / 自动投标 / 自动经营决策仍禁止。
7. Codex C targeted smoke 已通过：Excel citation display 与 meeting transcript boundary display 均 pass；当前下一步是 Phase 2.48 combined Git baseline。
8. Phase 2.47 combined docs artifact baseline 已完成：commit `bfe7981`，tag `phase-2.47-internal-mvp-operating-artifacts-baseline`。
9. Phase 2.47 planning、2.47a checklist、2.47b run record template 已形成可复用 docs artifact 包。
10. Phase 2.46d Mac mini local MVP smoke result baseline 已完成：commit `255c2e97fa6d644c2d83655e7ac919c8401f54f2`，tag `phase-2.46d-mac-mini-local-mvp-smoke-result-baseline`。
11. Codex C smoke 结果：`Go`，P0=0，P1=0，P2=2；仅支持 internal controlled MVP continuation。
12. Mac mini 已到货且 smoke Go，但不等于 production rollout ready。

## Day-1 Pilot 已知问题

1. P1 retrieval recall：`@主标书` 最高投标限价 / 招标控制价 / 投标报价上限未召回具体金额。
2. P1 retrieval recall：`@主标书` 投标资质具体等级 / 类别未召回。
3. P1 partial：项目经理、联合体、业绩、人员要求已有相关 evidence，但仍需人工复核。
4. P2 latency：会议纪要决策 / 风险与公司方向分析长输出偏慢。
5. Pilot 期间所有经营建议必须保留人工决策声明，不得当成自动经营决策。

## Phase 2.35 当前状态

1. Phase 2.35 最小实现已完成，目标测试 `22 passed`。
2. Codex C 复验显示安全边界通过：无编造、facts/transcript 均未替代 evidence。
3. Phase 2.35b 已完成 metadata precision 小修：限价需具体金额，资质需具体等级 + 类别。
4. Phase 2.35b 已新增 API trace 顶层 profile 字段：`metadata_guided_query_profile`、`metadata_deep_field_profile`。
5. alias 首次绑定不稳定已在 Codex C 真实 CLI 中复现：bind 成功后正式 Q1/Q2 变为 `alias_missing=true / retrieval_suppressed=true`。
6. Phase 2.35c 已完成主仓库最小修复：`上一轮已锁定的当前文件` 等说法现在会走 current-document bind / current retrieval fallback，不再被误当成标题或历史上下文。
7. Codex C 真实终端复验通过：session `20260429_165301_e3c312` 中正式 Q1/Q2 均为 `alias_resolved`，`alias_missing=false`，`retrieval_suppressed=false`。
8. Phase 2.35c Git baseline 已完成：Hermes_memory commit `ec77c96`，Hermes 主仓库 commit `ead4e899`，tag `phase-2.35c-alias-session-baseline`。
9. Phase 2.35c baseline 只能声明 alias/session 修复收口；deep-field recall 与 trace 透出仍不完全收口。

## Phase 2.36 规划入口

1. 目标：把 Phase 2.35c 剩余 tail item 分清是“真实缺字段 / 章节召回不足 / trace 展示问题 / 需人工复核”。
2. 重点字段：最高投标限价 / 招标控制价 / 投标报价上限、投标资质具体等级 / 类别、项目经理等级 / B 证、联合体、类似业绩、人员数量 / 专业 / 资质。
3. 推荐方向：优先规划 section-targeted retrieval diagnostics 与 trace polish，不直接扩大到完整自动审标。
4. 规划阶段不需要 Codex C；只有进入实现并影响真实终端输出后才需要真实 CLI 复验。

## Phase 2.36a / 2.36b 当前状态

1. Phase 2.36a Hermes_memory retrieval-layer trace diagnostics 已完成并通过 Codex B review，目标测试合计 `30 passed`。
2. Codex C 真实终端抽样显示 Q1/Q2 安全边界正常、无编造，但终端 trace 仍为 `metadata_deep_field_profile=null`、`deep_field_profile=null`、`deep_field_diagnostics=null`。
3. 失败定位转入 Hermes 主仓库 adapter / kernel / context_builder trace 映射与展示层。
4. Codex C 指定 Step 1 一步绑定 prompt 仍失败：`请在企业记忆中锁定“...”，并绑定为 @主标书` 未被 alias bind parser 稳定识别。
5. 下一步 Phase 2.36b 只做主仓库消费层 / 展示层最小修复；不扩大 Hermes_memory retrieval 逻辑，不进入真实业务数据写入。
6. Phase 2.36b 主仓库最小实现已完成：adapter / kernel / context_builder 可提升并渲染 deep-field trace，session scope parser 支持 `绑定为 / 绑定成` 与中文弯引号标题。
7. Phase 2.36b 目标测试通过：主仓库 py_compile 通过，`tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py` 为 `59 passed`。
8. Codex C 终端复验显示 Phase 2.36b 的一步 alias binding 与 terminal-visible trace 已基本通过：Q1/Q2 分别显示 `pricing_scope` / `qualification_scope` 与 diagnostics。
9. Phase 2.36b 暂不 baseline：Q1 diagnostics 出现 concrete found 与答案 Missing Evidence 不一致；Q2 对“一级注册建造师电子证书要求”存在过度表述为项目经理等级的风险。
10. Phase 2.36c 已完成 Hermes_memory 最小修复：final retrieval evidence 会重新校正 concrete evidence，metadata anchor 不足时输出保守 Missing Evidence diagnostics。
11. Phase 2.36c 已补项目经理等级边界：电子证书格式 / 材料条款不能作为 explicit role-level requirement。
12. Phase 2.36c 目标测试 `33 passed`；Codex B review 已通过。
13. Codex C 真实终端复验已通过：session `20260430_123308_6660a8` 中 Step 1 alias binding 成功，Q1 限价 diagnostics 与 Missing Evidence 一致，Q2 未把电子证书 / 材料条款推断为项目经理等级。
14. Phase 2.36c Git baseline 已完成：commit `d491a44`，tag `phase-2.36c-tender-deep-field-diagnostics-baseline`。
15. deep-field recall 仍 partial，真实限价金额、具体资质等级 / 类别、业绩、人员数量继续作为后续尾项，不得写成完整自动审标能力收口。

## Phase 2.37 规划入口

1. 目标：把 Day-1 / Codex C / 用户真实试用反馈转成结构化 issue intake records。
2. 推荐先做 issue intake / triage，而不是继续盲修 deep-field recall。
3. issue_type 至少覆盖 retrieval_recall、trace_ux、latency、alias_session、contamination_false_positive、missing_evidence_expected、answer_boundary。
4. priority 规则必须保留 P0/P1/P2/P3，P0 包括编造、facts/transcript 替代 evidence、跨文件污染、权限泄露和自动决策越界。
5. Phase 2.37 规划已完成，新增 `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`。
6. 推荐 Phase 2.37a：local issue intake schema / templates / dry-run validator or summary generator。
7. Phase 2.37a 仍不得自动修复 issue、写 DB / facts / document_versions、修改 OpenSearch / Qdrant、进入 rollout 或做自动审标结论。
8. Phase 2.37 planning Git baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
9. Phase 2.37a 入口已写入 `docs/NEXT_CODEX_A_PROMPT.md`：local issue intake schema / template / dry-run validator + summary generator。
10. Phase 2.37a 最小实现已完成：本地 intake 工具支持 template、单文件 / 目录读取、schema 校验、triage summary 与 strict invalid exit。
11. Phase 2.37a 目标验证通过：py_compile 通过，`tests/test_phase237a_pilot_issue_intake.py` 为 `9 passed`，临时 dry-run smoke 通过。
12. 下一步需 Codex B review；通过后只做 Phase 2.37a Git baseline，不直接进入 deep-field recall 修复、repair 或 rollout。
13. Phase 2.37a Git baseline 已完成：commit `1e1ca45`，tag `phase-2.37a-pilot-issue-intake-baseline`。
14. Phase 2.37b 最小 runbook / storage convention 已完成：新增 `docs/MVP_PILOT_ISSUE_INTAKE_RUNBOOK.md` 与 `reports/pilot_issues/` ignore / README 策略。
15. Phase 2.37b 验证通过：`git diff --check` 通过，template / strict dry-run 命令通过，`reports/pilot_issues/example.json` 被 git ignore 命中。
16. 下一步需 Codex B review；通过后只做 Phase 2.37b docs baseline，不直接进入 P1 修复、repair 或 rollout。
17. Phase 2.37b Git baseline 已完成：commit `e8c0631`，tag `phase-2.37b-pilot-issue-intake-runbook-baseline`。
18. Phase 2.37c planning 已完成：新增 `docs/PHASE237C_PILOT_ISSUE_TRIAGE_SUMMARY_PLAN.md`，规划 daily / per-round triage summary、P0/P1/P2/P3 分诊、首批 known issue 候选与后续 Phase 2.37d 方向。
19. 下一步需 Codex B review；通过后只做 Phase 2.37c docs baseline，不直接进入 P1 fix、repair、rollout 或外部 issue 创建。
20. Phase 2.37c Git baseline 已完成：commit `4aa6bd4`，tag `phase-2.37c-pilot-issue-triage-summary-plan-baseline`。
21. Phase 2.37d 最小实现已完成：新增本地 triage summary generator，读取 `reports/pilot_issues/*.json` 并输出 ignored 的 JSON / Markdown summary；目标测试 `9 passed`，`git diff --check` 通过。
22. Phase 2.37d Git baseline 已完成：commit `d97a67c`，tag `phase-2.37d-pilot-triage-summary-baseline`。
23. Phase 2.38a 最小实现已完成：新增只读 source availability audit runner，字段覆盖限价、资质等级/类别、项目经理等级、类似业绩、人员要求；目标测试 `10 passed`。
24. Phase 2.38a Git baseline 已完成：commit `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。
25. Codex B localhost 覆写 read-only live audit 显示：`price_ceiling=anchor_only`，`qualification_grade_category=concrete_source_found`，`project_manager_level=ambiguous`，`performance_requirement=concrete_source_found`，`personnel_requirement=concrete_source_found`。
26. Phase 2.38b 最小实现已完成：新增只读 concrete recall diagnostics runner，目标测试 `9 passed`，`git diff --check` 通过。
27. Phase 2.38b localhost read-only preview：`qualification_grade_category=candidate_in_top_k`，`performance_requirement=candidate_in_top_k`，`personnel_requirement=candidate_present_but_low_rank`。
28. `price_ceiling` 保持 `field_should_remain_missing_evidence`；`project_manager_level` 保持 `field_requires_human_review`。
29. Phase 2.38b Codex B review 已通过，下一步只做 Git baseline，不直接进入 2.38c。
30. Phase 2.38b Git baseline 已完成：commit `a8c93f1`，tag `phase-2.38b-tender-recall-diagnostics-baseline`。
31. Phase 2.38c planning 已完成：新增 `docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`，结论为人员要求低排名更像 query/profile/candidate-pool tail，不是 source missing。
32. Phase 2.38c 推荐后续 Phase 2.38d：personnel-only aliases / section hints / candidate-pool diagnostics；继续后置限价缺源、项目经理人工复核、broad retrieval tuning、repair 与 rollout。
33. Phase 2.38c Git baseline 已完成：commit `ff49941`，tag `phase-2.38c-personnel-recall-tail-plan-baseline`。
34. Phase 2.38d 入口已写入 `docs/NEXT_CODEX_A_PROMPT.md`：仅处理 `personnel_requirement` 低排名，禁止顺手处理限价、项目经理等级、broad retrieval tuning、repair、reindex 或 rollout。
35. Phase 2.38d 首轮实现、review-fix 与 Q1 intent fix 已通过 Codex B 复审。
36. Codex C 真实终端复验显示 retrieval / trace 层已修复：Q1/Q2 均为 `personnel_scope`，metadata fields 仅 `personnel_requirement`；Q3 broad query 仍为 `qualification_scope`。
37. Codex C 第二轮复验显示最终回答仍失败：Q1/Q2 会输出项目经理 / 每个项目只能1个 / 类似工程业绩，Q3 人员小节仍有隐式数量过度表述。
38. 主仓第二轮 final answer guard 已完成：`personnel_scope` context block 明确禁止输出项目经理 / 项目负责人 / 注册建造师 / 一级建造师 / B证 / 安全考核证 / 投标资质 / 联合体 / 类似工程业绩，且禁止把角色列表转成隐式数量。
39. 第三轮 structured answer guard 已完成：`personnel_forbidden_answer_terms`、`personnel_count_inference_forbidden=true`、`ignore_non_personnel_content_in_mixed_chunks=true` 已进入 `personnel_scope` context。
40. broad `qualification_scope` 不应误套 personnel-only boundary 的测试已补，主仓目标测试 `12 passed`。
41. 第四轮 safe fallback contract 已完成：若答案草稿含 forbidden terms 或隐式数量推断，context 要求丢弃草稿并输出 Missing Evidence / 人工复核模板。
42. 当前白名单未允许修改 `run_agent.py`；本轮未接入真正 post-answer retry / replacement，仍需 Codex C 真实终端复验。
43. 下一步等待 Codex B review；通过后建议 Codex C 重跑 Q1/Q2/Q3；通过后再由 Codex B 写入 Phase 2.38d Git baseline prompt。

## 后置项

1. 完整 AI 审标 / 自动审标：后置，当前只做 retrieval evidence 与 trace 改善。
2. 长输出 query 延迟优化：需先收集更多 Pilot 样本，不在 Phase 2.35b 中扩大。
3. repair executor：后置，必须经过单独 Phase 规划、人工确认和显式指令。
4. item-level audit summary：后置，避免过早暴露 fact_id / document_id 等实体信息。
5. report review 写业务 DB：后置到 Yellow Lane；仅允许 Codex B 审核后显式 opt-in 的 report-level sanitized audit 写入。
6. archive / review / audit 默认 readiness 扫描：后置，避免未使用 review workflow 的环境产生噪声。
7. rollout readiness：后置，当前仍不进入生产 rollout。
8. production cron / scheduler：后置，Nightly Sprint 只做本地协作协议，不创建系统定时任务。
9. default real reports / reviews scan：后置，除非用户显式指定输入。
10. production rollout 继续后置；MVP Pilot 不得解释为 production ready。
11. Data Steward 产品化、Building Asset Catalog MVP、建筑本体 / 知识图谱、空间索引、子 Agent 调度与监控面板均后置；当前不新增 DB schema、Neo4j、PostGIS、空间索引代码或生产级 scheduler。

## 永久边界

1. 不擅自修改 retrieval contract。
2. 不擅自修改 memory kernel 主架构。
3. 不执行 destructive repair / delete / cleanup。
4. 不让 facts 自动替代 retrieval evidence。
5. 不创建生产 cron / 定时任务。
6. 每轮开始读取 ACTIVE_PHASE 与 PHASE_BACKLOG。
7. 用户要求执行任务入口时，读取 `docs/NEXT_CODEX_A_PROMPT.md`。
8. 夜间执行时读取 `docs/NIGHTLY_SPRINT_PROTOCOL.md` 与 `docs/NIGHTLY_SPRINT_QUEUE.md`。
9. 每轮结束更新 ACTIVE_PHASE、HANDOFF_LOG、reports/agent_runs/latest.json。
10. 夜间 sprint 结束额外写入 ignored 的 `reports/nightly_runs/<timestamp>.json`。
11. planning / implementation / validation / baseline 分阶段推进。
12. baseline 前默认需要 Codex B 审核，除非用户明确授权。

# Hermes Memory 当前待办清单

## Phase 2.116b Natural Import Response Polish No-Go Fix

1. 本地最小修复已完成：fuzzy discovery default candidate display 不再把 `title/source_name/display_path` 的绝对路径原样暴露给用户。
2. 同会话 alias retrieval 的 contamination trace 现在会基于实际 returned evidence 覆盖 stale `third_document_contamination`，in-scope evidence 不再误报第三文件污染。
3. 验证通过：targeted regression `2 passed`；py_compile 通过；natural import / flow / session scope / structured citation / file steward regression `132 passed`。
4. 未执行 OpenWebUI / 8642 live validation，未上传，未写 DB / facts / versions / OpenSearch / Qdrant。
5. Codex B review 通过，runtime candidate 已推送：Hermes main `f887d12bf` / `phase-2.116b-natural-import-response-polish-fix-runtime-candidate`。
6. Codex C 在正确 2.116b 版本上复验仍返回 `No-Go`：Case 2 `third_document_contamination=true`，Case 4 `raw_path_output=true`。
7. 下一步：打回 Codex A 进入 2.116c root-cause-first 修复。当前不进入下一阶段，不做 stable closeout。

## Phase 2.116c

1. Codex A 必须先定位根因，不能继续猜测式补丁。
2. 需要证明并修复：污染信号最终来自哪个 trace/context 字段；raw path 从哪个候选字段穿透；safe candidate 为什么为空。
3. 修复后需目标测试 + 回归，再交 Codex B review 和 Codex C live validation。

## Phase 2.116 Natural Import User-facing Response Polish

1. 本地最小实现已完成：默认导入成功回复显示工作区、分类、别名、后续提问建议；导入失败回复说明路径不可见并提示授权目录。
2. 诊断字段保留给 `response.diagnostics` / 显式 debug render；默认普通用户不再看到整段 `Natural file import diagnostics`。
3. Fuzzy discovery 默认候选隐藏 `document_id/version_id/chunk_count/workspace_id` 等技术字段，只展示 safe alias / workspace / category。
4. 验证：Hermes 主仓 py_compile 通过；targeted suite `38 passed`；扩展 natural import / session / file steward regression `130 passed`。
5. Codex B review 通过，Hermes main runtime candidate 已推送：`e04cc6feb` / `phase-2.116-natural-import-response-polish-runtime-candidate`。
6. Codex C / 测试机复验返回 `No-Go`：fuzzy discovery 默认回复仍泄露 raw path；alias retrieval 出现第三文件污染信号。
7. 下一步：Codex A 执行 Phase 2.116b 最小修复，仅处理上述两个 blocker。
8. 继续禁止改 upload adapter、ingestion/indexing、retrieval contract、workspace inference、平台 Gateway、NAS 或 production rollout。

## Phase 2.115 Workspace Context / Auto Alias / Fuzzy File Discovery

1. 新增用户体验 P0/P1 需求：自然语言导入不应要求用户手填 `PROJECT_CONTEXT`；Hermes 应自动推断 `workspace_context`。
2. Codex A 已完成本地 runtime candidate：从安全文件名 / 目录标签 / 会话 / 既有 alias 推断工作区，自动生成安全 alias，并将 imported document/version 绑定到工作区注册表。
3. 模糊找文件可返回安全候选，例如“我找到 @C塔主标书 / @C塔人力成本测算表，你说的是哪一个？”。
4. Codex B review 通过，目标验证 `129 passed`；runtime candidate 为 `1ac8099e4` / `phase-2.115-workspace-auto-alias-runtime-test-candidate`。
5. 下一步：测试机 / OpenWebUI / 8642 验证无 `PROJECT_CONTEXT`、无显式 `ALIAS` 的导入流。
6. 工作区/alias/import diagnostics 仍不是正文 evidence；回答内容必须通过 retrieval evidence + citation。
7. 继续禁止 raw path / raw content / secret 写 memory，禁止 NAS full scan，禁止 DWG/RVT/BIM content overclaim。

## Phase 2.114a Final User-flow Acceptance Go

1. 测试机 / OpenWebUI / 8642 已复验 `phase-2.114a-natural-import-path-parser-runtime-test-candidate`，结论 `go`。
2. 真实用户流通过：授权小样本 path extraction -> natural import -> alias -> same-session retrieval -> evidence IDs -> citation。
3. 安全边界通过：无 secret / raw path / file content 输出；无 NAS scan；无 repair / cleanup / backfill / reindex / delete / migration / rollout；无手动 DB/index 写入。
4. Freeze checklist 已更新：`phase2_114_final_user_flow_acceptance=go`，`final_complete_user_flow=go`。
5. 下一步：进入 Phase 2 stable MVP closeout / Phase 3 known-gap carryover；不要继续扩 Phase 2 功能。

## Phase 2.114a Natural Import Path Parser Fix

1. Codex A 已完成 parser-only runtime fix：中文 prompt 中 `文件路径：/Users/...xlsx。` 可正确提取授权绝对路径。
2. 支持中文路径、未加引号路径、路径父目录空格、同 prompt alias / project context。
3. 多路径仍 fail-closed，不支持本阶段多文件导入；普通 retrieval / path inspection prompt 不误触发 import。
4. 验证通过：Hermes 主仓库 py_compile；natural import parser / flow / runtime tests `54 passed`。
5. Runtime test-candidate 已推送：Hermes 主仓库 commit `c8ed29a83c441f58939f64b6b175ae4cac980ea3`，tag `phase-2.114a-natural-import-path-parser-runtime-test-candidate`。
6. 下一步：测试机 / OpenWebUI / 8642 复跑 Phase 2.114 final user-flow acceptance。

## Phase 2.113a Self-Awareness Review Fix

1. Codex A 已完成 Codex B review fix：收窄 fuzzy file-discovery trigger，普通“找字段 / 找内容”查询不再 suppress retrieval。
2. 明确找候选文件的 query 仍保持 fail-closed：无安全候选时返回 `file_discovery_no_safe_candidate`，不靠普通 retrieval 猜文件。
3. self-awareness trigger 已扩展到更自然的“管理文件 / 管理公司文件 / 使用记忆库”问法。
4. 验证通过：Hermes 主仓库 py_compile；`tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_natural_file_import_runtime.py` 为 `102 passed`。
5. 当前仍未 baseline；下一步必须 Codex B review，通过后再交 Codex C / 测试机验证 OpenWebUI / 8642 用户侧表现。

## Phase 2.113 Hermes Memory Self-Awareness / Kernel Activation

1. 当前新增 P0 blocker：Hermes 用户侧还没有可靠激活自己的 Hermes_memory / workspace / retrieval / evidence kernel 自我认知。
2. 该问题会让 Hermes 退化为“普通聊天助手 + 外置记忆库”，偏离企业内核级 Agent PRD 目标。
3. Codex A 下一步必须实现最小 runtime fix：能力说明、自然导入成功反馈、自动/推荐别名、模糊找文件候选、低敏 memory/workspace 边界。
4. 验收必须证明：Hermes 会说“文件已导入/记下，别名是 @xxx”，能用 safe alias 继续检索，并在多候选时要求用户确认。
5. 继续禁止：raw path / raw content / secret 写 memory，memory metadata 当 evidence，DWG/RVT/BIM 内容 overclaim，NAS full scan，DB CRUD，production rollout。
6. Phase 2 full completion 继续 blocked；2.113 修复后仍需 Codex B review 与测试机 / 8642 验证。

## Phase 2 Natural Import Closeout Review / Freeze Checklist Update

1. 已把 Phase 2.112i 测试机 Go 结果写入 closeout / freeze checklist：natural-language import usability = `passed_with_scope`。
2. 已明确 accepted scope：授权小 `.xlsx`、8642 / OpenWebUI-compatible backend、显式 `@建筑类数据样表`、same-session retrieval evidence、citation、无第三文件污染。
3. 仍未声明 production-ready：NAS full scan、DWG/RVT/BIM content、large-file parser/indexing、automatic memory write、repair/reindex/cleanup automation 均继续排除。
4. Phase 2 full completion 仍不能宣布；剩余 PRD/Roadmap P0/P1 缺口需继续保留或显式重分类。
5. 下一步：Codex B review 本轮 docs / eval manifest diff，通过后再做 selective baseline。

## Phase 2.112i Test-machine Retrieval Backend Environment Fix

1. Phase 2.112h alias gate 已通过：测试机已证明 explicit requested alias `@建筑类数据样表` 能保存并 follow-up `alias_resolved`。
2. 当前 blocker 转为 retrieval backend 环境：`retrieval_backend_failed_postgres_hostname_unresolved` / DB 服务不可达。
3. 不要把开发机本地 8000/8642 监听状态当成测试机最终结论；当前可信 blocker 是测试机 retrieval backend `postgres` hostname unresolved。
4. 下一步必须修复测试机 Hermes_memory API 的 DB hostname / network 配置；不得继续打回 alias parser / continuity 代码。
5. 已完成：测试机修复 8642 后端访问 Hermes_memory retrieval backend 的运行环境后，follow-up retrieval + citation 通过。
6. 下一步：进入 Phase 2 closeout / freeze checklist 更新，把自然语言导入小型授权 `.xlsx` 验收项标记为 passed-with-scope。

## Phase 2.112h Explicit Natural Import Alias Preservation Fix

1. 打回 2.112g：测试机已确认 2.112g 部署并重启，但导入阶段绑定的 alias 不是用户指定的 `@建筑类数据样表`。
2. 新 blocker：explicit alias import 只 partial；follow-up 请求用户指定 alias 仍 `alias_missing=true`、`retrieval_suppressed=true`。
3. Codex A 下一轮必须聚焦 natural import alias parsing / preservation；不得扩大到 ordinary memory、global alias、平台代码或真实导入。
4. 验收必须证明常见自然语言 alias 表达都能解析，且 requested alias 优先于 generated alias。
5. Phase 2 natural import closeout 仍 blocked，直到测试机真实 retrieval evidence + citation 通过。

## Phase 2.112g Header-only Stable Owner Restore Fix

1. development-machine 最小修复已完成：gateway stable owner fallback 支持 header-only `X-Hermes-Session-Id`。
2. accepted import turn 与 follow-up header-only 请求会生成同一 safe owner，并可恢复 imported alias 的 scoped document/version filters。
3. 验证：py_compile 通过；新增 gateway targeted tests `3 passed`；natural import / upload client / session scope regression `109 passed`。
4. Codex B review 已通过；runtime test-candidate 已推送：Hermes agent commit `20d9fb561`，tag `phase-2.112g-header-owner-restore-runtime-test-candidate`。
5. 注意：完整 `tests/gateway/test_api_server.py` 在当前主仓 `.venv` 因缺 async pytest 插件 false-fail existing async tests；后续可在具备 async 插件环境复核。
6. Phase 2 natural import closeout 仍 blocked，直到测试机真实 retrieval evidence + citation 通过。

## Phase 2.112f Alias Continuity Restore Fix

1. 测试机 Phase 2.112e 真实 OpenWebUI / 8642 验收仍 Pause：导入阶段 `alias_bound` 且 `alias_continuity_status=stored`，但 follow-up `@建筑类数据样表` 仍返回 `alias_missing=true`、`retrieval_suppressed=true`。
2. 已确认 `X-Hermes-Session-Id` 存在，import owner source 为 `gateway_session_key`，不是单纯缺少 stable owner header。
3. 当前 root cause category：`hermes_alias_store_restore_bug`。
4. Codex A 下一轮必须修复 follow-up alias-missing 分支的 owner-scoped continuity restore，并补齐 sanitized `alias_continuity_*` diagnostics。
5. 继续禁止 alias-global restore、ordinary memory alias persistence、DB/index writes、NAS scan、repair/reindex/rollout。
6. Phase 2 natural import closeout 仍 blocked，直到测试机证明 `@alias` retrieval evidence + citation 通过。

## Phase 2.112e API Server Stable Owner Bridge Fix

1. Codex A 已完成 API server stable owner bridge，Codex B review 通过。
2. 已接受 owner source：`X-Hermes-Session-Id`、`X-OpenWebUI-Conversation-Id`、`X-OpenWebUI-Chat-Id`、`X-Conversation-Id`。
3. 无 stable owner 时仍 fail-closed，输出 sanitized `stable_owner_missing`；不得恢复 alias-global registry。
4. 已验证：py_compile；API server owner bridge targeted tests `7 passed`；natural import / upload client / session scope regression `106 passed`。
5. Hermes agent runtime test-candidate 已推送：commit `091fd7414`，tag `phase-2.112e-api-server-owner-bridge-runtime-test-candidate`。
6. 下一步：测试机 Codex checkout tag，重启 8642，执行真实 OpenWebUI natural import -> `@alias` retrieval + citation 验收。

## Phase 2.112d Alias Continuity Scope Review Fix

1. Codex A 已完成 owner-scoped continuity 小修：`@alias` continuity 不再按 alias 全局恢复，而是按 safe owner key + alias 恢复。
2. Stable owner 使用哈希化 key；diagnostics 只输出 `alias_continuity_owner_source`，不暴露 raw gateway/session value。
3. 无 stable owner 时 fallback 为 process-local / non-persistent；新 store load 不会恢复 unscoped fallback alias。
4. 已补 TTL/stale cleanup；过期 continuity 不恢复，返回 `alias_continuity_status=expired` 并 suppress retrieval。
5. 冲突候选继续 fail-closed 并 suppress retrieval，safe candidates 不含 raw path/token/owner。
6. 验证通过：py_compile；natural import / upload client / session scope regression `105 passed`；gateway latest-user drift targeted test `1 passed`。
7. 下一步：Codex B review Phase 2.112d；通过后再考虑 runtime test-candidate tag 与测试机 OpenWebUI / 8642 复验。

## Phase 2.112c OpenWebUI Alias Continuity Fix

1. Codex A 已完成 runtime fix：natural import 成功后写入 bounded alias-continuity registry；follow-up api session drift 仍可用 `@alias` 恢复 imported `document_id/version_id` scoped retrieval。
2. 冲突策略：同 alias 出现多个 document/version 候选时 fail-closed，suppress retrieval，并只输出安全候选供用户澄清。
3. diagnostics 已补：`alias_continuity_status`、`alias_continuity_source`、`api_session_key_source`、`history_message_count`；raw path / import diagnostics 不作为 evidence。
4. 开发侧验证通过：py_compile，natural import / upload client / session scope regression `102 passed`，gateway latest-user drift test `1 passed`。
5. 下一步必须 Codex B review；通过后才允许 selective test-candidate baseline / tag，并交测试机复验真实 OpenWebUI / 8642 `@alias` retrieval + citation。
6. Phase 2 full closeout 仍 blocked，直到真实验收通过。

## Phase 2.112b Natural Import Alias Binding / Retrieval Blocker

1. Codex A 已完成 Phase 2.112b 最小 runtime fix：同一 OpenWebUI conversation history 可从上一轮 natural import diagnostics 恢复 alias；已存在导入 alias 的 title rebind 不再因 title resolver miss 失败。
2. 已覆盖 `alias_bind_failed`、follow-up `alias_missing=true`、`retrieval_suppressed=true` 的 blocker 测试；主仓 targeted regression `99 passed`。
3. Hermes agent runtime test-candidate 已推送：commit `1d02a7918`，tag `phase-2.112b-natural-import-alias-runtime-test-candidate`。
4. 测试机 Codex 与 Codex C 分工保持不变：测试机 Codex 跑真实 OpenWebUI / 8642；Codex C 只做开发机测试代码 / 验证支持。
5. 下一步由测试机 Codex 只重跑 alias + retrieval + citation 验收；不要重复无关真实导入。
6. 验收通过前不得 final baseline Phase 2.112，也不得宣布 natural import closeout。

## Phase 2.112 Codex B Review / Codex C Validation

1. Codex B review 已通过 Phase 2.112 实现，targeted tests 复跑 `97 passed`。
2. 下一步必须执行真实 OpenWebUI / 8642 验收：explicit alias、auto alias、same-session retrieval citation、bounded fuzzy discovery。
3. 验收通过前不得宣布 natural import usability closeout，也不得 baseline Phase 2.112。
4. 注意排除主仓无关 dirty：`uv.lock`、Phase 2.11e repo hygiene 文档、adapter reload test。


## Phase 2.112 Natural Import Workspace Retrieval Fix

1. Codex A 已完成 Phase 2.112 最小实现，等待 Codex B review。
2. 已修复：natural import 成功后 alias 从 `alias_seeded` 持久化为 `alias_bound`，并可在同 session 用 `@alias` 解析到 imported `document_id/version_id`。
3. 已补：无显式 alias 时自动生成安全 alias；文件发现只在 session alias 范围内返回候选并抑制普通 retrieval。
4. 已验证：主仓 py_compile 通过，natural import / upload client / session scope targeted tests `97 passed`。
5. 未完成：真实 OpenWebUI / 8642 natural import -> same-session retrieval citation 验收；global workspace metadata discovery 后置。
6. Phase 2 closeout 继续 blocked，直到该项通过 Codex B review 与 Codex C 真实验收。


## Phase 2.111 Codex B Review

1. Phase 2.111 natural import closeout pack 已通过 Codex B review。
2. 验证已通过：`git diff --check`、matrix JSON parse、evidence template py_compile、目标 pytest `14 passed`、latest JSON parse / ignore check。
3. 当前可 baseline：`docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`、`eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json`、`docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md` 与阶段文档。
4. full Phase 2 closeout 仍未完成；仍需要 future accepted Hermes CLI natural-language import smoke，或用户显式例外。
5. baseline 后不要自动执行 Codex C smoke；必须等待用户给出具体小型非敏感文件、alias 与项目上下文授权。

## Phase 2.110 Phase 2 Full Closeout Return Plan

1. 当前进入 Phase 2.110，目标是正式打回完整 Phase 2 closeout，而不是否定稳定平台 baseline。
2. 当前真实自然语言使用流程：受控 operator / API / CLI / checklist 可用；完全产品化的一句话自动导入 / 入库 / 建别名 / 连续查询尚未达标。
3. 已新增 `docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md` 与 `eval/phase2_inventory/phase2_full_closeout_return_checklist.json`。
4. 当前可保留：平台 read-only catalog-only 稳定集成、Hermes 独立企业 Agent 内核定位、DB/NAS catalog-only 契约、小批 NAS scratch / parser dry-run 边界、标书/会议/Excel/PPTX controlled MVP 证据边界。
5. 当前必须打回：full Phase 2 PRD / Roadmap closeout。不得宣布 Phase 2 完整完成。
6. 下一步：优先做 Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack，明确哪些缺口必须补证、哪些需要用户显式移到 backlog / Phase 3+。

## Phase 2.109 Phase 2 Final Freeze Checklist

1. 当前进入 Phase 2.109，目标是最终冻结检查，不做 runtime 实现。
2. 结论必须保持三段式：平台稳定集成 freeze=`go`；Hermes 独立内核保留=`go`；完整 Phase 2 PRD / Roadmap closeout=`pause`。
3. 已新增 `docs/PHASE2109_PHASE2_FINAL_FREEZE_CHECKLIST.md` 与 `eval/phase2_inventory/phase2_final_freeze_checklist.json`。
4. 仍未关闭的 full closeout gap：PRD 100+ / Roadmap 300+ eval、Top5 / citation target-scale metrics、structured fact spot-check、tender deep fields、full RBAC/ABAC、version diff、knowledge admin / human validation、natural import usability。
5. 下一步：Codex B review Phase 2.109；通过后 selective baseline。不得声称 full Phase 2 closeout。

## Phase 2.108 Standalone Kernel Freeze Contract

1. 当前进入 Phase 2.108，目标是补齐 Phase 2 收口前的 standalone Hermes kernel freeze contract。
2. 核心判断：平台 catalog-only / Gateway 只读是安全表面，不是 Hermes 产品上限；Hermes 脱离平台仍应保留企业 Agent 内核定位。
3. 已新增 `docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md`。
4. Phase 2 验收新增：Hermes 自有 workspace、session/context、memory/evidence/retrieval、文件治理和后续 NAS governance 路线必须被保留。
5. 当前仍不进入 runtime 实现、不连接平台/DB/NAS、不写 memory/index/object-store、不进入 production rollout。
6. 下一步：Codex B review Phase 2.108；通过后 selective baseline。不得把 stable platform tag 写成 full Phase 2 closeout。

## Phase 2 Stable Hermes Platform Baseline Tag

1. Phase 2.107 baseline 已完成并推送：commit `3ef3966`，tag `phase-2.107-minimal-freeze-blocker-closure-baseline`。
2. 平台 0B Gateway hardening controlled live smoke 已回传 `Go`：`EXPECT_HERMES_AGENT_AVAILABLE=true`，`PASS=14 FAIL=0`。
3. 稳定平台集成 tag：`phase-2-stable-hermes-platform-integration-baseline`。
4. 当前稳定范围：catalog-only asset query、Gateway permission / redaction、Missing Evidence、安全 IDs / traces、authorityHealth.orange、responseId/queryId/traceId、safeMemoryCandidates=[]、sanitizedContextRefs=[]。
5. 当前不是 production rollout，不是 Phase 2 full PRD/Roadmap closeout，不是 Phase 3 transition。
6. known risk：native session/thread lifecycle、Evidence Layer、Memory runtime、target-scale metrics、natural import usability 仍后置或需业务决策。
7. 下一步：创建并推送 stable tag；测试机 checkout stable tag 后再决定 Phase 2 freeze 后续。

## Phase 2.107 Minimal Freeze Blocker Closure Plan

1. 当前 Phase 2.107 docs / matrix 内容已实现，目标是把 stable Hermes 冻结前的 blocker 做成最小 closure matrix。
2. Phase 2.106 baseline 已完成：commit `fe2706d`，tag `phase-2.106-platform-stable-hermes-freeze-readiness-baseline`，pushed=true。
3. 已新增 `docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md` 与 `eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json`。
4. 最新 Platform / DB Agent alignment report 已纳入：当前平台接入 `architecture_authority_health=orange`，仍有 OpenAI-compatible plugin-mode 风险，但 Gateway 安全边界接近 green。
5. 最小 stable-tag blocker set：平台身份/权责 wording、Gateway 权限与 path redaction、catalog-only safe refs、Missing Evidence、shared contract sync、test-machine update、0B Gateway hardening、high-risk forbidden-field fail-closed、authority health orange、前端文案收束。
6. 可带风险冻结：runtime session refs、Evidence Layer、Memory runtime、target-scale metrics；但 session/thread 风险只能在 0B Gateway 明示 `authority_health.orange` 与 placeholder fields 后冻结。Phase 3+ 后置 production rollout、full Data Steward、Agent DB CRUD/SQL、NAS semantic collection。
7. 下一步：Codex B review Phase 2.107；通过后由用户显式授权 docs / matrix baseline。不得自动创建 stable tag 或进入 Phase 3。

## Phase 2.106 Platform Stable Hermes Freeze Readiness

1. 当前 Phase 2.106 docs / checklist 内容已实现，目标是形成可供平台稳定嵌入的 Hermes Phase 2 冻结基线。
2. 已新增 stable Hermes freeze readiness 文档、platform capability baseline、测试机更新 prompt 与 freeze checklist JSON。
3. 冻结目标是 `Phase 2 Stable Hermes for Platform Integration`，不是声明 Phase 2 全部 PRD / Roadmap 指标已完成。
4. 冻结范围优先保证：catalog-only asset query、Gateway permission / redaction、Missing Evidence、安全 IDs、query / trace、共享契约、Hermes 内核权责边界。
5. 不进入冻结范围：production rollout、DWG/RVT/BIM 内容理解、NAS semantic collection、Agent DB CRUD、Agent SQL、自动 repair/reindex/cleanup、full Data Steward productization、Phase 2 full closeout。
6. 下一步：Codex B review Phase 2.106；通过后由用户显式授权 docs / checklist baseline。不得自动进入 Phase 2.107 或 Phase 3。

## Phase 2.105 Hermes Kernel Authority / Platform Alignment Contract

1. 当前进入 Phase 2.105，目标是立刻通过文档把 Hermes 与平台边界对齐，防止 Hermes 被做成平台内的单轮智能问答插件。
2. 已完成 Phase 2.104d baseline：commit `f0fabc4`，tag `phase-2.104d-feedback-scoring-linkage-contract-baseline`，pushed=true。
3. 已新增 `docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`、`docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md`、`eval/phase2_inventory/hermes_platform_authority_alignment_examples.json`。
4. 已明确：Hermes 是企业 Agent 内核，负责 session continuity、reasoning state、tool orchestration、evidence / Missing Evidence、memory continuity；平台负责 UI、Gateway、permission proof、project_scope、path redaction 与 platform audit。
5. Data Steward / Catalog 只是 Hermes 的一个能力模块，不是 Hermes 全貌；平台不得把 Hermes 降级为路径问答 AI 或 catalog-only 插件。
6. 下一步：Codex B review Phase 2.105；通过后由用户显式授权 docs / fixture baseline。本阶段不跑 Codex C 真实终端验收。

## Phase 2.104d Feedback / Scoring Linkage Contract Planning

1. 当前进入 Phase 2.104d，目标是规划 feedback 如何安全进入 eval inventory、offline scoring pack 与 issue intake。
2. 已新增 `docs/PHASE2104D_FEEDBACK_SCORING_LINKAGE_CONTRACT.md` 与 `eval/phase2_inventory/feedback_scoring_linkage_examples.json`。
3. feedback 只能作为 evaluation / triage signal；不能直接成为 facts、content evidence、permission proof、memory evidence、repair 或 official metric pass。
4. 允许标签需包括 helpful、wrong_document、missing_evidence、wrong_boundary、citation_problem、permission_problem、overclaim、needs_human_review、irrelevant_result。
5. 禁止在 feedback linkage 中保存 raw user note、raw answer text、raw path、raw DB/catalog row、secret、token 或客户敏感材料。
6. 下一步：Codex B review Phase 2.104d；通过后由用户显式授权 docs / fixture baseline。本阶段不跑 Codex C 真实终端验收。

## Phase 2.104c Governed Document Evidence Search Contract Planning

1. 当前进入 Phase 2.104c，目标是规划 future-only `document_evidence_search` contract，解决 Hermes 从 catalog-only 走向 governed evidence retrieval 的接口边界。
2. 已新增 `docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md` 与 `eval/phase2_inventory/document_evidence_search_contract_examples.json`。
3. 当前仍不能实现或声称已支持 `document_evidence_search`；本阶段只定义 future request / response / gate / citation / Missing Evidence 合同。
4. 正文回答必须同时满足当前平台权限、Evidence Availability 允许、citation-bearing governed evidence 三个条件。
5. catalog-only、parser-required、unsupported、permission-denied、memory-reference-only 均不能回答正文内容，必须走 Missing Evidence 或安全拒绝。
6. 下一步：Codex B review Phase 2.104c；通过后由用户显式授权 docs / fixture baseline。本阶段不跑 Codex C 真实终端验收。

## Phase 2.104b Low-sensitive Memory Continuity + Permission Boundary Contract

1. 已新增 `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md`，拆清 Platform permission、catalog permission decision 与 Hermes memory continuity reference 三层边界。
2. 已新增 `eval/phase2_inventory/memory_continuity_permission_examples.json`，包含 8 条 sanitized fixture examples。
3. 当前唯一权威授权来源必须是 Platform / Gateway permission proof；Hermes memory 只能保存低敏引用，不能授权、不能绕过 denial、不能成为 content evidence。
4. 允许低敏 memory 字段仅限 related IDs、query/trace IDs、feedback label、偏好/分组/上次 evidence mode 等 UX continuity metadata。
5. 禁止把 raw path、raw row、正文内容、DWG/RVT/BIM 内容、客户敏感 note、secret、permission proof token 或未授权 ACL snapshot 写入 Hermes memory。
6. 下一步：Codex B review Phase 2.104b；通过后由用户显式授权 docs / fixture baseline。不得自动进入 Phase 2.104c。

## Phase 2.104a Evidence Availability Contract Docs + Fixtures

1. 已新增 `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md`，定义 Evidence Availability Contract 状态枚举、字段要求、安全规则和 Missing Evidence 语义。
2. 已新增 `eval/phase2_inventory/evidence_availability_contract_examples.json`，包含 7 条 sanitized fixture examples。
3. 状态枚举：`catalog_only`、`parser_required`、`evidence_indexed`、`unsupported_type`、`permission_denied`、`manual_review_required`。
4. fixtures 使用 fake IDs，不包含真实项目名、文件名、NAS 路径、storage path、raw row、asset_uid、source_id、secret 或业务敏感内容。
5. 当前仍不能把 `evidence_indexed` 解释为平台已开放 `document_evidence_search`；它只是 future authorized evidence-search path 的 contract state。
6. 下一步：Codex B review Phase 2.104a；通过后由用户显式授权 docs / fixture baseline。不得自动进入 Phase 2.104b。

## Phase 2.104 Platform Layered Capability Plan

1. 已新增 `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`，把平台接入能力拆为 `Catalog Layer -> Evidence Layer -> Memory Layer -> Orchestration Layer`。
2. 当前可用层仍仅为 Catalog Layer：只读资产目录、安全 file/model IDs、permission decision、Missing Evidence、query/trace IDs。
3. Evidence Layer / Memory Layer / Orchestration Layer 均保持 next / future，不得写成 current runtime capability。
4. 设计已明确后续 contract：Evidence Availability、future `document_evidence_search`、low-sensitive Memory Continuity、Feedback、Capability Response。
5. 共享 `DigitalDeliveryProject` 已核对：`agent-briefings/hermes_capability_handoff.md` 与 `docs/01_capability_matrix.md` 已包含 Hermes layers 相关条目；本阶段未修改共享文件。
6. 下一步：Codex B review Phase 2.104；通过后由用户显式授权 docs baseline。不得自动进入 Phase 2.104a 实现。

## Phase 2.103 Test Machine Update + Hermes Capability Maximization Handoff

1. Phase 2.102b baseline 已完成：commit `5c37661`，tag `phase-2.102b-metric-scoring-pack-baseline`，pushed=true。
2. 已新增 `docs/PHASE2103_TEST_MACHINE_UPDATE_AND_CAPABILITY_HANDOFF.md`、`docs/CODEX_TEST_MACHINE_UPDATE_TO_PHASE2102B_PROMPT.md`、`docs/DB_TEAM_HERMES_CAPABILITY_MAXIMIZATION_HANDOFF.md`。
3. 已明确数据库 / 平台团队口径：Hermes 不是普通对话 Agent，而是证据优先、权限闭环、Missing Evidence 驱动的企业记忆内核。
4. 当前可最大化接入：只读 catalog search、安全 file/model IDs、query/trace IDs、permission decision、Missing Evidence、feedback、low-sensitive related_file_ids memory。
5. Phase 2.103a 已修复 `existing memory evidence` 含混表述；low-sensitive memory references 不是 content evidence，`related_file_ids` 不代表 Hermes 已读取文件正文。
6. 当前不可接入为 current：Agent DB CRUD、Agent SQL、NAS scan、DWG/RVT/BIM 内容理解、NAS semantic index、production rollout。
7. 下一步：Codex B re-review Phase 2.103a；通过后由用户显式授权 selective docs baseline。

## Phase 2.102b Metric Scoring Pack

1. Phase 2.102a baseline 已完成：commit `0ee07f5`，tag `phase-2.102a-eval-inventory-manifest-baseline`，pushed=true。
2. 已新增离线 metric scoring pack：`scripts/phase2102b_metric_scoring_pack.py`、`tests/test_phase2102b_metric_scoring_pack.py`、`docs/PHASE2102B_METRIC_SCORING_PACK.md`。
3. Scorer 只计算 `metric_eligible=true` cases 的 Top5 / citation rates，并输出 missing results、excluded cases、forbidden behavior summary；ineligible cases 不进 denominator，但其中任何 forbidden behavior 仍会 block review。
4. 已固定安全边界：不运行 API / CLI / Gateway / DB / NAS smoke，不连接真实系统，不读 raw rows / NAS paths / storage paths / secrets，不写 DB/index/object-store/memory。
5. 当前 19-case inventory 不满足 PRD 100+ 或 Roadmap 300+；Phase 2 closeout readiness 仍为否。
6. 下一步：Codex B re-review Phase 2.102b；通过后由用户显式授权 selective baseline。

## Phase 2.102a Eval Inventory Manifest

1. Phase 2.102 baseline 已完成：commit `a5c1490`，tag `phase-2.102-metric-evaluation-evidence-pack-baseline`，pushed=true。
2. 已新增 `eval/phase2_inventory/phase2_eval_inventory_manifest.json` 和 `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`，建立稳定 question IDs / groups / expected evidence / citation expectations / metric eligibility。
3. 当前 starter inventory：19 accepted cases、15 metric-eligible cases、4 metric-ineligible cases，覆盖 12 个 required groups。
4. 本阶段未计算 Top5 / citation accuracy，未声称 PRD 100+ 或 Roadmap 300+ 已满足。
5. 仅使用 committed docs/tests 作为 evidence refs，未读取 ignored reports、raw DB rows、NAS paths、secrets 或 private run records。
6. 下一步：Codex B review Phase 2.102a manifest；通过后由用户显式授权 selective docs/data baseline。


## Phase 2.102 Metric / Evaluation Evidence Pack

1. Phase 2.101 baseline 已完成：commit `5f15852`，tag `phase-2.101-prd-acceptance-gap-closure-plan-baseline`，pushed=true。
2. 已新增 `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`，集中映射 PRD / Roadmap 中 eval count、Top5、citation accuracy、fact spot-check、permission denial、parser/source coverage、Gateway、Data Steward、Mac mini / employee trial、natural import 等证据。
3. Evidence taxonomy 已固定为：`measured_pass`、`measured_fail`、`partial_evidence`、`smoke_only_not_metric`、`missing_metric`、`requires_user_decision`。
4. 当前结论：Phase 2 metric closeout decision=`not_ready`；PRD 100+ / Roadmap 300+、Top5 80/85、citation 85/90、structured fact manual spot-check 90 均缺 committed numerator / denominator。
5. 本阶段 docs-only；未读取 ignored real reports、raw DB rows、NAS paths、secrets 或 private run records，未运行 API/CLI/Gateway/DB/NAS smoke，未改代码、未写 tests、未进入 rollout。
6. 下一步：Codex B review Phase 2.102 evidence pack；通过后由用户显式授权 selective docs baseline。


## Phase 2.101 PRD Acceptance Gap Closure Plan

1. Phase 2.100a baseline 已完成：commit `8456979`，tag `phase-2.100a-phase2-boundary-audit-baseline`，pushed=true。
2. Phase 2.101 已新增 `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`，把 audit 中的 partial / not_started / user_decision_required 项转成 gap closure decision table。
3. 当前分类包括：`phase2_closeout_blocker`、`phase2_evidence_pack_required`、`phase2_backlog_candidate_user_decision`、`phase3_plus_candidate_user_decision`、`already_satisfied_keep_evidence`。
4. 重点待决策缺口：结构化实体关系、structured fact extraction 口径、tender deep fields、version diff、incremental delete/invalidation、部门/项目/密级权限、反馈闭环、eval metrics、知识管理员/人审、parser/source evidence、Mac mini / employee trial、自然语言导入、Gateway、Data Steward。
5. 本阶段未实现功能、未运行 smoke、未连接 DB/NAS/API/Gateway、未进入 Phase 3、未声明 Phase 2 closeout readiness。
6. 下一步：Codex B review Phase 2.101；通过后由用户显式授权 selective docs baseline。


## Phase 2.100a Phase 2 / Phase 3 Boundary Acceptance Audit Coverage Fix

1. 已新增 `docs/PHASE2100_PHASE2_PHASE3_BOUNDARY_ACCEPTANCE_AUDIT.md`，形成 PRD / Roadmap / Technical Design / acceptance matrix traceability audit。
2. Codex B review 发现覆盖 blocker：PRD §13 MVP 验收未逐项入矩阵，Data Steward / BIM Phase 2 试点边界与 Phase 3+ 产品化边界需拆分，retrieval quality dashboard / automatic eval pipeline 需明确，文档重复段落需清理。
3. Phase 2.100a 已补入 PRD §13 显式矩阵行、Data Steward split、eval/dashboard rows，并清理 confusing duplicate boundary sections。
4. 当前结论：Phase 2 closeout readiness=否；不能因为 micro-phase count 到 100 就进入 Phase 3 或 final closeout。
5. Phase 2.101 建议优先做 PRD acceptance gap closure plan，先决定哪些缺口必须 Phase 2 关闭前完成，哪些需要用户明确重分类到 backlog / Phase 3+。
6. 当前不进入 runtime implementation、repair、rollout、DB/API/NAS/Gateway smoke 或 Phase 3。

## Data Steward / NAS Catalog-only Risk Boundary

1. 已采纳 `hermes_agent_risk_notes.md` 中值得进入主线的建议，并固化为 `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`。
2. 项目内企业 Agent 正式名称统一为 **Hermes**，不使用 Jarvis 作为正式称呼。
3. 后续 Data Steward / DB / NAS / 前端耦合必须遵守：catalog metadata 不等于正文 evidence；Hermes memory 不等于 NAS 内容索引；只读 Catalog Tool 不等于 SQL Tool。
4. 当前仍禁止把 catalog rows、真实 `storage_path`、DWG / RVT 内容、NAS 文件正文或 raw row 写入 `documents/chunks/Qdrant/OpenSearch` 或 Hermes long-term memory。
5. 后续 prompt / tool description / 前端文案需要避免承诺 DWG / RVT 内容理解、BIM 构件级搜索、NAS 全文搜索或 NAS 语义搜索。

## Phase 2.97 Frontend Gateway Read-only Trial Runbook

1. Phase 2.96 baseline 已完成：commit `6fff43f`，tag `phase-2.96-gateway-controlled-smoke-result-review-baseline`，pushed=true。
2. 已新增 `docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md`，定义 limited internal frontend trial runbook / operator checklist。
3. Runbook 明确 allowed endpoints、allowed query types、forbidden-field scan、side-effect checklist、Go/Pause/No-Go、feedback capture 与 escalation rules。
4. 本阶段未执行真实 Gateway smoke，未连接 DB/NAS/API，未实现 Gateway code，未运行 parser/writer，未写 index/object-store，未进入 rollout。
5. Codex B review 已通过；下一步只做 Phase 2.97 selective docs baseline。

## Phase 2.98 Digital Delivery Standard Agent Boundary Review

1. Phase 2.97 baseline 已完成：commit `05e7275`，tag `phase-2.97-frontend-gateway-readonly-trial-runbook-baseline`，pushed=true。
2. 已新增 `docs/PHASE298_STANDARD_AGENT_BOUNDARY_REVIEW.md`，记录共享数字化交付标准 v0.1 的 Hermes Agent 回答边界评审。
3. Review 结论：标准 v0.1 可作为 catalog-only answer boundary basis，但不得被当作 DWG/RVT/BIM 内容理解能力证明。
4. 已记录 `R001-R043` rule grouping、DWG/RVT/BIM Missing Evidence 边界、permission/path/conflict safety、overclaim risks 与标准化回答模板。
5. 本阶段未改代码、未改数据库、未连接 DB/NAS/API、未运行 Gateway smoke、未修改共享文档、未进入 rollout。
6. Codex B review 已通过；下一步只做 Phase 2.98 selective docs baseline，不自动进入 Phase 2.99。

## Phase 2.99 Standard Boundary Prompt / Tool Description Alignment

1. Phase 2.98 baseline 已完成：commit `40f71b9`，tag `phase-2.98-standard-agent-boundary-review-baseline`，pushed=true。
2. 已新增 `app/services/asset_catalog/standard_answer_boundary.py`，提供纯 Python 标准回答边界分类与模板。
3. 已覆盖 DWG/RVT/BIM/PDF/Office Missing Evidence、`current-lineage` 限定语、`A004-A010` lineage-only 口径、memory 低敏引用边界。
4. Phase 2.99a 已补 `docx` / `xlsx` 正文类问题回归；Office extension content questions 统一要求 `full_text_evidence`。
5. 已新增 `docs/PHASE299_STANDARD_BOUNDARY_PROMPT_TOOL_ALIGNMENT.md`。
6. 目标测试 `11 passed`；explicit probe 中 `docx/xlsx/pptx/pdf` 均返回 `missing_evidence ('full_text_evidence',)`。
7. 本阶段未连接 DB/NAS/API，未运行 Gateway smoke，未修改共享文档，未执行 parser/writer/scratch copy，未写 index/object-store/memory，未进入 rollout。
8. 下一步：Codex B review Phase 2.99a；通过后再做 selective baseline。

## Phase 2.96 Gateway Controlled Smoke Result Review

1. Phase 2.95 baseline 已完成：commit `3d70626`，tag `phase-2.95-shared-contract-alignment-baseline`，pushed=true。
2. 已新增 `docs/PHASE296_GATEWAY_CONTROLLED_SMOKE_RESULT_REVIEW.md`，审查最新 Frontend / Gateway controlled smoke `Go` 报告。
3. Review 结论：该 Go 只授权 read-only controlled Gateway smoke 通过；permission-denied fail-closed 与 catalog-only Missing Evidence / `asset_catalog_only` 是最重要的 passed gates。
4. 该 Go 不是 production rollout，不授权 Agent DB CRUD、Agent SQL、NAS scan/copy、parser/writer/index 写入、Agent answer integration、真实 `storage_path` 暴露或 DWG/RVT 内容理解。
5. Phase 2.96 baseline 已完成：commit `6fff43f`，tag `phase-2.96-gateway-controlled-smoke-result-review-baseline`，pushed=true。

## Phase 2.97 Frontend Gateway Read-only Trial Runbook

1. 当前进入 Phase 2.97 docs-only runbook planning。
2. 目标：创建内部受控前端 Gateway 只读试用 operator checklist，明确 allowed endpoints、safe fields、forbidden-field scan、side-effect checks、Go/Pause/No-Go 与 feedback capture。
3. 本阶段不运行真实 Gateway smoke、不连接 DB/NAS/API、不实现 Gateway code、不写 DB/index/object-store、不进入 rollout。
4. Codex A 应执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成后停止等待 Codex B review。

## Phase 2.95 Shared Contract Alignment

1. Phase 2.95 alignment 文档已完成，Codex B review 通过。
2. 下一步只做 Phase 2.95 selective docs baseline。
3. 实际 Frontend / Gateway controlled smoke 已按正常平台登录流程重跑并返回 `Go`；该 Go 仍需 Phase 2.96 正式审查。
4. Phase 2.96 应记录并审查该 Go 报告，确认其仍是 read-only controlled smoke，不是 production rollout。
5. 当前仍禁止 DB/NAS 写入、parser/writer/index 写入、Agent answer integration 或 rollout。

## Phase 2.95 Shared Contract Alignment

1. Phase 2.94a baseline 已完成：commit `712cd83`，tag `phase-2.94a-gateway-smoke-handoff-baseline`，pushed=true。
2. 已将共享文档空间 `DigitalDeliveryProject` 纳入 Hermes 主线契约维护流程。
3. 已新增 `docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md`，记录共享文件读取清单、Hermes 主责文件、同步触发条件、当前一致性结论与不一致项。
4. 当前 required shared contract 未发现 mismatch；本轮未修改共享空间文件。
5. 后续修改 Catalog Tool schema、Missing Evidence、memory 写入边界、`related_file_ids`、prompt/tool description、标准解释能力时，必须同步共享文档。
6. 本阶段不执行真实 Gateway smoke、不连接 DB/NAS/API、不改代码、不运行 parser/writer、不写 index/object-store、不 rollout。
7. 下一步：Codex B review Phase 2.95 alignment；通过后再做 selective docs baseline。

## Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack

1. Phase 2.94a handoff pack 已完成，Codex B review 通过。
2. 已新增 `docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`，用于后续单独授权的 Codex C / 数据库团队只读 controlled smoke。
3. Prompt 覆盖 endpoint matrix、safe fields、forbidden-field scan、permission-denied、catalog-only Missing Evidence / `asset_catalog_only`、Go / Pause / No-Go 与 final report template。
4. 该 prompt 不是 runtime authorization，不得自动执行真实 smoke。
5. 下一步只做 Phase 2.94a selective docs baseline；baseline 后再决定是否进入 Phase 2.94b / runtime smoke authorization。

## Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack

1. Phase 2.94 baseline 已完成：commit `b41bf9b`，tag `phase-2.94-frontend-gateway-smoke-plan-baseline`，pushed=true。
2. Phase 2.94a 已完成 docs-only handoff pack：新增 `docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`。
3. 交接 prompt 已包含 sanitized inputs、endpoint matrix、safe response fields、forbidden-field negative assertions、permission-denied、catalog-only Missing Evidence / `asset_catalog_only`、Go / Pause / No-Go 与 final report template。
4. 本阶段未执行真实 smoke、未连接 DB/NAS/platform API/Hermes API、未实现 Gateway code、未运行 parser/writer、未写任何 index/object-store、未进入 rollout。
5. 下一步：Codex B review Phase 2.94a handoff prompt；review 通过后才考虑 selective docs baseline。
6. 不得自动进入 Phase 2.94b 或真实 frontend / Gateway smoke。

## Phase 2.93 Read-only Gateway Implementation Review

1. Phase 2.92 baseline 已完成：commit `36de5a7`，tag `phase-2.92-readonly-gateway-acceptance-plan-baseline`，pushed=true。
2. 已完成 Phase 2.93：新增 `docs/PHASE293_READONLY_GATEWAY_IMPLEMENTATION_REVIEW.md`。
3. Review 结论：数据库团队“极小批次：Hermes 命名收束 + 只读 Gateway 前端复验”回传报告满足 Phase 2.92 P0 gates，decision=`go`，scope=`read_only_gateway_review_passed`。
4. 该结论不代表 production readiness，不授权 Gateway implementation、Agent DB CRUD、NAS scan、content ingestion 或 rollout。
5. P1 follow-up：Phase 2.94 应规划 frontend controlled smoke，覆盖 response schema sample、trace ids、safe identifiers、permission-denied copy、Missing Evidence / `asset_catalog_only` 与 forbidden-field negative assertions。
6. Codex B review 已通过；下一步只做 Phase 2.93 selective docs baseline，baseline 后再规划 Phase 2.94。
7. 当前仍禁止：Gateway code implementation、真实 DB 连接、平台 Gateway smoke、Agent DB CRUD、Agent SQL、NAS scan、parser、scratch copy、writer、index/object-store write、Agent answer integration、production rollout。

## Phase 2.94 Frontend Controlled Smoke Planning

1. Phase 2.93 baseline 已完成：commit `d84cb62`，tag `phase-2.93-readonly-gateway-implementation-review-baseline`，pushed=true。
2. 已新增 `docs/PHASE294_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PLAN.md`。
3. 规划覆盖 capabilities、health、chat、catalog search、compatibility route、permission-denied behavior、catalog-only content question。
4. 已固定未来 smoke 必查：Hermes naming、server-generated `project_scope`、Missing Evidence / `asset_catalog_only`、`query_id` / `trace_id`、`file_id` / `model_id` / `source_view`、`permission_decision`、forbidden fields 不泄露。
5. 已固定 Go / Pause / No-Go：任何 forbidden field、frontend-trusted `project_scope`、catalog metadata as content evidence、denied request leak、DB/index/object-store write、parser/NAS scan/rollout 都是 No-Go。
6. 默认不执行真实 Gateway smoke；若需要 runtime smoke，必须另行授权并保持 read-only。
7. Codex B review 已通过；下一步只做 Phase 2.94 selective docs baseline。

## Phase 2.92 Read-only Gateway Acceptance Planning

1. Phase 2.91 baseline 已完成：commit `cf89e1e`，tag `phase-2.91-runtime-evidence-writer-smoke-gate-baseline`，pushed=true。
2. 已新增 `docs/PHASE292_READONLY_GATEWAY_ACCEPTANCE_PLAN.md`，定义数据库平台 read-only frontend Gateway 接入 Hermes 的 P0 / P1 / P2 验收 gates。
3. 当前允许数据库团队继续：平台后端 Gateway、Hermes 前端入口、health / capabilities、read-only catalog metadata preview、server-side `project_scope` permission proof、Missing Evidence / catalog-only 展示。
4. 当前仍禁止：Agent DB CRUD、Agent 生成 SQL、前端直连 Hermes raw/internal endpoints、信任前端传入 `project_scope`、返回真实 `storage_path` / raw row / NAS path、DWG/RVT 内容理解、NAS scan、parser、scratch copy、writer smoke、index/object-store 写入、Agent answer integration、production rollout。
5. 数据库团队已回传初步实现报告：Hermes 命名收束、read-only Gateway endpoints、forbidden-field assertions、Missing Evidence / `asset_catalog_only` 行为、构建与专项脚本均通过；Hermes 侧暂定 provisionally go。
6. 下一步只做 Phase 2.92 selective docs baseline；baseline 后进入 Phase 2.93 review 数据库团队 Gateway implementation report。

## Phase 2.91 Runtime Evidence Writer Smoke Gate Implementation

1. Phase 2.90 baseline 已完成：commit `3ee37e3`，tag `phase-2.90-test-machine-preflight-readiness-baseline`，pushed=true。
2. 测试机 runtime preflight-only 已返回 `preflight_ready_for_operator_stop`，但这仍不是写入授权。
3. Phase 2.91 本地实现已完成：新增 runtime smoke gate service、CLI、target tests 与阶段文档。
4. 默认 gate-only，不写真实 DB；目标测试 / 临时注入 DB session 中可调用 `EvidenceOnlyWriter.write()` 验证 created counts、idempotency 与 rollback dry-run。
5. 验证通过：TDD RED 已观察；目标测试 `12 passed`；py_compile 通过；writer + preflight + smoke 组合回归 `29 passed`。
6. Codex B review 已通过；下一步执行 selective Git baseline。
7. 仍禁止真实 Hermes DB 写入、parser、scratch copy、NAS scan、OpenSearch / Qdrant / MinIO 写入、Agent answer integration、repair/reindex/rollout。

## Phase 2.90 Test-Machine Repository Update Gate

1. Phase 2.89 baseline 已完成：commit `4e0bd62`，tag `phase-2.89-test-machine-runtime-preflight-handoff-baseline`，pushed=true。
2. 测试机 repo update 已返回 `Go`：head `4e0bd62`，worktree clean，required docs present。
3. Runtime preflight-only 已返回 `Go`：decision state `preflight_ready_for_operator_stop`，output `phase289-runtime-preflight-report-001.json`。
4. 安全结果：writer 未调用、DB 未写入、parser 未运行、NAS 未扫描、index/object-store 未写入、Agent answer 未接入、未 rollout。
5. 当前仍不授权调用 `EvidenceOnlyWriter.write()`、真实 DB 写入、parser、NAS copy/scan、OpenSearch / Qdrant / MinIO 写入、Agent answer integration 或 rollout。
6. 下一步先做 Phase 2.90 selective docs baseline；之后再规划 Phase 2.91 first controlled writer smoke execution gate。

## Phase 2.89 Test-Machine Runtime Preflight Smoke Handoff

1. Phase 2.88 baseline 已完成：commit `b09c3d1`，tag `phase-2.88-runtime-evidence-write-preflight-baseline`，pushed=true。
2. Phase 2.89 docs-only / handoff-only package 已完成，Codex B review 通过。
3. 测试机 prompt 固定 reviewed ref `b09c3d1` / `phase-2.88-runtime-evidence-write-preflight-baseline`，只允许运行 `scripts/phase288_runtime_evidence_write_preflight.py`。
4. Handoff 明确 local ignored approval JSON、worktree status file、output report path、sanitized fields、Go/Pause/No-Go 与 `preflight_ready_for_operator_stop` 后强制停止。
5. 当前仍不授权 `EvidenceOnlyWriter.write()`、真实 DB 写入、parser、NAS copy/scan、OpenSearch / Qdrant / MinIO 写入、Agent answer integration、repair/reindex/rollout。
6. 下一步：只做 Phase 2.89 selective docs baseline，不自动执行测试机 prompt。

## Phase 2.88 Runtime Evidence Write Preflight Runner

1. Phase 2.87d baseline 已完成：commit `3b01b0f`，tag `phase-2.87d-runtime-evidence-write-execution-pack-baseline`，pushed=true。
2. Phase 2.88 首轮 implementation 已完成：新增 runtime evidence write preflight service、CLI、target tests、ignored report storage 与阶段文档。
3. Runner 读取 local operator approval JSON 与本地 sanitized prerequisite report refs，校验 required fields、expiry、test-machine env、scope limits、allowed write action、feature flags、idempotency key、write_run_id、payload fingerprint 与 git/worktree 状态。
4. 决策状态：`preflight_ready_for_operator_stop`、`preflight_pause`、`preflight_no_go`。
5. 本阶段未调用 `EvidenceOnlyWriter.write()`，未执行真实 DB write，未接 API / CLI runtime，未运行 parser，未复制文件，未写 OpenSearch / Qdrant / MinIO，未接 Agent answer，未启用真实写入 feature flags。
6. Codex B review 已通过；下一步只做 selective Git baseline，不自动进入 Phase 2.89 或真实 runtime smoke。

## Phase 2.87d Runtime Evidence Write Smoke Execution Pack Planning

1. Phase 2.87c baseline 已完成：commit `490b5ca`，tag `phase-2.87c-runtime-evidence-write-smoke-plan-baseline`，pushed=true。
2. Phase 2.87d docs-only / handoff planning 已完成。
3. 已新增 `docs/PHASE287D_RUNTIME_EVIDENCE_WRITE_EXECUTION_PACK.md` 与 `docs/CODEX_TEST_MACHINE_RUNTIME_EVIDENCE_WRITE_SMOKE_PROMPT.md`。
4. 交接包已覆盖 test-machine preconditions、reviewed refs、env key names、operator approval JSON path/schema、prior report refs、feature flags、one-run write boundary、preflight-only commands、stop points、sanitized report、rollback/idempotency checks 与 Go / Pause / No-Go。
5. 本阶段未执行 writer，未写真实 DB，未接 API / CLI runtime，未运行 parser，未复制文件，未写 OpenSearch / Qdrant / MinIO，未接 Agent answer，未启用真实写入 feature flags。
6. Codex B review 已通过；下一步只做 selective docs baseline，不执行测试机 prompt，不自动进入 Phase 2.88 或真实 runtime smoke。

## Phase 2.87c Controlled Runtime Evidence Write Smoke Planning

1. Phase 2.87b baseline 已完成：commit `44cc837`，tag `phase-2.87b-evidence-only-writer-baseline`，pushed=true。
2. Phase 2.87c docs-only planning 已完成，新增 `docs/PHASE287C_RUNTIME_EVIDENCE_WRITE_SMOKE_PLAN.md`。
3. 规划已覆盖 prerequisite chain、operator approval JSON、feature flags default-off、transaction / commit boundary、rollback dry-run、idempotency、post-write inspection、sanitized report、Go / Pause / No-Go 与 Codex C/test-machine validation prompt outline。
4. 本阶段未实现 API / CLI runtime wiring，未执行 writer，未写真实 DB，未运行 parser，未复制文件，未写 OpenSearch / Qdrant / MinIO，未接 Agent answer。
5. Codex B review 已通过；下一步只做 selective docs baseline，不自动进入 Phase 2.87d 或真实 runtime smoke。

## Phase 2.87b Evidence-only Writer Service Implementation

1. Phase 2.87a baseline 已完成：commit `fb7baba`，tag `phase-2.87a-write-target-discovery-baseline`，pushed=true。
2. Phase 2.87b 首轮实现已完成：新增 dedicated evidence-only writer service 与测试。
3. Writer 只允许在 test-local DB/session 中验证 `Document`、`DocumentVersion`、`Chunk`、`CitationRecord` 边界。
4. 已覆盖 approval/feature flag gates、chunk limit、forbidden raw fields、idempotency duplicate/conflict、rollback dry-run。
5. 验证通过：TDD RED 已观察；目标测试 `7 passed`；py_compile 通过；Data Steward regression `133 passed`。
6. Codex B review 已通过；下一步只做 selective Git baseline。
7. 本阶段仍不执行真实 DB smoke，不接 API / CLI runtime，不写 index/object-store，不接 Agent answer。
8. 仍禁止：真实 `documents/chunks/document_versions` 写入、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、NAS scan、parser、raw content 输出、Agent DB/NAS CRUD、production rollout。

## Phase 2.87a Exact Write Target Discovery / Implementation Gate

1. Phase 2.87 baseline 已完成：commit `069fbec`，tag `phase-2.87-first-real-evidence-write-smoke-plan-baseline`，pushed=true。
2. Phase 2.87a discovery 已完成，新增 `docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md`。
3. 候选 write targets 已识别：`Document/documents`、`DocumentVersion/document_versions`、`Chunk/chunks`、`CitationRecord/citations`，可选 `IngestionJob/ingestion_jobs`。
4. 关键阻塞：现有 upload ingestion path 会读取 file bytes、执行 parser/chunker，并可能写 OpenSearch/Qdrant；不得直接复用为 first real evidence-only smoke。
5. direct real write 当前仍为 `Pause`；Phase 2.87b 如后续授权，应先实现 dedicated evidence-only writer service、idempotency metadata 与 run-scoped rollback dry-run。
6. Codex B review 已通过；下一步只做 selective docs baseline。
7. 仍禁止：真实 `documents/chunks/document_versions` 写入、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、NAS scan、parser、raw content 输出、Agent DB/NAS CRUD、production rollout。

## Phase 2.87 First Real Hermes Evidence Write Smoke Planning

1. Phase 2.87 docs-only planning 已完成，新增 `docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md`。
2. 规划目标：定义未来 Mac mini / 测试机第一次真实 Hermes evidence write smoke 的安全门槛。
3. 已固定 tiny scope：最多 1 source asset、1 document version、20 chunks。
4. 已固定后续 Phase 2.87a 必须另行 operator approval JSON；approval 必须匹配 source asset、project scope、permission proof、limits、target environment、write run id、rollback reference 与 expiration。
5. 已固定 feature flags default off：real evidence write、smoke、Agent answer integration、index write 均默认关闭。
6. 已固定 exact write target gate：Phase 2.87a 必须命名 SQLAlchemy model/table、repository method、transaction boundary 与 rollback/invalidation method；否则 `Pause`。
7. Codex B review 已通过；下一步只做 selective docs baseline。
8. 仍禁止：writer implementation、真实 `documents/chunks/document_versions` 写入、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、NAS scan、parser、raw content 输出、Agent DB/NAS CRUD、production rollout。

## Phase 2.87 First Real Hermes Evidence Write Smoke Planning

1. Phase 2.86a baseline 已完成：commit `c5372fc`，tag `phase-2.86a-evidence-write-rehearsal-baseline`，pushed=true。
2. 当前进入 Phase 2.87 docs-only planning：规划未来第一次真实 Hermes evidence write smoke 的安全边界。
3. 目标 scope：Mac mini / 测试机 only，最多 1 source asset、1 document version、20 chunks，必须有独立 operator approval。
4. 规划文档已完成，Codex B review 已通过；下一步只做 selective docs baseline。
5. 后续 Phase 2.87a 才可能实现 first real write smoke；2.88 才考虑 index write planning；2.89 才考虑 Agent answer integration planning。
6. 仍禁止：真实 `documents/chunks/document_versions` 写入、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、NAS scan、raw content 输出、Agent DB/NAS CRUD、production rollout。

## Phase 2.86a Temp Evidence Write Rehearsal Implementation

1. Phase 2.86 baseline 已完成：commit `8455d4a`，tag `phase-2.86-controlled-real-evidence-write-plan-baseline`，pushed=true。
2. Phase 2.86a 首轮实现已完成：新增 temp repository evidence-write rehearsal service、CLI、target tests、ignored report directory 与 Phase 2.86a docs。
3. Runner 从 ignored local `nas_evidence_write_dry_run.v0` report 生成 ignored local `nas_evidence_write_rehearsal.v0` report，使用 in-memory / temp SQLite repository rehearsal。
4. 能力覆盖：document / version / chunk / citation rehearsal records、idempotency duplicate detection、idempotency conflict no-go、rollback dry-run、sanitized CLI summary。
5. 验证：TDD RED 已观察；target tests `7 passed`；py_compile 通过；Data Steward regression `126 passed`；CLI temp smoke 输出 sanitized `rehearsal_go`。
6. 当前仍未完成：真实 Hermes DB `documents/chunks/document_versions` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
7. Codex B review 已通过；下一步只做 selective Git baseline。
8. 仍禁止：执行 parser、复制真实文件、读取 raw text、扫描 NAS、写真实 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。

## Phase 2.86 Controlled Small-batch Real Hermes Evidence Write Planning

1. Phase 2.85a baseline 已完成：commit `380e7a0`，tag `phase-2.85a-evidence-write-dry-run-baseline`，pushed=true。
2. Phase 2.86 docs-only planning 已完成，新增 `docs/PHASE286_CONTROLLED_REAL_EVIDENCE_WRITE_PLAN.md`。
3. 规划明确 future first real write smoke 只能是 test-machine-only tiny scope：最多 1 source asset、1 document version、20 chunks。
4. 规划已固定 prerequisite chain、operator approval、feature flags default off、write target boundary、citation metadata、idempotency、locks、rollback dry-run 与 Go / Pause / No-Go。
5. Codex B review 已通过；下一步只做 docs-only baseline。
6. 后续候选仍需单独授权：Phase 2.86a local/temp repository rehearsal、Phase 2.87 first test-machine real Hermes evidence write smoke、Phase 2.88 index write planning、Phase 2.89 Agent answer integration planning。
7. 仍禁止：执行 writer、真实写 `documents/chunks`、执行 parser、复制真实文件、读取 raw text、扫描 NAS、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。

## Phase 2.85a Local Evidence Write Dry-run Runner Implementation

1. Phase 2.85 baseline 已完成：commit `dfd9d16`，tag `phase-2.85-evidence-write-dry-run-plan-baseline`。
2. Phase 2.85a 目标实现已完成：local in-memory evidence write dry-run runner、CLI、tests、ignored report storage policy 与 Phase 2.85a docs。
3. Runner 从 ignored local preflight report 生成 ignored local `nas_evidence_write_dry_run.v0` report，模拟 documents / chunks / citations / idempotency / rollback。
4. 当前仍未完成：真实 `documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
5. 仍禁止：执行 parser、复制真实文件、读取 raw text、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
6. 下一步完成 full validation，再由 Codex B review 是否 baseline。

## Phase 2.83a Evidence Write Payload Dry-run Implementation

1. Phase 2.83 baseline 已完成：commit `d3cedc9`，tag `phase-2.83-evidence-payload-contract-plan-baseline`。
2. 当前进入 Phase 2.83a：local evidence-write payload dry-run。
3. 已新增 `AssetCatalog` payload builder 与 CLI，从 ignored local eligibility report 生成 ignored local payload plan。
4. Payload states：`payload_not_allowed`、`payload_ready_for_human_review`、`payload_ready_for_write_dry_run`、`payload_no_go`。
5. `payload_ready_for_write_dry_run` 只表示“可进入未来写入 dry-run 规划”，不表示已写入、已索引或可回答。
6. 当前仍未完成：真实 evidence write preflight、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
7. 仍禁止：执行 parser、复制真实文件、读取 raw text、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
8. 下一步只做 Phase 2.83a Git baseline，baseline 后再决定 controlled evidence write preflight planning。

## Phase 2.83 Evidence Write Payload Contract Planning

1. Phase 2.82a baseline 已完成：commit `1838e3a`，tag `phase-2.82a-evidence-eligibility-dry-run-baseline`。
2. 当前进入 Phase 2.83：只规划 future evidence-write payload contract。
3. 已新增 `docs/PHASE283_EVIDENCE_WRITE_PAYLOAD_CONTRACT_PLAN.md`。
4. 规划明确：future payload 是 planning artifact，不是 document evidence，不得直接进入 Agent answer。
5. 规划定义 future `nas_evidence_write_payload.v0` schema、candidate document / chunk contract、citation contract、decision states 与 gates。
6. 当前仍未完成：payload dry-run builder、真实 payload artifact、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
7. 仍禁止：执行 parser、复制真实文件、读取 raw text、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
8. Codex B review 已通过；下一步只做 Phase 2.83 docs baseline。

## Phase 2.82a Evidence Write Eligibility Dry-run Implementation

1. Phase 2.82 baseline 已完成：commit `931e6e1`，tag `phase-2.82-evidence-write-eligibility-plan-baseline`。
2. 当前进入 Phase 2.82a：local evidence-write eligibility dry-run。
3. 已新增 `AssetCatalog` eligibility evaluator 与 CLI，从 ignored local sanitized manifest 生成 ignored local eligibility report。
4. Eligibility report states：`not_eligible`、`eligible_for_human_review`、`eligible_for_evidence_write_planning`、`no_go`。
5. `eligible_for_evidence_write_planning` 只表示“可进入下一步规划”，不表示已写入、已索引或可回答。
6. 当前仍未完成：future evidence-write payload dry-run、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
7. 仍禁止：执行 parser、复制真实文件、读取 raw text、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
8. 下一步只做 Phase 2.82a Git baseline，baseline 后再决定 future evidence-write payload planning。

## Phase 2.82 Evidence Write Eligibility Planning

1. Phase 2.81a baseline 已完成：commit `985a622`，tag `phase-2.81a-sanitized-evidence-manifest-dry-run-baseline`。
2. 当前进入 Phase 2.82：只规划 evidence-write eligibility review。
3. 已新增 `docs/PHASE282_EVIDENCE_WRITE_ELIGIBILITY_PLAN.md`。
4. 规划明确：manifest 是 review-only，不是 document evidence，不得直接进入 Agent answer。
5. 规划定义 future gates：permission proof、manifest ready、parser parsed、cleanup all_deleted、安全 flags 全 false、人工 review、file type allowlist 等。
6. 当前仍未完成：eligibility evaluator、eligibility report artifact、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
7. 仍禁止：执行 parser、复制真实文件、读取 raw text、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
8. Codex B review 已通过；下一步只做 Phase 2.82 docs baseline。

## Phase 2.81a Sanitized Evidence Manifest Dry-run Implementation

1. Phase 2.81 baseline 已完成：commit `804d069`，tag `phase-2.81-sanitized-evidence-manifest-plan-baseline`。
2. 当前进入 Phase 2.81a：ignored local sanitized evidence manifest dry-run。
3. 已新增 `AssetCatalog` manifest builder 与 CLI，从 sanitized parser preview metadata 生成 `nas_evidence_manifest.v0`。
4. Manifest artifacts 默认写入 ignored local 目录 `reports/nas_evidence_manifests/`。
5. 已新增测试覆盖 ready / no-go / unsafe-field rejection / CLI output。
6. 当前仍未完成：真实 manifest smoke、ingestion、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
7. 仍禁止：执行 parser、复制真实文件、读取 raw text、写 DB/index/object-store、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
8. Codex B review 已通过；下一步只做 Phase 2.81a Git baseline，baseline 后再决定 evidence-write eligibility planning。

## Phase 2.81 Sanitized Evidence Manifest Planning

1. Phase 2.80a Mac mini / 测试机 controlled scratch parser dry-run 已返回 `go`。
2. 验证结果：`sample_count=3`、`copied_count=3`、`parsed_preview_count=3`、`cleanup_status=all_deleted`。
3. 安全边界：未输出 raw text / secret / raw row / 真实文件名 / 真实 NAS 路径 / 敏感业务数据；未写 DB / OpenSearch / Qdrant / MinIO；未接入 Agent answer；未 rollout。
4. 当前能力：Hermes 已证明可在权限证明下复制小批授权样本到本地 scratch，并执行 parser dry-run preview 后清理。
5. 当前仍未完成：sanitized evidence manifest、ingestion、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
6. 已新增 `docs/PHASE281_SANITIZED_EVIDENCE_MANIFEST_PLAN.md`。
7. Phase 2.81 只做 sanitized evidence manifest planning；未实现 manifest runner。
8. Phase 2.81a 如获授权，只能生成 ignored local manifest，不得写 DB/index/object-store，不得接入 Agent answer。
9. 仍禁止：真实 manifest artifact 生成、DB/index/object-store 写入、Agent DB/NAS CRUD、Agent final answer integration、production rollout。
10. Codex B review 已通过；下一步只做 Phase 2.81 docs baseline，baseline 后再决定是否另行授权 Phase 2.81a。

## Phase 2.80 Controlled Scratch Parser Dry-run Planning

1. Phase 2.79a Mac mini / 测试机 small batch NAS scratch-copy smoke 已返回 `go`。
2. 验证结果：`sample_count=3`、`copied_count=3`、`hashes_computed=3`、`cleanup_status=all_deleted`。
3. 安全边界：未输出 secret / raw row / 真实 NAS 路径 / 敏感业务数据；未写 DB / OpenSearch / Qdrant / MinIO；未执行 parser / Agent answer integration / rollout。
4. 当前能力：Hermes 已证明可在权限证明下复制小批授权样本到本地 scratch、计算 hash 并清理。
5. 当前仍未完成：parser、ingestion、`documents/chunks` 写入、OpenSearch / Qdrant 写入、Agent 基于 NAS 正文回答。
6. 已新增 `docs/PHASE280_CONTROLLED_SCRATCH_PARSER_DRY_RUN_PLAN.md`。
7. Phase 2.80 只做 controlled scratch parser dry-run planning；未执行 parser。
8. Phase 2.80a 如获授权，只能生成 local sanitized preview / manifest，不得写 DB/index/object-store。
9. 仍禁止：真实 parser 执行、真实正文读取、DB/index/object-store 写入、Agent DB/NAS CRUD、production rollout。
10. Codex B review 已通过；下一步只做 Phase 2.80 docs baseline，不进入 Phase 2.80a。

## Phase 2.79 Small Batch Real Smoke Planning

1. 当前进入 Phase 2.79：Mac mini / 测试机小批真实 smoke 规划。
2. 已新增 `docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md` 与 `docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md`。
3. 本轮只做 docs / prompt planning，不执行真实 copy。
4. 目标样本：1-3 个小型非敏感文件，优先 Office / PDF / text / CSV / XLSX，单文件建议 <= 50MB，总量 <= 200MB。
5. 真实 smoke 必须后置到 Phase 2.79a 并单独授权。
6. 当前仍禁止：真实 NAS copy、parser、DB / `documents/chunks` / OpenSearch / Qdrant 写入、Agent CRUD、production rollout。
7. 下一步：Codex B review Phase 2.79 planning；通过后再决定 docs baseline 或 Phase 2.79a 授权。
8. 数据库团队可继续二期前半段：REST/API Key `project_scope`、权限证明、资产目录 UI 和 Agent 查询入口。

## Phase 2.78 Controlled Local Scratch Runtime

1. Phase 2.78 本地 fixture runtime 已完成首轮实现。
2. 新增 `AssetScratchRuntime`，要求 `runtime_authorized=true`、`scratch_copy_enabled=true`、`batch_copy_enabled=true`，否则 fail closed。
3. runtime 只处理 dry-run plan 中 `would_copy` 的 item，只允许 local path / `file://` fixture。
4. 成功和失败路径均执行 cleanup，并输出 sanitized run record；不得包含 source path / scratch path 原文。
5. 当前仍禁止真实 NAS 连接、真实企业文件复制、parser 调用、DB/index/object storage 写入、runtime flags 默认开启和 rollout。
6. 下一步：完成完整目标验证后交 Codex B review；Phase 2.79 才能规划小批量真实 smoke。

## Phase 2.76 / 2.77 NAS Scratch Copy Pipeline Dry-run

1. 当前进入按项目小批量 NAS scratch copy dry-run。
2. 新增 `AssetScratchCopyPlanner`，只基于 fake asset catalog 生成计划，不连接真实 NAS。
3. 新增默认关闭 feature flags：`PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false`、`PLATFORM_ASSET_BATCH_COPY_ENABLED=false`。
4. 默认限制：最多 10 个文件、总大小 2GB、单文件 512MB。
5. 允许候选：office / pdf / text / csv 等小型文件，且必须具备权限 scope、非 `UNKNOWN` 密级、非 `catalog_only`、active lifecycle、storage locator。
6. BIM 大模型 / unsupported 文件继续 metadata-only，不进入正文复制计划。
7. 当前仍不授权：真实 NAS 连接、文件复制、文件解析、selective indexing、写 `documents/chunks/OpenSearch/Qdrant`、Agent CRUD、production rollout。
8. 下一步：目标验证与 Codex B review；通过后再 baseline。

## Phase 2.75 Data Steward Catalog Query Preview

1. 当前进入 Phase 2.75：只读 catalog query preview。
2. Phase 2.74 能力边界已明确：真实 DB v1.1 结构 / 脱敏统计 / Hermes adapter contract 已打通，但尚未完整耦合，不支持企业 Agent 直接无损查询 NAS 文件正文。
3. 新增 `AssetCatalogQueryPreviewer`，让 catalog lookup 返回资产目录元数据预览；content answer 场景返回 `asset_catalog_only` Missing Evidence。
4. 缺少 REST/API Key `project_scope` 时继续 fail-closed；`permission_tags` 不是最终权限。
5. 验证通过：py_compile 通过，Data Steward 目标 pytest `77 passed`，`git diff --check` 通过。
6. 当前仍不授权：runtime enable、mirror、selective indexing、NAS scan、DB CRUD、Agent 改 MySQL / NAS、catalog metadata 替代 document evidence、production rollout。
7. Codex B review 已通过，已写入 `docs/NEXT_CODEX_A_PROMPT.md` selective baseline 任务。
8. 下一步：先完成 Phase 2.75 baseline；baseline 后再规划 Phase 2.76 project-scope 权限证明与主仓 preview UX。

## Phase 2.74 Test-machine v1.1 Adapter Smoke Handoff

1. 已新增 `docs/PHASE274_TEST_MACHINE_V11_ADAPTER_SMOKE_PLAN.md`。
2. 已新增 `docs/CODEX_TEST_MACHINE_V11_ADAPTER_SMOKE_PROMPT.md`，用于测试机 reviewed-ref 复验。
3. 下一步由用户把该 prompt 交给测试机 Codex 执行。
4. 当前仍不授权：runtime enable、mirror、indexing、Agent CRUD、NAS scan、DB 写入、production rollout。
5. 测试机 Go 后，再考虑 Data Steward 接入基线或 catalog query preview。

## Phase 2.73 Hermes v1.1 Readonly Adapter Contract Update

1. Hermes 侧 readonly adapter contract 已更新到 `delivery_platform.asset_views.v1.1`。
2. 已补齐 `permission_tags`、`confidentiality_level`、`last_seen_at`、`lifecycle_status`、`index_eligibility`、`ModelAssetView.project_id` 的本地契约测试。
3. catalog metadata DTO 已可透出 v1.1 字段，但仍保持 `content_evidence_available=false`。
4. 无 REST/API Key `project_scope` 时仍 fail-closed，不把 `permission_tags` 当最终权限。
5. 下一步：测试机部署 reviewed ref 后复验 v1.1 readonly adapter；仍不启用 mirror、indexing、Agent CRUD 或 rollout。

## Phase 2.72b DB LIMIT 30 Redacted Statistics Smoke Result

1. 测试机 `LIMIT 30` 脱敏统计 smoke 已通过。
2. 已新增 `docs/PHASE272B_DB_LIMIT30_REDACTED_SMOKE_RESULT.md`。
3. 统计结果可支持下一步 Hermes v1.1 readonly adapter contract planning。
4. 当前仍未授权：mirror、indexing、Agent CRUD、Data Steward runtime 默认开启、production rollout。
5. 下一步建议：Phase 2.73 规划 Hermes 侧 fake adapter / contract tests / DTO 预期更新，保持 feature flags 默认 off。

## Phase 2.72a DB LIMIT 30 Redacted Statistics Smoke Planning

1. 已新增 `docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md`。
2. 已更新 `docs/DB_LIMIT30_REDACTED_SMOKE_PLAN.md` 为 prompt ready。
3. 本仓库未执行 `LIMIT 30`，未读取真实行，未连接新 DB，未写任何系统。
4. prompt 只允许输出聚合统计：row count、null / non-null、枚举分布、timestamp coverage、size bucket、permission tag 前缀覆盖。
5. prompt 明确禁止 raw row、真实项目名、文件名、NAS 路径、ID 原值、`permission_tags` 原值、summary JSON 原文、secret、写操作、NAS scan、mirror、indexing、Agent CRUD、rollout。
6. 下一步：用户若授权，把该 prompt 交给测试机 Codex；若返回 Go，再规划 Hermes v1.1 readonly adapter contract update。

## Phase 2.72 DB v1.1 Structure-only Smoke Result

1. 测试机 v1.1 structure-only smoke 已通过。
2. 已新增 `docs/PHASE272_DB_V11_STRUCTURE_SMOKE_RESULT.md`，记录四个 View、v1.1 字段、`WHERE 1 = 0` 与安全边界。
3. 当前完成：真实 DB v1.1 结构级只读耦合。
4. 当前未完成：完整 Data Steward 耦合、mirror、selective indexing、Agent CRUD。
5. 下一步建议：规划 `LIMIT 30` 脱敏统计 smoke prompt，继续禁止 raw row / 真实业务标识输出；执行仍需用户显式授权。
6. 备选下一步：Hermes 侧 v1.1 readonly adapter contract update，继续保持 feature flags 默认 off。

## Phase 2.71 DB v1.1 Contract Alignment

1. 数据库团队已回复 schema gap request，并确认可推进 `delivery_platform.asset_views.v1.1` 合同评审。
2. 已新增 `docs/DB_SCHEMA_GAP_SANITIZED_RESPONSE.md`，记录脱敏回复。
3. 已新增 `docs/PHASE271_DB_V11_CONTRACT_ALIGNMENT_PLAN.md`，明确 v1.1 字段、Hermes fail-closed 规则、后续 structure-only / `LIMIT 30` 顺序。
4. 已根据数据库团队第 6 节回复更新 `docs/CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md`，固定 `permission_tags` 枚举、`UNKNOWN` 默认密级、`stale_unverified` 生命周期与 `catalog_only` 默认索引资格。
5. 已根据数据库团队第 6 节回复更新 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`，用于 v1.1 完成后的结构复验。
6. v1.1 短期建议字段：`ModelAssetView.project_id`、粗粒度 `permission_tags`、`confidentiality_level`、`last_seen_at`、`lifecycle_status`、`index_eligibility`、`AuditEventView.event_id` checkpoint 语义；`project_scope` 以 REST / API Key 调用者上下文为主。
7. 当前下一步：把 `CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md` 交给数据库团队；v1.1 完成后再执行 `CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`。
8. 当前仍禁止：`LIMIT 30`、真实行读取、raw row 输出、mirror migration、DB CRUD、NAS scan、indexing、Data Steward runtime activation、production rollout。
9. 数据库团队已完成 v1.1 目标环境部署：V17 migration 已应用，后端测试实例健康检查 `UP`。
10. 已更新 `docs/DB_V11_DEPLOYMENT_BLOCKER_STATUS.md`；当前允许测试机执行 v1.1 structure-only smoke。
11. 下一步执行 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`；仍禁止 `LIMIT 30`、真实行读取、mirror、indexing 和 Agent CRUD。

## Phase 2.70 DB Schema Contract Gap Review

1. 测试机 DB `structure_only` smoke 已通过，代表 Hermes 与真实 DB 完成第一阶段只读结构级耦合。
2. 已新增 `docs/PHASE270_DB_SCHEMA_CONTRACT_GAP_REVIEW.md`，梳理真实 View 字段与 Hermes contract 的 P0 / P1 / P2。
3. 已新增 `docs/DB_SCHEMA_GAP_REQUEST_TO_DB_TEAM.md`，建议发给数据库团队评审 P1 字段缺口。
4. 已新增 `docs/DB_LIMIT30_REDACTED_SMOKE_PLAN.md`，仅作为后续脱敏样本 smoke 规划，不是执行授权。
5. P1 关键缺口：权限标签、项目范围、密级、`ModelAssetView.project_id`、`last_seen_at`、lifecycle / moved / stale / missing、index eligibility、事件 checkpoint 语义。
6. 当前不允许 `LIMIT 30`、真实样本读取、mirror migration、DB CRUD、NAS scan、selective indexing 或 rollout。
7. 下一步：数据库团队回复字段补齐可行性；用户若授权，再生成 `LIMIT 30` 脱敏样本 smoke prompt。

## DB Team Direct Handoff Protocol

1. 后续 DB / Data Steward prompt 与测试机前置检查不再经由 Codex A。
2. Codex B 直接与用户 / 数据库团队 / 测试机 Codex 对接，维护 DB prompt、审核 sanitized report、列出数据库团队配合项。
3. 已新增 `docs/DB_TEAM_DIRECT_HANDOFF_PROTOCOL.md` 固化流程。
4. Codex A 继续负责主线功能实现，但不再作为 DB 测试机 prompt 生成中转。
5. 当前下一步可直接把 `docs/CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md` 交给测试机 Codex / operator。
6. 前置条件 Go 后，仍需用户显式授权才能重新执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`。

## Phase 2.69b DB Structure-only Precondition Runbook

1. Phase 2.69b precondition prompt 已完成：`docs/CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md`。
2. 该 prompt 只允许测试机确认 Hermes_memory install / version、secure env key names、readonly credential key name、contract version、MySQL client 或 Hermes readonly tooling；禁止连接 DB、执行 SQL、读取真实行、安装工具或输出 secret。
3. 当前结论：`ready_for_test_machine_precondition_check`。
4. 下一步：Codex B review；通过后用户可交给测试机 Codex 执行前置条件检查。
5. 若前置条件 Go，也不得自动重新执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`；必须等待用户显式指令。
6. 后置继续禁止：真实行读取、`LIMIT 1/30` 样本、NAS scan、DB CRUD、migration、mirror write、OpenSearch / Qdrant 写入、repair/backfill/reindex/delete、production rollout。

## Phase 2.69 DB Structure-only Smoke Runbook Planning

1. Phase 2.69 runbook / prompt planning 已完成。
2. 新增 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`，用于测试机 Codex 执行 `structure_only` smoke。
3. prompt 已明确只允许结构握手 SQL，不允许真实行读取或 `LIMIT 1` / `LIMIT 30`。
4. prompt 已明确不得输出 secret、真实项目名、文件名、NAS 路径、`asset_uid`、`source_id`、raw row 或 SQL stderr。
5. prompt 已明确无 host / port / database / readonly credential 安全注入时必须 `Pause`。
6. 下一步：Codex B review；通过后由用户决定是否把 prompt 交给测试机 Codex。
7. 后置：`LIMIT 30` 脱敏样本、mirror migration、DB CRUD、selective indexing、operation plan / approval、production rollout。

## Phase 2.68 Data Steward DB Branch Intake / Merge Readiness Review

1. Phase 2.68 只读接收评审已完成，结论为 `ready_for_mainline_acceptance`。
2. 已确认主线包含低耦合 Data Steward / asset catalog 接口，所有 Data Steward runtime / readonly / sample flags 默认关闭。
3. 已确认 catalog-only 预览与 retrieval guard 不写 `documents` / `chunks` / OpenSearch / Qdrant；Missing Evidence 支持 `asset_catalog_only`；权限 scope / tags 缺失保持 deny / fail-closed。
4. 已确认 DB 支线 closeout baseline：branch `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
5. 验证：Data Steward target tests `71 passed`，MVP runner regression target `32 passed`，`git diff --check` 通过。
6. 后续不得 raw merge DB 支线未跟踪 QA probe 文件；不得连接真实 DB、扫描 NAS、写 migration / `documents` / `chunks` / OpenSearch / Qdrant。
7. 下一步建议 Phase 2.69 planning：测试机真实 DB `structure_only` smoke；需数据库团队提供网络路径、只读凭证安全传递方式、View contract 版本与 `structure_only` 授权，不要求 secret 明文。
8. `LIMIT 30` 脱敏样本、mirror migration、DB CRUD、selective indexing、operation plan / approval 与 production rollout 继续后置。

## Phase 2.68 Data Steward DB Branch Intake / Merge Readiness Review（planning 原始记录）

1. 当前进入 Phase 2.68：接收评审 Data Steward DB 支线与主线已选择性接入内容。
2. DB 支线 closeout baseline：`/Users/Weishengsu/Hermes_memory_db0`，branch `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
3. 本阶段只做只读 review、目标测试与文档交接，不连接真实 MySQL，不扫描 NAS，不写 migration / `documents` / `chunks` / OpenSearch / Qdrant。
4. 本阶段不实现 DB CRUD；未来写操作必须通过平台 API / operation plan / approval / audit，不允许 Agent 直接改 MySQL 或 NAS。
5. 必查项：feature flags 默认 off、catalog-only 不进入正文 evidence、Missing Evidence 支持 `asset_catalog_only`、权限缺失默认 deny、无 QA probe / secret / 真实样本混入。
6. 若 review 通过，下一阶段规划测试机真实 DB `structure_only` smoke；届时再联系数据库团队确认网络路径、只读凭证传递方式、View contract 版本与授权范围。
7. 内部受控 MVP 试用可并行继续，production rollout 仍禁止。

## Phase 2.66 Mac mini Controlled Install Planning

1. 已完成 Mac mini 侧受控安装规划文档：`docs/PHASE266_MAC_MINI_CONTROLLED_INSTALL_PLAN.md`。
2. 推荐下一步为 Phase 2.66a preflight-only，而不是直接 full install。
3. Phase 2.66a 只检查 macOS / user / git / uv / Docker / disk / target dirs / Git remote refs / env key names。
4. Phase 2.66a 禁止启动 Docker、运行 API / CLI smoke、上传文件、连接真实 DB、扫描 NAS、写 DB/index、repair/backfill/reindex/delete/migration。
5. Mac mini 侧必须回传 Go / Pause / No-Go 结果后，才判断是否进入受控安装执行。
6. 当前不进入 production rollout。

## Phase 2.65 reviewed-ref fix

1. 已完成 Codex B review fix：hermes-agent reviewed ref 从 `NEEDS_REVIEWED_AGENT_REF` 更新为 `phase-2.56e-natural-import-real-upload-smoke-baseline`。
2. 已同步 Mac mini landing plan、install/update quickstart、Codex Mac mini prompt 与 operator command sheet。
3. 新增测试断言：reviewed hermes-agent tag 生成 `ready_for_operator_review`，placeholder ref 仍生成 `pause`。
4. 验证：py_compile 通过；Phase 2.65 / 2.60 / 2.63 / 2.62 / 2.61a 目标测试 `41 passed`；reviewed / placeholder manifest smoke、diff check、latest JSON check 均通过。
5. 当前 Mac mini install handoff 不再因 hermes-agent reviewed ref 缺失而 pause。
6. 本阶段未执行真实 Mac mini deployment、Docker startup、API / CLI smoke、真实 DB/NAS/Data Steward smoke、DB/index 写入或 rollout。
7. 下一步：Codex B review；通过后再写 Phase 2.65 selective Git baseline prompt。

## Phase 2.65 Mac mini MVP Landing Acceleration Pack

1. 已完成 Mac mini MVP landing pack 首轮实现。
2. 新增只读 `scripts/phase265_mvp_release_manifest.py`，只输出 install/update/rollback manifest，不读取 `.env`，不启动服务，不执行 git pull，不修改仓库状态。
3. 新增 `docs/PHASE265_MAC_MINI_MVP_LANDING_PLAN.md` 与 `docs/MAC_MINI_MVP_INSTALL_UPDATE_QUICKSTART.md`。
4. 已更新 `docs/CODEX_MAC_MINI_INSTALL_AND_UPDATE_PROMPT.md` 与 `docs/MAC_MINI_OPERATOR_COMMAND_SHEET.md`，写入 Hermes_memory reviewed ref 与 hermes-agent 缺 ref pause 规则。
5. 验证：py_compile 通过；Phase 2.65 / 2.60 / 2.63 / 2.62 / 2.61a 目标测试 `40 passed`；manifest sample / diff check / latest JSON check 通过。
6. 当前 Mac mini install readiness 为 `Pause`：缺 hermes-agent reviewed ref；不应猜测 branch/tag/commit。
7. 本阶段未执行真实 Mac mini deployment、Docker startup、API / CLI smoke、真实 DB/NAS/Data Steward smoke、DB/index 写入或 rollout。
8. 下一步：Codex B review；通过后再写 Phase 2.65 selective Git baseline prompt。

## Phase 2.64b Selective Data Steward DB Integration

1. 已完成 Data Steward DB 支线选择性合入首轮实现。
2. 已按白名单接入 `app/services/asset_catalog/**`、`tests/test_data_steward_*.py`、Data Steward / DB contract docs。
3. 已在 `app/core/config.py` 增加 Data Steward feature flags，默认全部关闭。
4. 已明确未执行 raw merge，未引入 `.claude/**`、DB 支线交接文件、QA probe 或任何会回退主线 Phase 2.57-2.63 MVP 的删除。
5. 目标验证：Data Steward pytest `71 passed`，target ruff `All checks passed!`，Phase 2.63 / 2.62 / 2.61a regression `28 passed`。
6. 本阶段未连接真实 DB，未扫描 NAS，未写 migration / documents / chunks / OpenSearch / Qdrant，未创建 PR，未 commit / tag / push。
7. 下一步：Codex B review Phase 2.64b；通过后再写 selective Git baseline prompt。

## Phase 2.64 Data Steward DB Branch Intake / PR Review

1. Phase 2.63 baseline 已完成：`fee1dcb` / `phase-2.63-operator-daily-summary-baseline`。
2. 已完成 DB 支线 intake / PR readiness review 首轮记录。
3. DB 支线 `/Users/Weishengsu/Hermes_memory_db0` 当前 branch `codex/data-steward-db0-contract`，HEAD `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
4. DB 支线 branch 与 tag 已推送到 origin。
5. DB 支线验证：`npm test` 为 `71 passed`，`npm run lint` 为 `All checks passed!`，`git diff --check` 通过。
6. 本阶段未连接真实 DB，未扫描 NAS，未写 migration / documents / chunks / OpenSearch / Qdrant，未 merge 到 `main`，未创建 PR。
7. Phase 2.64 当前不建议 baseline；需先由 Codex B review intake / merge gates。
8. 下一步：Codex B review Phase 2.64；通过后由用户决定是否创建 PR、写 merge plan 或等待测试机真实 DB smoke。

## Phase 2.63 Internal MVP Operator Daily Summary Workflow

1. Phase 2.62 baseline 已完成：`fd7d4a7` / `phase-2.62-issue-triage-summary-baseline`。
2. Phase 2.63 daily summary workflow 已完成 implementation 并通过 Codex B review。
3. 目标验证通过：`28 passed`，py_compile / diff check / latest JSON check 均通过。
4. 下一步只执行 Phase 2.63 selective Git baseline；baseline 后停止。
5. Phase 2.64 建议进入 Data Steward DB Branch Intake / PR Review，对接数据库团队。

## Phase 2.64 候选：Data Steward DB Branch Intake / PR Review

1. DB 支线 closeout baseline：`/Users/Weishengsu/Hermes_memory_db0`，branch `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
2. 数据库开发团队正在等待企业 Agent 接入与测试数据库可用性。
3. Phase 2.64 建议做接收审查、目标验证、必要 push、PR readiness 文档；不继续 DB 功能开发，不 merge 到 main，不连接真实 DB，不扫描 NAS。

## Phase 2.63 Internal MVP Operator Daily Summary Workflow

1. Phase 2.62 baseline 已完成：`fd7d4a7` / `phase-2.62-issue-triage-summary-baseline`。
2. 已完成首轮 implementation：新增 `scripts/phase263_mvp_operator_daily_summary.py` 与目标测试。
3. runner 可读取 Phase 2.62 summary 或直接读取 issue JSON / issue 目录，并输出每日 `ready` / `pause` / `no_go` operator summary。
4. Markdown 输出保持脱敏，不输出 raw query、notes、expected/actual behavior、local full path、document ids 或 chunk ids。
5. 验证：`py_compile` 通过，Phase 2.63 / 2.62 / 2.61a 目标测试 `28 passed`。
6. 下一步：Codex B review；通过后再写 selective Git baseline prompt。

## 后置候选：Data Steward DB Branch Intake / PR Review

1. DB 支线 closeout baseline：`/Users/Weishengsu/Hermes_memory_db0`，branch `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
2. 后续可开独立 DB branch intake / PR review 阶段。
3. 当前 Phase 2.63 不处理 DB branch merge，不进入 DB-5 / DB-6，不接真实数据库，不扫描 NAS。

## Phase 2.62 Internal MVP Issue Triage Summary Runner

1. Phase 2.61c baseline 已完成：`959ac78` / `phase-2.61c-internal-mvp-issue-storage-baseline`。
2. 已实现只读本地 issue triage summary runner：`scripts/phase262_mvp_issue_triage_summary.py`。
3. runner 可把显式 issue JSON 或 ignored issue 目录聚合为脱敏 summary，供 Codex B 快速 review。
4. 本阶段未创建外部 issue，未写 DB/index，未 repair，未 rollout。
5. Codex B review 已通过；下一步只执行 Phase 2.62 selective Git baseline，baseline 后停止。

## 后续主线任务：Data Steward DB branch intake / merge readiness

1. DB / NAS / Data Steward 支线是 Hermes 主线后续能力的一部分，不再视为临时旁支；但不得打断当前内部 MVP issue triage / Mac mini 落地主线。
2. DB 支线 closeout baseline：`/Users/Weishengsu/Hermes_memory_db0`，分支 `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
3. 推荐后续开独立主线阶段处理：`Data Steward DB Branch Intake / PR Review`。
4. 合入前必须确认：feature flags 默认 off；catalog-only 不写 `documents/chunks`；不写 OpenSearch / Qdrant；Missing Evidence 支持 `asset_catalog_only`；`permission_tags/project_scope` 缺失默认 deny；测试 agent probe 文件不纳入提交。
5. DB-5 selective indexing、DB-6 operation plan / approval、真实 DB smoke、真实 NAS / BIM 扫描、真实 retrieval/indexing 继续后置，需要用户单独授权。
6. 当前不直接本地 merge；优先 Draft PR / merge readiness review，避免把支线中的 `.claude/*`、历史文档或非必要文件无差别并入主线。

## Phase 2.61c Local Issue Storage Artifact

1. Phase 2.61c artifact 已完成并通过 Codex B review。
2. 新增 `reports/internal_mvp_issues/.gitignore` 与 `README.md`，真实 issue JSON / Markdown / 截图 / 日志 / 表格 / 文档默认 ignored。
3. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 selective Git baseline。
4. baseline 白名单仅限 storage policy 文件与交接文档；不得纳入历史 Phase 2.38 dirty 或 DB/NAS 草稿。
5. 继续禁止真实 issue records、外部 issue 创建、API/CLI smoke、DB/index 写入、repair/backfill/reindex、Data Steward 和 production rollout。

## Phase 2.61c Local Issue Storage Artifact

1. Phase 2.61b baseline 已完成：`d62b8a6` / `phase-2.61b-issue-storage-policy-baseline`。
2. 已创建 `reports/internal_mvp_issues/.gitignore` 与 `README.md`，固化本地 issue records ignored storage。
3. 真实 issue JSON / Markdown / 截图 / 日志 / 表格 / 文档默认不入 Git。
4. 本轮未生成真实 issue records，未创建外部 issue，未写 DB，未 repair，未 rollout。
5. 下一步：Codex B review Phase 2.61c artifact；通过后再写 selective Git baseline prompt。

## Phase 2.61b Local Issue Storage Policy Planning

1. Phase 2.61a baseline 已完成：`b60d4d7` / `phase-2.61a-mvp-issue-intake-baseline`。
2. Phase 2.61b docs-only planning 已完成并通过 Codex B review：新增 `docs/PHASE261B_ISSUE_STORAGE_POLICY_PLAN.md`。
3. 推荐方向：后续使用 `reports/internal_mvp_issues/` 保存本地 issue records，真实 JSON / Markdown 默认不入 Git。
4. Phase 2.61c 可只提交 `.gitignore` / `README.md`，不提交真实 issue records；不得在 2.61b baseline 中创建真实 issue records。
5. 继续禁止真实上传、API/CLI smoke、DB/index 写入、外部 issue 自动创建、repair/backfill/reindex、Data Steward 和 production rollout。
6. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，只做 Phase 2.61b selective docs-only Git baseline。

## Phase 2.61a Internal MVP Issue Intake Runner

1. Phase 2.61 planning 已完成并经 Codex B review 通过。
2. 当前下一步：实现本地 issue intake template / dry-run validator / summary generator。
3. 目标是把 Mac mini 真实试用问题结构化回收，减少人工复制长聊天记录。
4. 本阶段不写 DB、不创建外部 issue、不 repair、不 rollout。
5. Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成后交 Codex B review。

## Phase 2.61 Internal MVP Operator Flow / Issue Intake Planning

1. Phase 2.60 baseline 已完成：`f445182` / `phase-2.60-mvp-local-readiness-pack-baseline`。
2. Phase 2.61 docs-only planning 已完成：新增 `docs/PHASE261_INTERNAL_MVP_OPERATOR_FLOW_PLAN.md`。
3. 规划已定义使用前 readiness gate、使用中记录字段、P0/P1/P2/P3 分级、Codex A/B/C/D 分工和 Phase 2.61a 候选。
4. 推荐下一步：Codex B review。通过后再写 Phase 2.61a local issue intake template / dry-run validator prompt。
5. 当前仍不允许真实上传、API/CLI smoke、DB/index 写入、Data Steward、production rollout。

## Phase 2.61a Internal MVP Issue Intake Runner

1. Phase 2.61a implementation 已完成，等待 Codex B review。
2. 新增 `scripts/phase261a_mvp_issue_intake.py`，支持 `--new-template` 与 `--input-json`。
3. 新增 `tests/test_phase261a_mvp_issue_intake.py`，目标测试当前为 `9 passed`。
4. runner 固定 `dry_run=true`、`read_only=true`、`destructive_actions=[]`、`external_issue_created=false`、`repair_attempted=false`、`production_rollout=false`。
5. P0 或危险字段会输出 `no_go`；P1 输出 `pause`；合法 P2/P3 输出 `ready`。
6. 当前不写 DB、不创建外部 issue、不写默认 reports 路径、不进入 repair 或 rollout。

## Phase 2.60 Internal MVP Launch Readiness Pack

1. Phase 2.59 baseline 已完成：`2603a87` / `phase-2.59-natural-import-second-smoke-plan-baseline`。
2. 当前用户选择暂不执行第二真实文件 smoke，优先把本地 MVP 推进到 Mac mini 内部真实使用前的 readiness 形态。
3. 下一步 Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`：实现只读 local readiness runner、目标测试和 operator 文档同步。
4. 本阶段不上传文件、不运行真实 API/CLI smoke、不写 DB/index、不进入 Data Steward、不开 production rollout。
5. 完成后交 Codex B review；不自动 baseline。

## Phase 2.57 Natural Import MVP Usability / Evidence Planning

1. Phase 2.57 docs-only planning 已完成。
2. 新增 `docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`。
3. 后续候选：
   - Phase 2.57a：自然语言导入 evidence template / runbook runner dry-run。
   - Phase 2.57b：第二个小文件真实导入验证，但必须重新取得用户显式授权。
   - Phase 2.58：Mac mini MVP operator checklist 更新。
4. 当前禁止：API / CLI smoke、上传文件、DB / index 写入、cleanup / repair / reindex、Data Steward、production rollout。

## Phase 2.56e Natural Import Real Upload Client

1. Phase 2.56e implementation + real smoke 已完成，等待 Codex B review。
2. 自然语言 CLI 导入用户授权 `.docx` 成功：`document_id=ee54b72c-b88b-4fad-be54-007240285356`，`version_id=950da5fe-dd7c-4eba-8764-916b556d14ce`，`chunk_count=1`，`indexed_count=1`。
3. `@C塔人力测算` 同 session retrieval smoke 只返回新导入文档 evidence。
4. 下一步只建议 Phase 2.56e selective baseline；不得自动 cleanup / delete / repair / backfill / reindex。
5. Data Steward、bulk/NAS/TB 文件池、production rollout 仍后置。

## Phase 2.56d Natural Import Runtime Wiring

1. Phase 2.56d runtime wiring 最小实现已通过 Codex B review，下一步只做 selective Git baseline。
2. Hermes 主仓新增 runtime preflight hook；自然语言导入 intent 会在普通 retrieval / LLM answer 前被拦截。
3. 默认真实 upload 关闭，返回 `real_upload_enabled=false`、`upload_adapter_status=disabled`、`ingestion_status=not_executed`。
4. fake adapter success / failure / missing id 测试通过；runtime disabled-path CLI smoke 通过。
5. 本轮未调用真实 Hermes_memory upload API、未上传真实文件、未写 DB / OpenSearch / Qdrant。
6. baseline 后停止；后续 Phase 2.56e 才可复用用户授权文件做真实自然语言导入 smoke。

## Phase 2.56c Natural Import Real Smoke Result

1. Phase 2.56c 已执行到 stop condition：`runtime_not_wired_to_real_upload_adapter`。
2. 已通过文件 metadata preflight、Hermes_memory API health、Hermes CLI help、natural import parser preflight。
3. Hermes 主仓 runtime 尚未把 `run_natural_file_import_preflight()` 接入 `run_agent.py` 用户路径，也未配置真实 upload adapter。
4. 本轮未调用普通 upload path 绕过验证，未上传文件，未写 DB / OpenSearch / Qdrant，未绑定 alias，未做 retrieval smoke。
5. 下一步建议：Codex B review 后规划 Phase 2.56d runtime wiring 最小实现；继续禁止 cleanup / delete / repair / backfill / reindex / rollout。

## Phase 2.56c Natural Import Real Smoke Authorization Gate

1. 用户已授权 Phase 2.56c 单文件自然语言导入真实 smoke。
2. 授权文件：`/Users/Weishengsu/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_sn2cczdp4u2l12_c2fd/msg/file/2026-05/C塔项目人力配置及成本测算表0506.docx`。
3. 文件 metadata：regular file，`16885 bytes`，Microsoft Word 2007+ `.docx`。
4. 用户接受产生测试 document/version/chunk/OpenSearch/Qdrant 记录；cleanup/delete/repair/reindex 默认不授权。
5. 下一步 Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`；必须优先验证自然语言导入路径，不得绕过成普通 upload 后声称通过。

## Phase 2.56b Natural Import Real Smoke Planning

1. Phase 2.56b planning 已通过 Codex B review。
2. 规划覆盖授权门槛、样本要求、执行步骤、验收字段、stop conditions、run record 与非目标。
3. 下一步只做 docs-only selective Git baseline。
4. baseline 必须排除 `PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 与 DB/NAS 草稿。
5. Phase 2.56c 才可在用户显式授权后执行真实自然语言导入 smoke。

## Phase 2.56a Natural Import Real Adapter Skeleton

1. Phase 2.56a implementation 已通过 Codex B review。
2. 真实 upload 默认关闭；`real_upload_enabled=False` 时 valid import fail-closed 为 `real_upload_disabled`。
3. Codex B 复跑 Hermes 主仓 py_compile 与 targeted pytest，结果 `25 passed`。
4. 下一步只做 dual-repo selective Git baseline。
5. baseline 必须排除 Hermes 主仓既有 dirty：`hermes_memory_adapter.py`、`uv.lock`、PHASE211E 文档、adapter reload 测试。
6. baseline 必须排除 Hermes_memory 既有 dirty：`PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 与 DB/NAS 草稿。
7. Phase 2.56b 才可在用户显式授权后做自然语言导入真实小文件 smoke。

## Phase 2.55a Codex B Review / Baseline Prompt

1. Phase 2.55a 单文件真实 upload smoke 已通过 Codex B review。
2. 不需要 Codex C targeted validation。
3. 下一步仅执行 selective Git baseline，不进入 Phase 2.56。
4. baseline 白名单：`ACTIVE_PHASE.md`、`PHASE_BACKLOG.md`、`HANDOFF_LOG.md`、`NIGHTLY_SPRINT_QUEUE.md`、`NEXT_CODEX_A_PROMPT.md`、`NEXT_CODEX_C_PROMPT.md`、`TODO.md`、`DEV_LOG.md`。
5. 不得纳入旧 dirty `PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`、DB / NAS 契约草稿或 ignored run records。
6. P2 展示尾项：API 顶层 `citations=[]`，但 result-level / CLI citations 可见；后续可在 UX polish 中处理。

## Phase 2.55a Internal MVP Real Upload Smoke Result

1. Phase 2.55a 单文件内部 MVP upload smoke 已完成并通过。
2. 授权文件已通过既有 `/api/v1/documents/upload` 入库：`document_id=06e59241-95e9-44ff-a73d-35d2f52a359b`，`version_id=7dc57676-c707-4f44-9688-0b77058f07a0`，`chunk_count=26`。
3. API hybrid retrieval 与 Hermes CLI alias / retrieval smoke 均只返回新上传文件 evidence，未发现第三文件污染。
4. 安全边界保持：`metadata_as_answer=false`、`facts_as_answer=false`、`snapshot_as_answer=false`、`requires_retrieval_evidence=true`。
5. 后续等待 Codex B review；不自动 baseline、不自动进入 Phase 2.56、不执行 cleanup / delete / repair / backfill / reindex。
6. 可选尾项：API `SearchResponse.citations` 顶层数组为空但 result-level citation fields 与 CLI citations 可见；由 Codex B 判断是否进入展示 / contract 外尾项。

## Phase 2.55a Internal MVP Real Upload Smoke

1. 用户已授权单个小型 `.docx` 文件用于内部 MVP upload smoke：`/Users/Weishengsu/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_sn2cczdp4u2l12_c2fd/msg/file/2026-05/卓羽智能核心技术能力汇报 PPT 大纲V1.0.docx`。
2. 下一步 Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`：仅做单文件 upload / ingestion / retrieval smoke 与 ignored sanitized run record。
3. 本轮允许 upload smoke 产生测试 document / version / chunk / index 记录；不允许 cleanup / delete / repair / backfill / reindex / migration。
4. 继续禁止目录递归上传、NAS / BIM / TB 文件池、Data Steward 实现、production rollout、自动审标或自动经营决策。
5. Codex A 完成后必须停止等待 Codex B review；是否需要 Codex C targeted validation 由 Codex B 再判断。

## 最新状态

1. Phase 2.55 planning 已通过 Codex B review，下一步只做 docs-only Git baseline。
2. baseline 文件只允许 Phase 2.55 规划文档与交接文档，不得纳入 `PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`。
3. baseline 后停止；Phase 2.55a 真实 upload smoke 必须等用户提供非敏感文件路径并明确授权。

## 最新状态

1. Phase 2.55 docs-only planning 已完成，新增 `docs/PHASE255_INTERNAL_MVP_REAL_UPLOAD_SMOKE_PLAN.md`。
2. 规划内容覆盖小型非敏感单文件、pre-flight、smoke steps、trace/citation 验收、stop conditions、sanitized run record 与 Phase 2.55a authorization gate。
3. 本轮未执行真实 upload、未运行 API / CLI smoke、未写 DB / index、未进入 Data Steward / BIM / NAS / TB 文件池。
4. Phase 2.55a 默认不允许；必须由用户提供非敏感文件路径并明确授权后才可执行。

## 最新状态

1. Phase 2.54c Codex C 复测已通过，当前下一步只做 selective Git baseline。
2. baseline 白名单：Hermes 主仓 `context_builder.py` / `test_session_document_scope.py`；Hermes_memory 交接文档。
3. 必须排除既有无关 dirty：Hermes_memory `PHASE238_TENDER_P1_RECALL_FIX_PLAN.md`，主仓 `hermes_memory_adapter.py` / `uv.lock` / PHASE211E 文档 / adapter reload 测试。
4. baseline 后停止，不进入 Phase 2.55、不真实 upload、不进入 Data Steward。

## 最新状态

1. Phase 2.54c display-tail fix 已通过 Codex B review。
2. 已写入 Codex C 复测入口：`docs/NEXT_CODEX_C_PROMPT.md`。
3. 复测只验证 Q3 file answer metadata 的 `title/source_name/source_type/citation_count` 与 safety flags，不进入完整 Pilot smoke。
4. 复测通过后再决定 Phase 2.54c baseline；当前不进入 Phase 2.55。

## 最新状态

1. Phase 2.54c display-tail fix 已完成：file answer metadata diagnostics 增加 required fields / echo required / safety flags 邻近展示。
2. `source_name` 已增加 metadata fallback，避免 evidence 本身缺 source_name 时真实 CLI 无稳定 source/title 可回显。
3. 主仓目标测试通过：py_compile 通过，targeted pytest `74 passed`。
4. 下一步：Codex B review；通过后 Codex C 重跑 Q3 file answer metadata targeted smoke。本轮不 baseline、不进入 Phase 2.55。

## 最新状态

1. Phase 2.54c Codex C 真实终端复验已完成：Q1 alias missing 与 Q2 active document continuation 为 pass，Q3 file answer metadata 为 partial。
2. Q3 最小尾项：`document_id/version_id/citation_count` 可见，但 `source/title` 与 `metadata_as_answer=false` / `facts_as_answer=false` / `snapshot_as_answer=false` 未在最终 CLI 输出中稳定透出。
3. 已写入 Codex A 下一步 prompt：只做 File Steward UX display-tail fix，优先增强 `ContextBuilder` 中 file answer metadata 诊断文案与目标测试。
4. 本轮仍不进入真实 upload、Data Steward / BIM / NAS / TB 文件池、DB / index 写入、repair 或 rollout。

## 最新状态

1. Phase 2.54b baseline 已完成，当前进入 Phase 2.54c 真实终端展示复验。
2. Codex C 需验证 `File steward diagnostics` / 等价字段、`auto_bind_allowed=false`、`metadata_as_answer=false`、`requires_retrieval_evidence=true`。
3. 如果真实 CLI 只显示等价语义但未逐字显示字段，可判 partial；若 metadata / facts / transcript 替代 evidence 则 fail。
4. 本轮不写新功能、不进入真实 upload、不进入 Data Steward / BIM / NAS / TB 文件池。

## 最新状态

1. Phase 2.54b File Steward UX runtime display integration 已通过 Codex B review，下一步只做 selective Git baseline。
2. 主仓 `ContextBuilder` 已新增 `File steward diagnostics:`，展示 alias failure、active document continuation、file answer metadata。
3. 目标测试通过：主仓 py_compile 通过，`test_file_steward_ux.py test_session_document_scope.py test_facts_agent_context.py` 为 `73 passed`。
4. 本轮未接真实 upload、未调用 Hermes_memory API、未写 DB / OpenSearch / Qdrant、未进入 Data Steward。
5. 下一步只做 baseline；不自动进入 Phase 2.54c / 2.53d。

## 最新状态

1. Phase 2.54a Git baseline 已完成，当前进入 Phase 2.54b File Steward UX runtime display integration。
2. 2.54b 只允许把 helper 接入 `ContextBuilder` 的展示层，不改 retrieval contract。
3. 目标体验：alias 失败时给明确下一步；active document 可继续时给提示；文件回答显示 metadata 但不把 metadata 当 answer。
4. 继续固定 `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`、`metadata_as_answer=false`、`requires_retrieval_evidence=true`。
5. 真实 upload / Data Steward / DB-index 写入 / rollout 仍后置。

## 最新状态

1. Phase 2.53c 双仓 baseline 已完成：mocked natural import integration 已固化，但仍不等于真实 upload 能力。
2. 当前进入 Phase 2.54a Enterprise Memory Native UX / File Steward UX minimum implementation。
3. 2.54a 只允许新增纯 helper 与目标测试：alias failure helper、active document continuation hint、file answer metadata display structure。
4. 继续禁止真实 upload、API / CLI smoke、DB / index 写入、Data Steward / BIM / NAS / TB 文件池、repair 与 rollout。
5. Phase 2.53d 真实 upload smoke 仍需用户单独授权和小型非敏感文件。

## 最新状态

1. 已采纳本地 PR `LOCAL_PR_ENTERPRISE_MEMORY_USABILITY_PROPOSAL.md`：企业文件记忆 usability 成为后续主线，不再只围绕 alias 小修。
2. 新增 Phase 2.54 Enterprise Memory Native UX 规划：让 Hermes 更像原生知道“找文件、锁文件、围绕文件工作”是自己的核心能力。
3. 下一步 Phase 2.53c：mocked natural import integration + File Steward UX bridge；不真实上传。
4. 后续 Phase 2.54a：file discovery first / active document continuation / alias failure helper / file-answer ergonomics。
5. 继续禁止 production rollout、真实 upload、DB / index 写入、Data Steward / BIM / NAS / TB 文件池，除非进入单独授权阶段。

## 最新状态

1. Phase 2.53b planning 已通过 Codex B review，下一步只做 docs-only baseline。
2. Phase 2.53b baseline 只提交规划文档和交接文档，不提交代码、不运行 API / CLI smoke、不真实上传文件。
3. Phase 2.53c mocked adapter / kernel integration 是后续候选，必须在 baseline 后另行授权 / review。
4. Phase 2.53d 真实 upload smoke 仍需用户显式授权和小型非敏感文件。

## 最新状态

1. Phase 2.53b docs-only planning 已完成：新增 `docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md`。
2. 规划结论：自然语言导入 parser 应作为 import preflight layer，在普通 retrieval / answer flow 前执行。
3. 后续 Phase 2.53c 建议只做 mocked upload adapter / kernel integration tests，不真实上传。
4. 后续 Phase 2.53d 才可在用户显式授权后做小型非敏感文件真实 upload smoke。

## 最新状态

1. Phase 2.53a Git baseline 已完成：Hermes 主仓 commit `f15a56de7`，Hermes_memory commit `c841104`，tag `phase-2.53a-natural-file-import-parser-baseline`。
2. 当前进入 Phase 2.53b docs-only planning：自然语言导入 parser 如何接入 adapter / kernel / alias seed。
3. Phase 2.53b 仍不真实上传文件，不运行 API / CLI smoke，不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
4. Data Steward / 企业数据库 / BIM / NAS / TB 文件池继续后置，不进入当前自然语言单文件导入 MVP。

## 最新状态

1. Phase 2.53a Codex B review 已通过，下一步执行 selective Git baseline。
2. baseline 只纳入自然语言导入 parser / dry-run planner 与交接文档，不纳入 Data Steward、真实 upload、adapter / kernel integration 或无关 dirty。
3. baseline 后先等待 Codex B review，再决定 Phase 2.53b adapter / alias seed / kernel integration planning。
4. 真实文件上传、目录导入、NAS / TB BIM、Data Steward、DB / index 写入、repair、rollout 继续需要单独授权。

## 最新状态

1. Phase 2.53a Natural Language File Import Parser / Dry-run Planner review-fix 已完成，等待 Codex B review。
2. 已修复 `不要导入 / 不要上传 / 不要收录` 等否定 intent：parser 返回 `detected=false`，不会进入导入 dry-run。
3. 已恢复 out-of-scope tracked docs deletion：`docs/MAC_MINI_MVP_DEPLOYMENT_RUNBOOK.md`、`docs/MVP_PILOT_RUNBOOK.md`。
4. 主仓目标测试通过：py_compile passed，`tests/agent/test_natural_file_import.py` 为 `10 passed`。
5. adapter / alias seed / kernel integration 后置 Phase 2.53b；真实 upload smoke 需单独授权。


## 最新状态

1. Phase 2.50b internal MVP evidence pack planning 已完成，等待 Codex B review。
2. Evidence pack 被定义为内部受控 MVP 人工审阅证据包，不是 production rollout approval、customer delivery、automatic tender review、automatic bid、automatic business decision 或 repair authorization。
3. 本轮不生成真实 evidence pack、不读取真实 reports、不运行 API / CLI、不启动服务、不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
4. Phase 2.51a baseline 已完成：commit `1aa6807f38d5a9242640a6822d35aeacafc3dc22`，tag `phase-2.51a-fake-deployment-record-dry-run-baseline`。


## 0. 当前 MVP Pilot 状态

1. Phase 2.50c internal MVP evidence pack sanitized template 已完成，等待 Codex B review。
2. Evidence pack 最小组成已规划并模板化：canonical run record JSON、Phase 2.49 review payload/report、operator sign-off summary、issue intake / triage summary、Codex C smoke / Pilot summary、optional deployment summary 和 human notes。
3. 真实 evidence pack 默认放在 ignored local path，不提交 Git；本轮没有生成真实 pack。
4. Phase 2.51a fake deployment / internal MVP run record dry-run baseline 已完成：commit `1aa6807f38d5a9242640a6822d35aeacafc3dc22`，tag `phase-2.51a-fake-deployment-record-dry-run-baseline`。
5. Phase 2.51b Minimal Mac Mini Operator Command Sheet baseline 已完成：commit `f64c53d677b886694adf221aa72e0ad6e89c40c9`，tag `phase-2.51b-mac-mini-operator-command-sheet-baseline`。
6. Phase 2.51 Git baseline 已完成：commit `60b081acfa4771eaa5134be3cda2632885853663`，tag `phase-2.51-mac-mini-operator-runbook-baseline`。
7. Phase 2.50b 不新增 generator、不生成真实 evidence pack、不读取真实 reports / run records、不写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant。
8. 下一步：Codex B review Phase 2.50c templates；通过后只做 docs-only baseline，不进入真实 evidence generation、deployment、repair、rollout 或 Data Steward。
7. Phase 2.49 Internal MVP Run Record Review Bridge review-fix 已通过 Codex B 复审并已完成 Git baseline。
2. 新增本地只读 runner：`scripts/phase249_internal_mvp_run_record_review.py`，必须显式传入 `--input-run-record`，不默认扫描真实 `reports/`。
3. runner 输出 sanitized review payload，可选 `--review-report` 调用 Phase 2.42a review dry-run report builder；固定 `dry_run=true`、`production_rollout=false`、`repair_authorized=false`、`destructive_actions=[]`、`data_mutation=false`。
4. unsafe signals：`facts_as_answer=true`、`transcript_as_fact=true`、`snapshot_as_answer=true`、第三文件污染、P0 issue => P0 / `no_go`；未复核 alias missing、retrieval suppressed、隐藏 Missing Evidence => `pause`。
5. Review-fix 已修复：count-only `issue_summary.p0_count` 不再被忽略；repair/data mutation boundary false 不再允许 `decision_hint=go`。
6. 本轮未读取真实 run record、未运行 API / CLI、未写 DB / facts / document_versions / audit_logs / OpenSearch / Qdrant，不进入 rollout、repair 或 Data Steward。
7. 下一步：Phase 2.49 Git baseline，不进入 Phase 2.50。
7. Phase 2.48b Meeting Transcript Boundary Trace Display Polish 已完成并通过 Codex B review。
2. Hermes 主仓库 `ContextBuilder` 现在会在会议纪要证据场景输出独立 `Meeting transcript diagnostics:` 分区。
3. meeting diagnostics 稳定显示 `meeting_transcript_used=true`、`transcript_as_fact=false`、`evidence_required=true`、`meeting_transcript_as_confirmed_fact=false`。
4. Phase 2.48b 不改 meeting ingestion contract / retrieval contract / memory kernel 主架构，不运行 smoke，不写 DB / facts / document_versions / OpenSearch / Qdrant。
5. Phase 2.48a Excel Citation Display Polish 已完成，Codex B review 通过。
6. Excel citation display 已区分 `citation_precision=cell_range`、`citation_precision=multi_row_range`、`row_range_fallback=true` 与 `citation_precision=row_range_fallback`。
7. 当前结论：内部受控 MVP 可以继续；production rollout、客户交付、自动审标、自动投标、自动经营决策仍禁止。
8. Codex C targeted smoke 已通过；下一步执行 Phase 2.48a / 2.48b combined Git baseline，不进入 Phase 2.49。
9. Phase 2.47 combined docs artifact baseline 已完成：commit `bfe7981`，tag `phase-2.47-internal-mvp-operating-artifacts-baseline`。
10. Phase 2.47 planning、2.47a checklist、2.47b run record template 已形成可复用 docs artifact 包。
11. Phase 2.46d Mac mini local MVP smoke result baseline 已完成：commit `255c2e97fa6d644c2d83655e7ac919c8401f54f2`，tag `phase-2.46d-mac-mini-local-mvp-smoke-result-baseline`。
12. Codex C smoke 结果：`Go`，P0=0，P1=0，P2=2；只代表 internal controlled MVP continuation，不代表 production rollout。
6. Phase 2.46c prompt artifact baseline 已完成：commit `595c51d`，tag `phase-2.46c-codex-c-mac-mini-smoke-prompt-baseline`。
7. Phase 2.46b Mac mini evidence attachment planning Git baseline 已完成：commit `01af018`，tag `phase-2.46b-mac-mini-evidence-attachment-plan-baseline`。
8. Phase 2.46a Mac mini Day-0 setup checklist artifact Git baseline 已完成：commit `e78c08e`，tag `phase-2.46a-mac-mini-day0-checklist-baseline`。
9. Phase 2.46 Mac mini Day-0 real-machine setup / internal MVP application prep planning Git baseline 已完成：commit `13e2206`，tag `phase-2.46-mac-mini-day0-setup-plan-baseline`。
10. Phase 2.45e sanitized deployment record template artifact Git baseline 已完成：commit `8bd7616`，tag `phase-2.45e-deployment-record-template-baseline`。
5. Phase 2.45d Mac mini real-machine deployment record docs-only Git baseline 已完成：commit `e12f82a`，tag `phase-2.45d-deployment-record-plan-baseline`。
6. Phase 2.45c read-only health-check script Git baseline 已完成：commit `fbad94f`，tag `phase-2.45c-health-check-dry-run-baseline`。
7. Phase 2.45c runner 默认不访问真实 API / CLI，不执行真实 Mac mini 部署。
8. Phase 2.45b health-check / deploy-smoke dry-run planning Git baseline 已完成：commit `d70497c`，tag `phase-2.45b-health-check-dry-run-plan-baseline`。
9. Phase 2.45a Mac mini MVP deployment runbook artifact Git baseline 已完成：commit `585d534`，tag `phase-2.45a-mac-mini-deployment-runbook-baseline`。
10. Phase 2.45a runbook 是 Mac mini 到货后的人工部署前 checklist / 操作签核表，不是 deployment script 或 production rollout。
11. Phase 2.45 Mac mini MVP server deployment planning Git baseline 已完成：commit `fa6aff4`，tag `phase-2.45-mac-mini-mvp-server-plan-baseline`。
12. Mac mini 到货不等于 production rollout ready；Day-0 仍必须人工 operator 执行并保留 stop conditions。
11. 遗留无关 dirty `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` 不得被 Phase 2.46 baseline stage / commit。
11. 继续禁止真实 tracked issue records、默认扫描真实 `reports/` / `reviews/`、DB / facts / document_versions / OpenSearch / Qdrant 写入、repair / rollout / Data Steward。
12. Phase 2.44c fake/temp-data sanitized issue intake dry-run artifact Git baseline 已完成：commit `cb29ed4`，tag `phase-2.44c-fake-issue-intake-dry-run-baseline`。
13. Phase 2.44b sanitized issue intake dry-run / recorder workflow planning Git baseline 已完成：commit `0241c4d`，tag `phase-2.44b-sanitized-issue-intake-dry-run-plan-baseline`。
14. Phase 2.44a MVP Pilot issue intake worksheet / sanitized template artifact Git baseline 已完成：commit `14c5640`，tag `phase-2.44a-pilot-issue-intake-worksheet-baseline`。
4. Phase 2.44 MVP Pilot continuation / issue intake planning Git baseline 已完成：commit `afb5a29`，tag `phase-2.44-pilot-continuation-issue-intake-plan-baseline`。
5. Phase 2.34 compare false-positive baseline 已完成：Hermes_memory commit `789ed22`，Hermes 主仓库 commit `5de49bf5`，tag `phase-2.34-compare-contamination-baseline`。
6. Phase 2.37 planning baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
7. Phase 2.37a / 2.37b / 2.37c 已完成 intake、runbook 与 triage summary planning baseline。
8. Phase 2.37d triage summary generator baseline 已完成：commit `d97a67c`，tag `phase-2.37d-pilot-triage-summary-baseline`。
9. Phase 2.38a Tender P1 Source Availability Audit baseline 已完成：commit `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。
10. Phase 2.39 Data Steward / BIM 数据管家 docs-only baseline 已完成：Data Steward 明确作为后置产品线，不并入当前 MVP Pilot，不新增 DB schema、Neo4j、PostGIS、空间索引代码或 scheduler。
11. Phase 2.38b Git baseline 已完成：commit `a8c93f1`，tag `phase-2.38b-tender-recall-diagnostics-baseline`。
12. Phase 2.38c 人员要求召回尾项规划 baseline 已完成：commit `ff49941`，tag `phase-2.38c-personnel-recall-tail-plan-baseline`。
13. Phase 2.38d personnel-only bounded recall implementation baseline 已完成；Codex C Q1/Q2/Q3 真实终端复验通过。
14. Phase 2.40 PRD Acceptance Matrix / MVP Evidence Pack planning baseline 已完成：commit `1383155`，tag `phase-2.40-prd-acceptance-matrix-plan-baseline`。
15. Phase 2.40a docs-only artifact baseline 已完成：commit `e6f7fc2`，tag `phase-2.40a-prd-acceptance-matrix-artifact-baseline`。
16. Phase 2.41 MVP Pilot Evidence Review / Go-No-Go planning baseline 已完成，Phase 2.41a checklist artifact baseline 已完成。
17. Phase 2.42 MVP Pilot Review Dry-run Report Planning 已完成，Codex B review 确认主线方向正确。
18. Phase 2.42a MVP Pilot Review Dry-run Report Generator baseline 已完成：commit `4c60b28`，tag `phase-2.42a-mvp-pilot-review-dry-run-generator-baseline`。
19. Phase 2.42b sanitized input template / dry-run runbook artifact baseline 已完成：commit `edd0e08`，tag `phase-2.42b-mvp-pilot-review-dry-run-template-baseline`。
20. Phase 2.43 Internal MVP Pilot Launch Candidate Planning 已完成并 baseline：commit `5141bb5`，tag `phase-2.43-mvp-pilot-launch-candidate-plan-baseline`。
21. Phase 2.43a MVP Pilot Launch Packet / Operator Checklist artifact 已完成并 baseline：commit `5423497`，tag `phase-2.43a-mvp-pilot-launch-packet-baseline`；未启动真实 Pilot、不生成真实 report、不运行 API / CLI、不写 DB、不进入 rollout、repair 或 Data Steward 实现。
22. Phase 2.43b MVP Pilot Pre-flight Smoke Prompt / Runbook artifact 已完成并 baseline：commit `ef2e43f`，tag `phase-2.43b-mvp-pilot-preflight-smoke-prompt-baseline`。
23. Codex C pre-flight smoke 已完成并返回 `Go`：API / CLI 可用，四个 alias 稳定，P0 为 0；P1 为主标书最高投标限价 / 招标控制价 Missing Evidence，P2 为部分 trace 字段未显式打印。
24. Day-1 Pilot 已开始但按 run sheet 触发 `Pause`：`@主标书` 绑定阶段出现 `alias_bind_failed`，正式 Q1 变为 `alias_missing=true / retrieval_suppressed=true`，Q2-Q10 未继续执行。
25. Phase 2.43d `@主标书` alias/session bounded fix 已完成：current bind fallback 遇到多 retrieval 候选时采用 top document 完成绑定并记录歧义诊断，title bind 多候选仍保持失败；主仓 session scope 测试 `51 passed`。
26. Codex C Day-1 断点续跑已通过：session `20260506_143354_d4ad05`，`@主标书` Q1-Q2 resolved，`alias_missing=false`，`retrieval_suppressed=false`；10 条 query 为 `6 pass / 4 partial / 0 fail`，P0 为 0，Decision 为 `Go`。
27. Phase 2.43d 双仓 Git baseline 已完成：Hermes_memory commit `d62852b`，Hermes 主仓库 commit `9e8e5667`，tag `phase-2.43d-main-tender-alias-session-baseline`。
28. Day-1 issue candidates 已记录：限价 Missing Evidence、主标书资质 / 项目经理 / 联合体 / 业绩 / 人员深层字段人工复核、Excel cell citation 降级、公司方向人工决策复核、trace display UX。
29. Codex B review Phase 2.44 planning 已通过：规划只记录 issue intake / continuation 边界，不进入实现、真实 report、真实 issue records、repair、rollout 或 Data Steward。
30. 下一步不得直接启动 production rollout、repair、Data Steward 实现、DB schema、Neo4j、PostGIS、空间索引或 scheduler 工作。

## 0.1 Phase 2.38b 当前待办

1. Phase 2.38b 新增只读 concrete recall diagnostics runner，判断 concrete candidate chunks 是 top-k、低排名存在，还是检索缺失。
2. 目标测试已通过：py_compile 通过，`tests/test_phase238b_tender_concrete_recall_diagnostics.py` 为 `9 passed`，`git diff --check` 通过。
3. live read-only preview 结果：资质 `candidate_in_top_k`，业绩 `candidate_in_top_k`，人员 `candidate_present_but_low_rank`。
4. `price_ceiling` 固定为 `field_should_remain_missing_evidence`，继续 Missing Evidence / 人工补源，不进入召回修复。
5. `project_manager_level` 固定为 `field_requires_human_review`，继续人工复核，不得从电子证书 / 材料条款推断等级。
6. 不直接修改 retrieval ranking，不改 retrieval contract / memory kernel，不进入 repair、backfill、reindex、rollout 或自动审标。
7. Git baseline 已完成：commit `a8c93f1`，tag `phase-2.38b-tender-recall-diagnostics-baseline`。
8. 下一步：Phase 2.38c 只规划 `personnel_requirement` 低排名尾项；限价与项目经理等级继续后置 / 人工复核。

## 0.1.1 Phase 2.38c 当前待办

1. Phase 2.38c docs-only planning 已完成，新增 `docs/PHASE238C_PERSONNEL_RECALL_TAIL_PLAN.md`。
2. 结论：`personnel_requirement` 是 candidate present but low-rank，偏 query/profile/candidate-pool tail，不是 source missing。
3. 推荐后续 Phase 2.38d 仅做 personnel-only bounded recall implementation。
4. 可选实现边界：personnel-specific aliases、section hints、candidate-pool diagnostics、before/after visibility。
5. 继续后置：限价缺具体金额、项目经理等级人工复核、broad retrieval tuning、自动审标、repair、rollout。
6. Codex B review 已通过；Phase 2.38c docs baseline 已完成：commit `ff49941`，tag `phase-2.38c-personnel-recall-tail-plan-baseline`。

## 0.1.2 Phase 2.38d 当前待办

1. Phase 2.38d 首轮实现已完成，Codex B review finding 已做最小修复，并通过 Codex B 复审。
2. Codex C 定向复验显示：retrieval / trace 层已通过，Q1/Q2 为 `personnel_scope`，Q3 broad query 为 `qualification_scope`。
3. Q1/Q2/Q3 当前阻塞转为最终回答边界：项目经理 / 一级建造师 / “每类1人”仍可能与 Missing Evidence 并存。
4. answer-boundary 第二轮最小修复已完成：主仓库 `personnel_scope` context block 明确人员-only 不得混入项目经理 / 注册建造师 / 一级建造师 / B证 / 安全考核证 / 投标资质 / 联合体 / 类似工程业绩，且不得从角色列表推断“每个项目只能1个 / 每类1人 / 至少各1名”。
5. 即使 citation chunk 同时混有人员信息和项目经理 / 资质 / 联合体 / 业绩信息，personnel-only 回答也必须只抽取人员部分。
6. 第三轮最小修复已补结构化 guard lines：`personnel_forbidden_answer_terms`、`personnel_count_inference_forbidden=true`、`ignore_non_personnel_content_in_mixed_chunks=true`。
7. 第四轮最小修复已补 safe fallback contract：`personnel_violation_if_answer_contains_forbidden_term=true`、`personnel_violation_if_answer_contains_inferred_count=true`、`personnel_safe_fallback_required_on_violation=true`，违规时要求丢弃草稿并输出 Missing Evidence / 人工复核模板。
8. 第五轮 runtime guard 已接入 `run_agent.py` 最终输出路径：personnel-only 违规答案会被替换为 Missing Evidence / 人工复核 safe fallback。
9. broad query `投标资质、项目经理、联合体、业绩、人员要求分别是什么？` 仍必须保持 `qualification_scope`，不得误套 personnel-only boundary。
10. `price_ceiling` 继续 Missing Evidence，`project_manager_level` 继续 human-review-only。
11. 主仓库目标测试已通过：py_compile 通过，`tests/agent/test_structured_citation_context.py tests/agent/test_session_document_scope.py` 为 `65 passed`。
12. Codex C 真实终端复验已通过：Q1/Q2 personnel-only safe fallback 触发且无禁词 / 数量推断，Q3 broad qualification 未被压扁；本轮进入 Phase 2.38d Git baseline，不进入 Phase 2.38e。

## 0.2 Phase 2.38a 历史状态

1. 新增只读 source availability audit runner，用于判断主标书 P1 字段是 concrete source、anchor-only、not found、ambiguous 还是 live skipped。
2. 字段覆盖：最高投标限价 / 招标控制价 / 投标报价上限、投标资质具体等级 + 类别、项目经理等级、类似业绩、人员要求。
3. 目标测试已通过：py_compile 通过，`tests/test_phase238a_tender_p1_source_audit.py` 为 `10 passed`。
4. 首轮 live read-only dry-run 因 `.env` 指向 `postgres` 主机名不可解析返回 `skipped_live_unavailable`。
5. Git baseline 已完成：commit `456b32d`，tag `phase-2.38a-tender-p1-source-audit-baseline`。

## 0.3 Phase 2.37d 历史状态

1. 本地 triage summary generator 已实现：读取 `reports/pilot_issues/*.json`，输出 dry-run JSON summary，可选写入 ignored 的 `reports/pilot_triage/*.json/*.md`。
2. 输出字段固定保留 `dry_run=true`、`destructive_actions=[]`、`writes_db=false`、`creates_external_issue=false`、`repairs_issue=false`、`rollout_approved=false`。
3. P0 => `pause`，P1 无 P0 => `continue_with_manual_review`，仅 P2/P3 或空输入 => `continue`。
4. Markdown summary 明确不是 repair 结果、不是 rollout approval，P1 需人工 review，Missing Evidence 不得被隐藏或改写。
5. 目标测试已通过：py_compile 通过，`tests/test_phase237d_pilot_triage_summary.py` 为 `9 passed`，`git diff --check` 通过。
6. 下一步：Codex B review；通过后只做 Phase 2.37d Git baseline，不直接进入 P1 retrieval fix、repair 或 rollout。

## 0.4 Phase 2.35 当前待办

1. Codex C 真实终端复验已完成：安全边界通过，但整体仍为 partial。
2. Phase 2.35b 已完成最小修复：API trace 顶层暴露 `metadata_guided_query_profile` / `metadata_deep_field_profile`，Q1/Q2 应可直接核对 `pricing_scope` / `qualification_scope`。
3. 最高投标限价 / 招标控制价 / 投标报价上限：metadata anchor 已要求具体金额 / 货币 / 万元 / 元；如真实标书仍无具体金额，必须继续 Missing Evidence。
4. 投标资质：metadata anchor 已要求具体资质等级 + 类别；证照清单不再强标为资质等级命中。
5. 项目经理、联合体、业绩、人员要求：已有相关 evidence，但仍为 partial，需要 Codex C 继续按 Missing Evidence / 人工复核口径验证。
6. 首次 session alias 绑定后丢失：主仓库 direct assertion diagnostics 未复现，暂作为 terminal-only tail，不能盲目大改。
7. 下一步：补全指定测试复跑后交 Codex B review；通过后由 Codex C 重跑 Day-1 Q1/Q2。

## 0.5 Phase 2.34 历史状态

1. Phase 2.33 Day-1 run sheet baseline 已完成：commit `bb9656b`，tag `phase-2.33-pilot-day1-run-sheet-baseline`。
2. Codex C Day-1 真实终端验收：`7 pass / 3 partial / 0 fail`，P0 为 `0`，四个 alias 后续解析稳定，无 facts 替代 evidence，无 transcript_as_fact，无实际第三文件污染。
3. 当前建议继续内部受控 Day-1 Pilot，但不得进入 production rollout 或自动经营决策。
4. 当前 Phase 2.34 优先处理 P1：`@会议纪要 vs @主标书` compare 输出层误报 `third_document_mixed=true`。实际 evidence 仅来自两份目标文档，属于 contamination / UX false-positive。
5. 主标书最高投标限价、资质等级、业绩、人员数量等深层字段召回仍为 P1 retrieval recall backlog；本轮不顺手扩大实现。
6. 会议纪要决策 / 公司方向分析长输出延迟为 P2 backlog；本轮不顺手优化。

## 1. Phase 2.1-Qdrant 未确认项

1. Qdrant 是否需要 `QDRANT_API_KEY`、以及 `api-key` header 是否生效尚未确认；当前仅验证了无鉴权的本地容器路径。
2. Dockerfile 依赖 `python:3.11-slim` 拉取在部分网络环境可能超时（docker.io oauth token timeout），导致 `docker compose build api` 失败；若团队主路径依赖容器构建，需准备镜像源/网络策略或提供替代运行方式。

## 2. 暂不推进事项

- production rollout
- repair executor / destructive repair / cleanup / delete
- facts 自动抽取
- facts 替代 retrieval evidence 或 final answer
- 完整 RBAC / ABAC / SSO / 管理后台
- OCR / ASR 全量化
- 全局 rerank rollout / 排序收益大规模优化
- 默认扫描真实 reports / reviews
- TB 级 BIM 原始模型内容全量解析、在线查看器、碰撞检测、自动算量、自动设计审查

说明：上述事项并非长期放弃，而是不进入当前 MVP Pilot / issue intake 阶段。当前已具备 rerank smoke、dense ingestion、facts governance、audit、version governance 与多模态 MVP 的阶段闭环；下一步重点是把真实试用反馈结构化分流，不扩大到 rollout 或自动修复。

## 0.5 Data Steward / BIM 数据管家后置规划

1. PRD 已将 BIM 数据管家扩展为 Data Steward 后置产品线：Hermes 初期只管理数据资产目录、版本、权限、项目归属、责任人、检索、引用和后续解析入口。
2. BIM 是 Data Steward 的首个高价值垂直场景；最小元数据包括项目、楼栋、楼层、空间、专业、系统、模型类型、版本、路径 / 存储位置、文件大小、hash、创建 / 修改时间、责任人和权限标签。
3. Data Steward 四层规划为文件资产目录、建筑本体、知识图谱和空间索引；Agent 层规划为 Supervisor、Catalog、Ontology、Spatial Index、Monitoring 和 Review。
4. 原始 BIM 模型、点云和 IoT 实时流不直接进入 LLM 上下文；Hermes 只保存元数据、派生文本、结构化属性、空间索引 metadata 和可追溯链接。
5. 当前只做产品规划，不新增 DB schema、Neo4j、PostGIS、空间索引代码或 agent scheduler；后续可单独规划 `Data Steward / Building Asset Catalog MVP`。
6. 当前主线仍是 Phase 2.38d / MVP Pilot，Data Steward 不进入当前实现资源池，不得影响审标 MVP 收口。

## 3. Phase 2.2 后续待办

1. 本节为历史状态归档。Phase 2.2 当时仅完成 `NoopReranker` 与 rerank hook，真实 provider、灰度与质量评测尚未完成。
2. 后续 Phase 2.3-2.8 已完成 rerank 局部默认启用、灰度观察、fail-open 与长期窗口验证。
3. Phase 2.9d 已完成 Aliyun embedding / rerank provider 首轮真调用，其中 rerank 使用 embedding key fallback 调用 `gte-rerank-v2`。
4. Phase 2.17 已完成 Rerank Smoke Audit 与 dense / hybrid eval 扩展，确认真实调用、合理 skipped、latency / fail-open 可观测。
5. 当前保留尾项不是“真实 reranker 未接入”，而是专用 `ALIYUN_RERANK_API_KEY` smoke 与排序收益专项评测；全局 rerank rollout 与排序策略优化继续后置。

## 4. Phase 2.3 待办

1. 当前黄金 query 已扩到 48 条，但样本仍以脱敏近真实评测语料为主，不是完整真实企业知识库；进入更大范围 rollout 前仍需补更大范围的真实业务 query 集。
2. rerank candidate 扩大策略尚未进入代码。当前只使用 `RERANK_INPUT_CAP` 截断，未实现 dense/sparse 内部 candidate target 扩大。
3. BGE / cross-encoder 只作为备选路线记录，当前不实现。
4. 当前 baseline vs experiment 已覆盖 48 条小规模样本，top-1 有提升且无回归，已足以支持“默认启用策略评估”，但仍不足以直接作为全局默认启用依据。
5. 默认启用实施前仍需补充 rollout policy 落地：按 query 类型灰度、超时阈值、成本观测和回退开关。
6. Phase 2.5 已落地局部默认启用规则，但当前只覆盖招标资料中的高收益 query；扩大范围前仍需更大规模真实 query 复测。
7. 需要补最小运行手册：灰度开关切换、timeout 观察、fail-open 监控与回滚步骤。
8. Phase 2.6 环境阻塞已解除：Docker daemon、Qdrant、OpenSearch 已恢复，灰度验证脚本可正常运行。
9. Phase 2.6 已修正灰度脚本的 request 上下文传递，当前局部默认启用可命中目标 query；后续应继续观察真实灰度下的 fail-open rate、p95/p99 与收益稳定性。
10. Phase 2.8 已完成退出标准与最后观察窗口判定：最后 `3` 次完整观察满足运行基线稳定、回退稳定、延迟可接受和后端异常窗口可控标准，Phase 2.8 已收口。Phase 2.9a 受控环境重跑显示：前一轮长窗口异常未在更干净环境中复现，dense / sparse 失败与 OpenSearch 超时均恢复为 `0`，命中集恢复稳定；当前更可能是 Mac Air 8GB 的本机资源瓶颈与并行负载放大了异常。Phase 2.9b 长窗口压力验证进一步表明：加装散热器后，Air 可稳定承载 `8` 次窗口，也可跑完 `12` 次窗口，但长窗口下会出现明显 `p99` 长尾尖峰；当前更像宿主机内存 / swap 与 Docker 资源竞争带来的长尾抖动，而不是业务链路失稳。该判断已由后续 Windows + WSL2 高可信补证承接，最终见 Phase 2.9c 条目。
11. Phase 2.9 后续默认采用“白天继续主线开发，晚上或空闲窗口跑长窗口验证”的节奏，避免重度验证打断主线。与此同时，可开始小批量、脱敏、低敏企业资料的受控验证，但不得改变当前规则、启用范围或 rollout readiness 主线判断。

## 5. Phase 2.9 真实文件测试后续待办

1. 增强大型标书深层结构化章节召回能力。当前在 800+ 页真实标书中，资质等级门槛、项目经理执业资格、总工期、里程碑节点、付款节点 / 支付比例、结算方式、缺陷责任期 / 质保金 / 保留金、延期误期赔偿、不平衡报价处置标准等核心参数仍无法稳定召回；下一步应优先增强“投标人须知前附表 / 资格审查 / 资信标 / 合同专用条款 / 工程量清单 / 限价明细”的章节定向检索能力。
2. 明确当前检索能力仍偏“初筛”，尚未达到完整审标。当前可稳定覆盖约 60%～70% 的高价值审标条款，但仍缺约 30%～40% 的核心商务 / 合同 / 资审参数；在补齐结构化召回前，暂不应宣称已具备“完整 AI 审标自动化能力”。
3. dense ingestion 未接通是 Phase 2.9 时的历史问题；已在 Phase 2.16 修复。当前新上传 dense ingestion、显式 backfill 与 6 文件真实池回填已完成；后续尾项是 eval 覆盖、回填策略治理和环境配置一致性。
4. 高可信度灰度测试已完成阶段补证。Windows + WSL2 高可信验证中，长窗口 `20/20` 成功，OpenSearch timeout / dense_failed_count / sparse_failed_count / 命中漂移 / 后端异常窗口均为 `0`；连续真实工作流 `30` 次 retrieval + `30` 次 agent ask 共 `60/60` 成功，document_id / 标题收敛失败与错误文档命中均为 `0`。该结论支撑 Phase 2.9c 稳定性收口，但仍不等同于生产级全面 rollout。
5. 下一步主线不再继续拆 Phase 2.9c 小轮，建议进入非阻塞尾项收敛：继续扩样验证“投标人须知前附表 / 资格审查 / 合同专用条款 / 工程量清单 / 限价明细”相关真实问法，并补 Aliyun embedding / rerank provider smoke。
6. Phase 2.9c 第一轮与第二轮结构化章节增强已证明方向有效：资质等级门槛、项目经理执业门槛、不平衡报价类查询已能更稳定收敛到“资格后审 / 资格审查文件 / 工程量清单”；付款节点、结算方式、缺陷责任期、质保金、误期赔偿已开始稳定打到“第三章 招标人对招标文件及合同范本的补充/修改”，但仍未证明能稳定命中最理想的合同专用条款 chunk。
7. 总工期 / 关键节点方向已从“明显打不进去”提升到“有提升但仍不稳定”。当前代表性查询能将目标 `工期要求` chunk 拉到 top1，但仍需更多真实问法扩样确认，不应直接宣称稳定够用。
8. 多文件连续切换稳定性已补证。Windows 连续真实工作流中 document_id / 标题收敛失败为 `0`、错误文档命中为 `0`，当前可作为 Phase 2.9c 收口证据。
9. 高可信度灰度证据已补齐到 Phase 2.9c 阶段可接受。Windows 长窗口 wall `p95/p99 = 2397.266 ms / 2596.483 ms`；连续真实工作流 `p95/p99 = 34.935 ms / 40.929 ms`。Aliyun embedding / rerank 当时因缺 secret 未真实调用，该历史尾项已由 Phase 2.9d 首轮真调用承接；当前仅保留专用 `ALIYUN_RERANK_API_KEY` smoke 为可选后置项。
10. 当前仍需继续作为质量尾项扩样的是“前附表 / 工期节点”。合同专用条款方向已开始逼近并出现真实命中提升；“总工期 / 关键节点 / 计划开工日期 / 计划竣工日期”已出现 top 结果改善，但仍未证明所有真实问法都稳定够用。
11. Phase 2.9c 最终收口判断：建议收口。`总工期 / 关键节点` 已从“明显打不进去”提升到“有提升但仍不稳定”，可作为质量尾项继续扩样；高可信机器长窗口与连续真实工作流补证已完成，稳定性阻塞已解除。
12. Phase 2.9c 后续不再继续拆小轮推进。下一阶段建议限定为非阻塞尾项收敛：继续扩样验证 `总工期 / 关键节点` 真实问法，并补 Aliyun embedding / rerank provider smoke；不得误判为生产级全面 rollout。
13. Phase 2.9c 新增兼容性回归修复项已完成：`RetrievalService.search()` 引入 `_infer_document_scope()` 后曾打断 `db=None` 路径，导致 `phase26_rerank_gray_validation.py` 报 `NoneType.query`。当前已在 service 层恢复无 DB 安全返回，并补上 `_database_fallback_search()` 的无 DB 保护；后续仍需持续把无 DB 评估脚本纳入最小回归保护，避免再次误判成环境问题。
14. 总工期 / 关键节点 不再作为 Phase 2.9c 稳定性收口阻塞。本轮增加 schedule 参数短语精确加权后，真实大标书查询已能把 `工期要求` 目标 chunk 提升到 top1，`施工工期 / 合同工期` 定义 chunk 提升到 top2，技术要求进度段落被压到更后；当前判定为“有提升但仍不稳定”，转入后续质量尾项。
15. Windows 高可信灰度补证已完成：长窗口 `20/20` 成功，连续真实工作流 `60/60` 成功；`OpenSearch timeout = 0`、`dense_failed_count = 0`、`sparse_failed_count = 0`、命中集漂移 `0`、后端异常窗口 `0`、document_id / 标题收敛失败 `0`、错误文档命中 `0`。Aliyun embedding / rerank 缺 secret 是当时历史状态，已由 Phase 2.9d provider smoke 首轮真调用补齐；专用 rerank key smoke 仍可选后置。
16. Phase 2.9d 非阻塞尾项已完成首轮收敛：Aliyun embedding 真调用返回 `executed` 与 `1024` 维向量；Aliyun rerank 使用 `ALIYUN_EMBEDDING_API_KEY` fallback 真调用 `gte-rerank-v2` 返回 `executed`，top chunk 正确；大型标书 `总工期 / 关键节点` 10 条真实问法扩样全部命中 `工期要求` 目标 chunk。后续若要求专用 rerank key，需单独补 `ALIYUN_RERANK_API_KEY` 专用 key smoke。
17. Phase 2.9d 文档基线已固化：Phase 2.9c 已收口，Phase 2.9d 首轮尾项已完成；当前仍不进入生产级 rollout。PRD 核心缺口继续保留为未完成：dense ingestion、结构化事实层、会话记忆层、权限治理层、增量更新闭环、审计日志闭环、完整评测系统、版本治理增强、知识管理员后台、人工校验机制。

## 6. Phase 2.10+ 企业级 Agent 长期能力候选

1. Phase 2.10 优先处理 Enterprise Session Document Scope：同一 Hermes 会话内维护 active document scope，支持文件切换、上下文防污染和多文件对比，不再依赖新开会话作为产品方案。
2. Phase 2.11 进入规划阶段：企业会话上下文治理继续增强，并规划 Excel、PowerPoint、图片、扫描件和会议音频的企业级摄取策略；当前只明确数据模型、解析 provider、引用格式、权限、审计和评测方式，不直接实现完整 multimodal ingestion。
3. 后续候选 Phase 2.12：Excel / PowerPoint ingestion MVP。Excel 应保留 sheet、行列坐标、表头、公式、金额和单位；PowerPoint 应保留页码、标题、正文、备注、图表说明和图片 OCR。
4. 后续候选 Phase 2.13：Meeting Audio Memory MVP。支持会议录音转写、发言人、议题、决策点、行动项、风险和后续跟进事项沉淀，并与项目、客户、合同和结构化事实关联。
5. 长期目标是将 Hermes 从文档检索器升级为企业级 Agent 中枢，但所有高风险动作仍需人工确认；会议、经营、投标、财务和法务相关结论必须保留来源、引用、权限与审计。

## 7. Phase 2.11 当前待办

1. 企业上下文治理详细设计已补齐：明确 active document、project scope、compare scope、history memory 的优先级和防污染规则。
2. Excel / PPTX 摄取验收样本已补齐：覆盖 sheet/cell、slide/page、备注、图表说明、引用位置和权限标签。
3. 会议音频记忆验收样本已补齐：覆盖转写、说话人、时间戳、议题、决策、行动项、风险和人工确认边界。
4. Phase 2.11a 最小切口已评审：建议优先选择企业上下文治理增强，而不是 Excel/PPTX ingestion MVP。
5. Phase 2.11a 最小实现边界：project scope / task scope / active document / compare scope / history memory 优先级、evidence source trace、history memory 不得替代本轮 retrieval evidence、上下文污染诊断规则。
6. Phase 2.11a 最小实现已在 Hermes 主仓库完成；Hermes_memory 保持 stateless，未改 retrieval contract。
7. Phase 2.11a 已修复 `history_memory_as_evidence` 语义错误：历史记忆可作为提示，但不得替代本轮 retrieval evidence。
8. Phase 2.11a 真实终端验收已通过：A 锁定、刚才文件延续、A/B 对比均无历史记忆伪 evidence 或第三文件污染。
9. Phase 2.11a 非目标：不实现 Excel/PPTX parser，不实现 OCR/ASR，不推进 facts、权限大改或 rollout。
10. 保留 dirty 声明：Hermes 主仓库 `uv.lock` 不处理；`tests/agent/test_memory_kernel_adapter_reload.py` 作为后续候选回归测试确认。
11. Phase 2.11b 已在 Hermes 主仓库完成 session-level 企业文件别名最小实现：alias 绑定 `document_id`，支持使用与对比；Hermes_memory 继续保持 stateless，不改 retrieval contract。
12. Phase 2.11b 已修复真实终端 alias 绑定路径：绑定在 Hermes 会话层完成，不依赖模型工具；Hermes_memory 侧无需变更。
13. Phase 2.11b 真实终端验收已通过：`@主标书` / `@交付标准` 绑定、使用、对比与 missing alias 抑制均通过；基础信息召回质量尾项不属于 alias 功能失败。
14. Phase 2.11c 已完成规划：优先用轻量 tender metadata snapshot 辅助基础信息召回，再配合 query profile / section boost；snapshot 不替代 evidence。
15. Phase 2.11c 最小实现已完成：Hermes_memory 新增轻量 `tender_metadata_snapshot` 导航，基础信息 query 可锚定工程地点、建设单位、代建单位等来源 chunk；真实大标书复测中三类 query 均返回目标 `document_id`，top1 不再落到第八章工程量清单。
16. Phase 2.11c 真实终端验收已通过：`@主标书` 绑定到 `869d4684-0a98-4825-bc72-ada65c15cfc9`，工程地点 / 建设单位 / 代建单位均由 metadata snapshot 导航到目标 evidence chunk。
17. Phase 2.11c trace 语义已验收：`metadata_snapshot_used=true`、`evidence_required=true`、`snapshot_as_answer=false`，最终答案由 retrieval evidence 支撑，`contamination_flags=[]`。
18. Phase 2.11d 已进入规划：需要用 15 条综合回归 prompt 验证 active document、alias、compare、metadata snapshot、history memory 非 evidence 与 missing alias suppress retrieval 的组合稳定性。
19. Phase 2.11d 新数据需求：第二份大型标书、一份企业制度 / 合同类文件；Hermes_memory 侧需配合确认入库、索引与文件级检索可用。
20. Phase 2.11d 新增文件已完成入库：香港中文大学医学院智能化工程标书 `613` chunks、3-1 数字化交付标准 `20` chunks、会议纪要汇编 `17` chunks，均完成 OpenSearch 索引。
21. Phase 2.11d 综合回归已执行 15/15 通过；当前未发现大标书、交付标准、会议纪要之间的 document scope 污染。
22. Phase 2.11d 非阻塞尾项：multi-document compare 顶层 trace 暂不聚合每份文档的 metadata snapshot 字段；当前不影响 retrieval evidence 与防污染结论。
23. Phase 2.11e 已完成边界规划：PRD / Roadmap / Technical Design 建议单独纳入文档基线，Linear 协作文档单独纳入协作基线，`scripts/run_local_api.sh` 单独纳入 DX 工具，`.run/` 建议删除或忽略，`uv.lock` 保留到依赖治理阶段。
24. Phase 2.11e hygiene 收口：`.run/` 已确认为本地 API 日志与 pid 运行产物并加入 `.gitignore`；`uv.lock` 当前为未跟踪依赖解析产物，暂不纳入提交，后续应单独做依赖治理与 lockfile 策略确认。
25. Phase 2.12 已完成立项评审草案：Excel / PPTX ingestion MVP 应先完成依赖治理与样本确认；实现前需准备 2-3 个真实 Excel 与 2-3 个真实 PPTX，并以 sheet/cell range、slide citation 为最小验收边界。
26. Phase 2.12 前置依赖治理已裁决：`uv lock --check` 通过，`uv.lock` 未发现敏感信息或本地绝对路径，适合作为项目依赖锁定文件纳入基线；后续新增解析依赖必须同步更新 `pyproject.toml` 与 `uv.lock`。
27. Phase 2.12 Excel/PPTX ingestion MVP 已完成首轮最小闭环：3 个 Excel 与 3 个 PPTX 均完成上传、解析、chunk、OpenSearch 索引与带 document_id 的 sparse 检索验证。后续尾项：真实 Hermes 终端验收、图表深层数据还原、图片 OCR、dense ingestion 仍需单独推进。
28. Phase 2.12a Hermes 主仓库 structured citation 消费层已完成最小修复：Excel/PPTX retrieval 结果在 CLI 层可稳定展示结构化 citation；Hermes_memory 本轮无 parser/contract 变更，仅记录阶段联调状态。
29. Phase 2.12 真实终端验收已收口：Excel 文件锁定、Excel 单项检索、PPTX 文件锁定、PPTX 单页信息、跨类型防污染 `5/5` 通过；当前可进入 Git baseline，不再阻塞 Phase 2.12 收口。
30. Phase 2.12 后置 Git 核对完成：Hermes 主仓库 `origin` 是上游 HTTPS 远端，推送失败原因是 GitHub HTTPS 凭证不可读；`backup2` 是当前可写备份远端，Phase 2.12 branch/tag 已在 `backup2` 固化，不需要把 primary remote 对齐混入功能阶段。
31. Phase 2.13 建议优先规划会议纪要 / 转写文本 ingestion MVP：先支持 `.docx` / `.txt` / `.md` 会议资料的 speaker、timestamp、action item、decision、risk 抽取与 citation，不直接进入原始音频 ASR。
32. Phase 2.13 首轮最小实现已完成：复用现有 docx/txt/md parser，新增会议文本 metadata 提取与 retrieval-time 动态补齐；真实样本 `会议纪要汇编 (2)` 未重复上传，行动项 / 决策 / 风险 query 均可命中会议 evidence，主标书查询未被会议 metadata 污染。
33. Phase 2.13 trace 语义已修正：会议纪要可作为 retrieval evidence，但 `transcript_as_fact` 必须恒为 `false`；行动项 / 决策 / 风险不会被误标为已确认 facts。
34. Phase 2.13 真实终端验收已通过：`@主标书` 与 `@会议纪要` 均可绑定，行动项 / 决策 / 风险提取命中会议 evidence；会议纪要与主标书对比无 evidence 混用，会议内容不会被当作招标文件条款引用。
35. Phase 2.14 已完成边界规划：先建设 API-level deterministic regression eval，再补少量 Hermes CLI smoke；覆盖 document scope、alias、compare、metadata snapshot、Excel/PPTX citation、meeting transcript 与 evidence policy。
36. Phase 2.14 最小 API eval runner 已完成：内置 11 条 case，真实本地运行 `10 passed / 0 failed / 1 skipped`；missing alias suppress 保持 CLI-only skipped，后续应补少量 Hermes CLI smoke。
37. Phase 2.14b CLI smoke 已在 Hermes 主仓库收口；Hermes_memory 本轮不改 retrieval contract 或业务代码。真实 runner `4/4` 通过，覆盖 missing alias、session alias bind/use、A/B compare 与 meeting transcript 非 fact 语义。

## 8. Phase 2.15 状态审计与下一阶段路线

1. Phase 2.15 已完成项目状态审计：企业文档检索底座、企业上下文治理、Excel/PPTX、会议纪要文本、API eval、CLI smoke 均已形成阶段闭环。
2. 当前 PRD 核心缺口仍包括：dense ingestion、结构化事实层、权限治理、审计日志、增量更新、知识管理员后台、人工校验机制、完整 OCR / ASR 与生产级 rollout。
3. 推荐下一阶段进入 `Phase 2.16 dense ingestion 与 hybrid 检索闭环补齐`，先让真实上传文件进入 Qdrant dense 索引，再评估权限 / 审计 / facts。

## 9. Phase 2.16 dense ingestion 与 hybrid 闭环待办

1. 已完成新上传文件 dense ingestion 最小实现：chunk 落库后生成 Aliyun `text-embedding-v3` 1024 维向量，并 upsert 到 Qdrant `hermes_chunks`。
2. 已完成 dense fail-open：Qdrant 或 embedding 失败不阻断 PostgreSQL / OpenSearch sparse ingestion，并在 `DocumentVersion.metadata_json.dense_ingestion` 记录状态、成功数、失败数和原因。
3. 已新增显式 backfill 脚本 `scripts/phase216_dense_backfill.py`；脚本必须传入 `--document-id`，不允许默认全库扫描。
4. 已完成 smoke：新上传小文件 sparse + dense 均完成；答疑文件 `1db84714-d49f-48a2-8fa9-c6f73424dd32` dense backfill `12/12` 成功，dense-only retrieval 可返回真实候选。
5. 后续待办：按显式 document_id 分批回填 6 文件真实池 / Excel / PPTX 样本，并复跑 Phase 2.14 API eval 与关键 hybrid smoke。
6. Rerank Smoke Audit 作为非阻塞尾项单独登记：后续需验证 rerank provider 是否启用、真实模型调用是否发生、触发条件、fail-open / latency / error trace 可观测性，以及是否纳入 Phase 2.14 eval 或后续 Phase 2.17 质量评测；本轮 dense ingestion 不混入 rerank 策略修改。
7. Phase 2.16 真实文件池 dense backfill 已完成：6 文件共 `1360` chunks，attempted `1360`、succeeded `1360`、failed `0`；两份大标书分别耗时约 `287.230s` 与 `243.877s`。
8. Phase 2.16 hybrid smoke 已完成：6 文件均 `dense_status=executed`、`sparse_status=executed`，结果 document_id 均收敛到目标文件；Phase 2.14 API eval 复跑 `10 passed / 0 failed / 1 skipped`，`p50/p95=38.416ms/271.507ms`。
9. Phase 2.16 可进入收口判断；后续如继续推进，应优先将 dense/hybrid smoke 结构化纳入评测集，并单独处理 Rerank Smoke Audit。

## 10. Phase 2.17 Rerank Smoke Audit 与 dense/hybrid eval 扩展

1. 当前 rerank 默认仍是关闭状态：`rerank_enabled=false`、`rerank_provider=noop`、`rerank_default_enablement_enabled=false`；真实调用需显式启用 Aliyun provider 与局部默认启用。
2. Rerank 触发条件应保持现有策略：候选数达标、query 命中关键词、request 侧 source_type 或 route_type 命中目标范围；本阶段不改策略。
3. Phase 2.17 已新增 Rerank Smoke Audit runner，覆盖主标书基础信息、主标书工期 / 关键节点、答疑文件、Excel structured query、会议纪要 action/decision/risk；本地 live smoke `5 passed / 0 failed`，其中 3 条 tender query 真实调用 `aliyun_text_rerank`，Excel 与会议纪要按当前策略合理 skipped。
4. Phase 2.17 已扩展 Phase 2.14 eval，增加 `dense_status`、`dense_returned`、`sparse_status`、`candidate_pool` 检查；本地 live eval `11 passed / 0 failed / 1 skipped`，dense/hybrid 链路执行且 returned document_ids 未污染。
5. Phase 2.17 非目标：不调 rerank 策略、不改排序权重、不做 query rewrite、不进入 rollout。
6. 后续尾项：若要判断 rerank 排序收益，需要另起排序质量评测阶段；本阶段只确认真实调用、合理跳过、fail-open 与 dense/hybrid 可观测。

## 11. Phase 2.18 权限与审计路线待办

1. Phase 2.18 已完成路线评审：权限 / 审计的企业落地价值最高，且当前检索、上下文、多模态、dense、rerank、eval 底座已足以支撑最小治理闭环。
2. Phase 2.18a 最小实现已完成：支持 requester / tenant / role placeholder、document ACL metadata placeholder、allow / deny / not_configured_allow policy decision、retrieval trace 与 audit log。
3. 当前 policy 默认行为：无 ACL 本地默认 allow，并标记 `not_configured_allow`；显式 tenant mismatch 或 ACL 不匹配时 deny，且 denied document 不进入 results / evidence。
4. Audit 存储复用现有 `audit_logs` 表；audit 写入失败 fail-open，不阻断 retrieval。
5. Phase 2.18a live smoke 已通过：无 ACL 默认 allow、requester allow、tenant mismatch deny 与三条 audit log 写入均验证通过，测试文档 metadata 已恢复。
6. Phase 2.18a 非目标：不做完整 RBAC/ABAC、不接企业 IAM/SSO、不做管理后台、不做 facts、不做原始音频 ASR、不进入 rollout。
7. 下一步建议做 Git baseline；facts、增量更新 / 版本治理、原始音频 ASR、rerank 质量评测均保留为后续阶段。

## 12. Phase 2.19 增量更新 / 版本治理路线待办

1. Phase 2.19 已完成路线评审：当前应优先做增量更新 / 文档版本治理，而不是直接进入 facts、完整 RBAC/ABAC 或原始音频 ASR。
2. Phase 2.19a 最小实现已完成：同名同类型文件上传复用同一 document，新增 version，旧 version 标记 superseded，新 version 标记 latest/active。
3. Retrieval 默认保持 `is_latest=true`；显式 `version_id` filter 可查询历史版本，并在 trace 输出 `stale_version` 与 `latest_version_id`。
4. Audit log 已记录 evidence `version_ids`；OpenSearch / Qdrant 已补 `version_id` filter 支持。
5. 已修复 live smoke 暴露的 OpenSearch 旧版本泄露风险：supersede 旧版本时按 `document_id + old_version_id` 限定更新 OpenSearch 旧 chunks 的 `is_latest=false`、`status=superseded`、`superseded_by_version_id`。
6. Phase 2.19a live smoke 已复验：默认 sparse / dense-only / hybrid 只返回 latest v2，显式旧 `version_id` 只返回 v1，audit 默认 latest 只记录 v2。
7. 当前非目标：不做复杂 diff、不做完整文档生命周期后台、不做全库重建、不物理删除旧 chunk、不做 facts 主线。
8. 尾项：Hermes 主仓库 alias store 若要绑定 version_id，需要后续联调 stale_version 诊断；审计 eval 纳入 Phase 2.14 可作为配套小任务。
9. Phase 2.19b 已进入 Hermes 主仓库边界规划：alias stale version 联调优先于审计 eval 扩展；Hermes_memory 继续保持现有 retrieval trace，不改 contract。
10. Phase 2.19b 主仓库最小实现已完成并完成 live smoke；Hermes_memory 继续只提供 `version_scope` / `latest_version_id` trace，不新增 contract。

## 13. Phase 2.20 治理类 Eval 扩展

1. Phase 2.20 已完成边界规划：将 access policy、audit log、version latest/default filtering、explicit historical version query、deny evidence 防泄露与 audit `evidence_version_ids` 纳入 API deterministic eval。
2. Alias stale version 属于 Hermes session layer，不纳入 Hermes_memory stateless API eval；后续应通过 Hermes CLI smoke 覆盖 `alias_stale_version`、`latest_version_id` 与 compare 一侧 stale 的用户侧诊断。
3. Phase 2.20a 最小实现建议：扩展 `scripts/phase214_regression_eval.py` 增加 governance case group，并在 Hermes 主仓库补少量 alias stale CLI smoke。
4. Phase 2.20 非目标：不做完整 RBAC/ABAC、不做复杂 diff、不做 facts、不进入 rollout、不改 retrieval contract、不改 memory kernel 主架构。
5. Phase 2.20a 最小实现已完成：Hermes_memory API eval 新增 `governance` group，5 条治理 case live 运行 `5 passed / 0 failed / 0 skipped`；主仓库 CLI smoke 新增 stale alias case，live runner `5 passed / 0 failed / 0 skipped`。
6. Phase 2.20a full eval 已复跑通过：`16 passed / 0 failed / 1 skipped`，`p50/p95=11.146ms/539.376ms`。
7. 环境注意事项：dense / hybrid eval 必须使用 `QDRANT_COLLECTION=hermes_chunks`；若本机 ignored `.env` 指向旧 `hermes_gate_chunks`，会造成 core dense `dense_returned=0` 假失败。
8. 本轮未回填、未放宽 eval 断言、未改治理功能；`missing_alias_suppress_cli_only` 继续由 CLI smoke 覆盖。

## 14. Phase 2.21 facts 路线裁决

1. Phase 2.21 已完成候选路线评审：增量治理、facts、原始音频 ASR、完整 RBAC/ABAC、生产级 rollout 均仍有价值，但下一阶段建议优先进入结构化 facts 最小闭环。
2. 推荐 Phase 2.21a 的原因：当前 retrieval evidence、version_id、access/audit 与 eval 已具备 facts 的可信来源基础，适合从文档检索助手推进到企业长期记忆系统。
3. Phase 2.21a 最小 facts 必须包含 `fact_type`、`subject`、`predicate`、`value`、`source_document_id`、`source_version_id`、`source_chunk_id`、`confidence`、`verification_status`、`created_by`、`confirmed_by`、`audit_event_id`。
4. facts 必须来源于 retrieval evidence + version_id + audit；未经人工确认或显式确认的 facts 必须标记 `unverified`，不得当作已确认企业事实使用。
5. Phase 2.21a 非目标：不自动把所有文档转 facts、不做复杂知识图谱、不做自动决策、不进入 rollout、不改 retrieval contract、不改 memory kernel 主架构。
6. Phase 2.21a 最小实现已完成：新增 evidence-backed facts service/API，创建 fact 必须绑定 source chunk，并保留 source document/version/chunk、confidence、verification_status、created_by、confirmed_by、audit_event_id。
7. Phase 2.21a live smoke 已通过：会议纪要 action item 与主标书建设单位各创建 1 条 `unverified` fact，by document / by subject 查询均能返回来源字段。
8. 后续尾项：facts 暂不参与 answer generation；如要进入真实业务，应先补 facts eval、权限过滤查询、人工确认工作流和 stale source 处理策略。

## 15. Phase 2.21b facts governance 待办

1. Phase 2.21b 已完成边界规划：优先推进 facts eval、facts 查询权限过滤与人工确认工作流的最小闭环。
2. facts eval 应纳入 Phase 2.14 deterministic eval，覆盖 source document/version/chunk、默认 unverified、confirm/reject 状态流转与 stale source version 诊断。
3. facts 查询权限过滤应继承 source document ACL / tenant soft policy；deny 后不得返回 fact，也不得泄露 source evidence。
4. facts query audit 应记录 requester、tenant、returned_fact_ids、denied_fact_ids、source_document_ids 与 policy_decision。
5. 人工确认工作流先限定为 `unverified -> confirmed/rejected`，不做 UI 管理后台。
6. 当前明确不做 facts 参与回答生成，不做自动全量 facts 抽取，不做知识图谱或 rollout。
7. Phase 2.21b 第一阶段已完成 facts eval：Phase 2.14 runner 新增 `facts` group，5 条 facts case 覆盖来源字段、默认 unverified、confirmed/rejected 与 stale source version。
8. 当前 live eval 结果：facts group `5 passed / 0 failed / 0 skipped`，full Phase 2.14 eval `21 passed / 0 failed / 1 skipped`。
9. 后续仍需实现 facts 查询权限过滤、fact query audit 与人工确认工作流字段增强。
10. Phase 2.21b 第二阶段已完成 facts 查询权限过滤与 fact query audit：facts 查询继承 source document 的 tenant / requester / role soft policy，deny 后不返回 fact。
11. facts query audit 已记录 requester、tenant、role、filter、returned_fact_ids、denied_fact_ids、source_document_ids 与 policy_decision；audit 写入失败 fail-open。
12. 当前仍未完成：facts 权限 eval 纳入 deterministic eval、facts 是否参与回答生成的独立设计。
13. Phase 2.21b 第三阶段已完成人工确认工作流字段增强：新增 confirmed_at、rejected_by、rejected_at、rejection_reason，confirm/reject 均写入 audit。
14. `confirm_fact` 不允许缺失确认人；`reject_fact` 不允许缺失拒绝人，缺失 rejection_reason 时默认写入 `not_specified`。
15. Phase 2.21b 三项最小目标已完成，建议在 Git baseline 后收口；facts 参与回答生成、自动抽取、复杂知识图谱仍后置。

## 16. Phase 2.22 facts 使用路线裁决

1. Phase 2.22 已完成路线评审：不建议立即让 confirmed facts 参与回答生成，也不建议自动 facts 抽取。
2. 推荐下一阶段进入 `Phase 2.22a facts 管理 / 确认工作流增强`。
3. 最小边界：按 verification_status / pending / document / project / subject 查询 facts，并返回 confirm / reject audit history。
4. facts 查询仍需继承 source document soft policy，不得绕过权限过滤。
5. 非目标：不做 Agent 回答引用 facts、不做自动抽取、不做知识图谱、不做 UI 管理后台、不进入 rollout。
6. Phase 2.22a 最小实现已完成：新增 facts 管理列表、pending 列表、confirm/reject review history 查询。
7. 管理列表支持按 verification_status、source_document_id、source_version_id、subject、fact_type、created_by、confirmed_by 过滤。
8. 管理查询继续继承 source document soft policy，deny 后不返回 fact；`fact.query` audit 写入失败仍 fail-open。
9. 当前仍未做：facts 参与回答生成、自动 facts 抽取、复杂知识图谱、UI 管理后台与 rollout。

## 17. Phase 2.23 confirmed facts 使用路线裁决

1. Phase 2.23 已完成路线评审：不建议直接让 confirmed facts 参与 Agent 回答生成，也不建议自动 facts 抽取。
2. 推荐下一阶段进入 `Phase 2.23a confirmed facts 只读检索 / 引用展示`。
3. 最小边界：list / search confirmed facts，并回链 source_document_id、source_version_id、source_chunk_id。
4. confirmed facts 查询必须继承 source document soft policy，并记录 fact.read / fact.query audit。
5. `stale_source_version` 必须可见；confirmed fact 不替代 retrieval evidence，不进入 Agent final answer。
6. 非目标：不做自动抽取、不做复杂知识图谱、不做 UI 管理后台、不进入 rollout。
7. Phase 2.23a 最小实现已完成：新增 `GET /api/v1/facts/confirmed` 与 service 层 `search_confirmed_facts`。
8. confirmed facts 查询支持 subject、predicate、fact_type、source_document_id、source_version_id 过滤，并返回 source_excerpt / source_location。
9. confirmed facts 查询写入 `fact.search` audit；source document soft policy deny 后仍不返回 fact。
10. 当前仍未做：facts 进入 Agent final answer、自动抽取、知识图谱、UI 管理后台与 rollout。

## 18. Phase 2.24 facts 进入 Agent 上下文路线裁决

1. Phase 2.24 已完成路线评审：建议 confirmed facts 先作为 Agent 辅助上下文，而不是直接进入 final answer。
2. 推荐下一阶段进入 `Phase 2.24a confirmed facts 辅助上下文`。
3. 最小边界：仅 confirmed facts 可进入 context，trace 必须包含 `facts_context_used=true` 与 `facts_as_answer=false`。
4. 每条 fact 必须显示 source_document_id、source_version_id、source_chunk_id；stale_source_version 必须明确提示。
5. facts 查询继续继承 source document soft policy，audit 记录 `facts_context_fact_ids`。
6. 非目标：不自动抽取 facts、不让 facts 替代 retrieval evidence、不做知识图谱、不做 UI、不进入 rollout。
7. Phase 2.24a 最小实现已完成在 Hermes 主仓库消费层；Hermes_memory 继续提供 confirmed facts 查询、权限过滤、source citation 与 stale source 诊断。
8. live smoke 已验证 confirmed facts 辅助上下文、stale source warning、无 retrieval evidence 时 suppress；`facts_as_answer=false` 保持不变。
9. 终端验收修复已完成：facts context 独立分区，meeting transcript 不再被标记为 facts，`stale fact source` query 可输出 `stale_fact_source_count` 与 `latest_version_id`。
10. 二次修复已完成：无作用域 stale / fact-answer policy query 抑制普通 retrieval，避免无关文档污染 facts 诊断。
11. alias 绑定 / retrieval-only 场景已稳定输出 facts false / [] / false 诊断，避免模型把 retrieval chunks 写成 fact ids。
12. Codex C 真实终端复验已通过：`@会议纪要` 绑定稳定，5 条正式验收全过，stale fact 检出，`facts_as_answer` 全场景为 false。
13. 复验未出现 E/C chunks 写入 `facts_context_fact_ids`、fact-only query 检索无关文档或 facts 替代 retrieval evidence。
14. 复验注意：`@会议纪要` 必须在同一会话内先绑定，避免新会话 alias_missing。
15. 当前仍未做：facts 进入 Agent final answer、自动抽取、知识图谱、UI 管理后台与 rollout。

## 19. Phase 2.25 项目状态审计与下一阶段路线裁决

1. Phase 2.25 已完成路线评审：当前 Hermes_memory 处于企业长期记忆底座 MVP 后段，核心检索、上下文、治理、facts 与评测均已有最小闭环。
2. 当前不建议直接进入生产 rollout、facts 自动抽取、facts 更深层 Agent reasoning、管理后台或 OCR / 原始音频 ASR。
3. 推荐下一阶段进入 `Phase 2.25a Enterprise Readiness Audit + 数据维护诊断小工具`。
4. Phase 2.25a 最小边界：环境配置、migration、索引健康、API 健康、eval 入口、备份恢复清单的 readiness audit / smoke。
5. 数据维护诊断建议只做 dry-run：重复 / 近似同名 document、latest/superseded 状态、OpenSearch/Qdrant count、一致性和 stale facts 检查。
6. 非目标：不自动修复、不默认全库重写、不做物理删除、不自动确认 facts、不改 retrieval contract 或 memory kernel 主架构。

## 20. Phase 2.25a readiness audit / 数据维护诊断

1. 已新增 `scripts/phase225_readiness_audit.py`，默认 dry-run，只输出诊断 JSON，不修改任何业务数据。
2. 已覆盖服务健康、版本治理、OpenSearch 一致性、Qdrant dense 一致性、facts 治理、audit logs 与 eval readiness。
3. `destructive_actions` 固定为空；light eval 默认不执行，避免 Phase 2.14 fixture 写入破坏只读语义。
4. 单元测试已覆盖 summary 聚合、warning/fail 判定、Qdrant collection 错误诊断与 stale facts 格式。
5. 本机默认 `.env` 指向容器主机名时会清晰失败；本机直跑需覆写 `DATABASE_URL` / `OPENSEARCH_URL` / `QDRANT_URL` / `QDRANT_COLLECTION`。
6. 使用 127.0.0.1 覆写后 live dry-run 结果为 `status=warn`，`22 passed / 1 warning / 0 failed`；warning 为已知 stale confirmed fact。
7. 后续可考虑 Git baseline，并将该 runner 纳入定期 smoke；当前仍不进入生产 rollout。

## 21. Phase 2.26 stale facts / 数据一致性 repair plan dry-run

1. Phase 2.26 已完成边界规划：下一步优先做 repair plan dry-run，而不是直接修复数据。
2. Phase 2.26a 建议新增只读脚本 `scripts/phase226_repair_plan_dry_run.py`，输出结构化 repair plan。
3. 覆盖项：stale confirmed facts、source missing facts、version index inconsistency、duplicate / near-duplicate documents 初步诊断、audit gap 说明。
4. 所有 plan item 必须 `executable=false`；全局 `dry_run=true` 且 `destructive_actions=[]`。
5. 默认 recommended_action 必须保守：`keep_with_warning`、`revalidate_against_latest`、`mark_needs_review`、`reject_if_source_missing`、`reindex_version_payload`、`rerun_dense_backfill`。
6. 硬边界：不修改 facts、document_versions、OpenSearch、Qdrant，不删除数据，不自动确认 facts，不执行 repair。
7. Phase 2.26b 或后续再考虑 readiness audit 定期 smoke / 报告归档；自动 repair 必须等 dry-run 稳定并经过人工确认。
8. Phase 2.26a 最小实现已完成：新增 repair plan dry-run runner 与 6 条单元测试，输出只读 JSON plan。
9. live dry-run 已检出已知 stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e`，无 critical failure。
10. 当前仍不执行 repair / reindex / backfill；下一步可做 Git baseline 后规划人工审核或定期报告。

## 22. Phase 2.26b readiness audit 报告归档规划

1. Phase 2.26b 已完成路线规划：下一步建议做 readiness audit / repair plan dry-run 报告归档，而不是 repair executor。
2. 最小边界：保存 readiness JSON、repair plan JSON，生成 manifest，并支持只读 trend diff。
3. 报告文件名应包含 timestamp、status、git commit，便于人工追踪。
4. 真实 `reports/**/*.json` 与 `latest.json` 默认不提交 Git；如需目录结构，只提交 README / `.gitkeep` / `.gitignore` 策略。
5. 默认不使用 symlink；最新报告指针优先规划为 ignored 的 `latest.json`。
6. 不创建系统 cron，不接生产 scheduler，不默认跑昂贵 full eval，不触发写 fixture 的 eval。
7. 硬边界：不修改 facts、document_versions、OpenSearch、Qdrant，不执行 repair/backfill/reindex，不进入 rollout。
8. 后续实现前需优先明确 reports 目录 ignore 策略与 fake report 单元测试。
9. Phase 2.26b 最小实现已完成：新增报告归档脚本、trend diff、reports ignore 策略与 6 条单元测试。
10. live smoke 已在临时目录归档 fake readiness / repair plan JSON，并生成 manifest/latest；未生成真实仓库 reports JSON。
11. 下一步建议先做 Git baseline，再规划定期 smoke runbook 或报告人工审阅流程；仍不进入 repair executor。

## 23. Phase 2.27 report review workflow 规划

1. Phase 2.27 已完成路线规划：下一步建议做 report-level 与 repair item-level 人工审阅流。
2. Phase 2.27a 最小边界：review record schema、item decision schema、本地 JSON / Markdown 记录、report path/hash 绑定。
3. report 状态建议包含 `pending_review`、`approved_for_manual_action`、`rejected`、`acknowledged`。
4. item decision 建议包含 `needs_review`、`approved`、`rejected`、`deferred`。
5. `approved` / `approved_for_manual_action` 不等于 executed；所有 review record 与 item decision 均必须 `executable=false`。
6. 真实 `reports/reviews/**/*.json` 与 review markdown 默认不入 Git；只提交模板、README 或 ignore 策略。
7. audit_logs 集成后置到 Phase 2.27b；repair executor 继续后置。
8. 硬边界：不写业务 DB，不修改 facts / versions / indexes，不执行 repair，不进入 rollout。
9. Phase 2.27a 最小实现已完成：新增本地 review record 脚本、item decision skeleton、reviews ignore 策略与 7 条单元测试。
10. live smoke 已在临时目录完成 dry-run-preview 与 tmp review JSON 写入；真实仓库未生成 review record。
11. 下一步建议先做 Git baseline，再评估 Phase 2.27b 是否规划 audit_logs 集成；repair executor 继续后置。

## 24. Phase 2.27b review audit 路线规划

1. Phase 2.27b 已完成路线规划：建议先做 report-level audit summary preview，而不是直接写 `audit_logs`。
2. 推荐最小边界：读取 review record，输出 sanitized audit payload，保持 dry-run，不写业务 DB。
3. 建议 event_type：`report.review.created`，后续可扩展到 acknowledged / approved_for_manual_action / rejected。
4. audit payload 可包含 report_hash、report_type、review_status、reviewer、reviewed_at、summary counts、`executable=false`。
5. 必须排除 notes、reason、approved_action、完整 item_decisions、report 原文和本机绝对路径。
6. item-level audit summary 后置，完整 review record 入 audit 不推荐。
7. 真实写 `audit_logs` 在 Phase 2.27b 时仍后置；该项已由 Phase 2.27d 独立阶段承接为显式 `--write-audit` opt-in 最小实现。
8. repair executor 继续后置，`approved_for_manual_action` 仍不等于 executed。
9. Phase 2.27b 最小实现已完成：新增 sanitized audit payload preview runner，读取本地 review record，只输出 report-level audit summary。
10. preview payload 固定 `dry_run=true`、`executable=false`、`would_write_audit_logs=false`，不写 DB、不写 audit_logs。
11. 已通过单元测试与临时目录 live smoke，确认 notes、reason、approved_action、完整 item_decisions、本机绝对路径和 item-level entity details 不进入 payload。
12. Phase 2.27b preview 不等于已写审计；后续 Phase 2.27d 已实现 report-level sanitized audit 的显式 `--write-audit` opt-in，仍不包含 item-level audit、完整 review record 入库或 repair 执行。
13. 本轮按 `NEXT_CODEX_A_PROMPT.md` 完成实现；未启用 Nightly Sprint，未提交 Git。

## 25. Phase 2.28 Agent Operating Protocol / 文件化交接机制

1. Phase 2.28 已新增 Codex A/B/C 文件化协作协议：`docs/AGENT_OPERATING_PROTOCOL.md`。
2. Codex A 每轮开始必须读取 PRD、ROADMAP、TECHNICAL_DESIGN、TODO、DEV_LOG、ACTIVE_PHASE、PHASE_BACKLOG。
3. Codex A 每轮结束必须更新 ACTIVE_PHASE、HANDOFF_LOG、`reports/agent_runs/latest.json`。
4. Codex B 负责读取交接文件、监督是否偏离 PRD / Roadmap / Phase 文档，并给下一轮 prompt。
5. Codex C 负责真实终端验收和 live smoke，不默认承担主实现。
6. `reports/agent_runs/latest.json` 是本地状态文件，默认 ignored，不入 Git。
7. `AGENT_OPERATING_PROTOCOL.md`、`ACTIVE_PHASE.md`、`HANDOFF_LOG.md`、`PHASE_BACKLOG.md` 可作为协作基线提交。
8. 硬停止条件已文档化：真实数据 mutation、repair/delete/cleanup、rollout、contract rewrite、主架构改动、facts 替代 evidence、生产 cron 等均需停止。
9. 下一步建议先做 Phase 2.28 协作协议 baseline，再进入 Phase 2.27b audit preview 实现。
10. Phase 2.28b 已新增 `docs/NEXT_CODEX_A_PROMPT.md` 作为 Codex A 固定任务入口，后续用户可只要求执行该文件。
11. `NEXT_CODEX_A_PROMPT.md` 当前写入 Phase 2.27b sanitized audit payload preview / dry-run 完整任务；本轮不创建脚本、不写测试、不进入实现。
12. `reports/agent_runs/latest.json` 继续作为 ignored 本地状态文件，不入 Git。
13. Phase 2.28c 已新增 Nightly Sprint Protocol 与 Queue，允许夜间仅执行 bounded Green Lane 任务。
14. Nightly Sprint 初始队列：Phase 2.27b audit preview / dry-run、Phase 2.27b baseline、Phase 2.27c route planning。
15. Yellow Lane 完成后必须停止等待 Codex B；Red Lane 夜间禁止，包括 repair executor、migration、rollout、facts 自动抽取、contract / 主架构修改与生产 cron。
16. `reports/nightly_runs/*.json` 是 ignored 本地状态文件，不入 Git；只提交 README / `.gitignore` 策略。

## 26. Phase 2.27c review audit write 路线规划

1. Phase 2.27c 已通过 Nightly Sprint Green Lane 完成路线规划：评审是否将 report review 事件真实写入 `audit_logs`。
2. 当前建议：可以进入后续最小实现，但仅限 report-level sanitized audit 写入；默认仍保持 preview-only。
3. 后续实现必须显式 opt-in，例如 `--write-audit`；不得在夜间自动执行真实 DB 写入。
4. audit payload 只能包含 review_id、report_hash、report_type、review_status、reviewer、reviewed_at、summary counts 与 `executable=false`。
5. 必须继续排除 notes、reason、approved_action、完整 item_decisions、本机绝对路径和 fact_id / document_id 等 item-level entity details。
6. `approved_for_manual_action` 仍不等于 executed；repair executor、item-level audit summary、完整 review record 入库继续后置。
7. 下一阶段候选：`Phase 2.27d report-level review audit write MVP`，但属于 Yellow Lane，必须等待 Codex B 审核与用户显式授权。

## 27. Phase 2.27d report-level review audit write MVP

1. Phase 2.27d 已完成最小实现：review audit preview 默认不写 DB，仅在显式 `--write-audit` 时写入 report-level sanitized `audit_logs`。
2. 写入事件限定为 `report.review.created`，并继续保留 `executable=false` 与 `approved_for_manual_action` 不等于 executed 的语义。
3. `notes`、`reason`、`approved_action`、完整 `item_decisions`、本机绝对路径、item-level entity details 与 `executed` 字段继续硬排除。
4. audit 写入失败 fail-open 并返回 warning；本阶段不扩大 schema，不写 item-level audit，不写完整 review record。
5. 测试结果：py_compile 通过，`tests/test_phase227b_review_audit_preview.py` 共 `15 passed`。
6. live smoke 使用临时 SQLite DB 写入 `1` 条 sanitized audit event；未写生产 / 真实业务 DB。
7. 下一步建议进入 Phase 2.27d Git baseline；baseline 后再评审是否需要把 report review audit 纳入 readiness / eval。
8. repair executor、repair 执行、rollout、真实数据修改继续后置并禁止自动推进。

## 28. Phase 2.27e review audit eval / readiness 规划

1. Phase 2.27e 已完成路线规划：建议优先把 report review audit 安全断言纳入 deterministic eval / unit test。
2. readiness audit 可增加只读检查：近期是否存在 `report.review.created` event，以及是否只统计 report-level sanitized audit。
3. `--write-audit` 的验证应使用临时 SQLite / fixture DB，不触碰真实企业 DB。
4. archive / review / audit 三者关联诊断可作为第二优先级，只使用 hash / id，不写本机路径或 item-level entity details。
5. item-level audit summary、完整 review record 入库、repair executor 与 rollout 继续后置。
6. 后续最小实现不得修改 facts、document_versions、OpenSearch、Qdrant，不得执行 repair/backfill/reindex/cleanup/delete。
7. Phase 2.27e 最小实现已完成：readiness audit 新增只读 `report.review.created` sanitized summary 检查，缺失事件为 warning，unsafe payload 为 fail；相关单测与只读 smoke 已通过。

## 29. Phase 2.27f archive / review / audit 关联诊断规划

1. Phase 2.27f 已完成路线规划：建议下一步只做 archive / review / audit 三者只读关联诊断。
2. 最小边界：用 `report_hash` / `report_type` 关联 archived report 与 review record，用 `review_id` / `trace_id=report_review:<review_id>` 关联 review record 与 audit event。
3. 输出只读 summary，缺少 archive / review / audit 任一环节时为 warning，不自动 fail。
4. 诊断输出不得包含 report 原文、本机绝对路径、notes、reason、approved_action、完整 item_decisions 或 item-level entity details。
5. 第一轮实现不建议直接纳入 readiness audit 默认扫描；可后续显式参数化接入。
6. item-level / repair-level linkage、repair executor、真实 DB 写入与 rollout 继续后置。
7. Phase 2.27f planning 已进入 baseline，下一步只建议在 Codex B 审核后实现只读 linkage summary。
8. Phase 2.27f 最小实现已完成：新增只读 linkage summary runner 与 9 条单元测试，临时目录 smoke 覆盖 pass / missing audit warn / unsafe audit fail；未写 DB、未写 `audit_logs`、未执行 repair。
9. Phase 2.27f 安全补丁已完成：audit event 顶层 unsafe 字段与绝对路径现在会 fail；目标测试 12 passed，临时 smoke 覆盖 unsafe top-level fail。

## 30. Phase 2.27g linkage readiness route planning

1. Phase 2.27g 已完成路线规划：评审 linkage summary 是否显式参数化接入 readiness audit。
2. 推荐路线为 B + D：后续如需要代码衔接，仅做显式参数读取 linkage summary；同时在 Phase 2.29 MVP readiness freeze 中列为人工验收项。
3. 不推荐默认扫描 `reports/` / `reviews/` / audit records，避免读取本机路径、notes、reason、完整 item_decisions 或 item-level entity details。
4. 不推荐继续追加新的 Phase 2.27x 实现；优先在 Phase 2.27g baseline 后进入 Phase 2.29 readiness freeze planning。
5. repair executor、rollout、真实 DB 写入、item-level linkage 与默认目录扫描继续后置。
6. Phase 2.27g planning baseline 已准备收口：本阶段只提交规划与交接文件，不写代码、不写 DB、不改 readiness runner。

## 31. Phase 2.29 MVP readiness freeze planning

1. Phase 2.29 已完成路线规划：当前进入 MVP readiness freeze，而不是继续补新功能或进入 rollout。
2. 已梳理候选 MVP 能力清单、必须复跑验证项、人工验收项与 Go/No-Go 判定标准。
3. 推荐下一步仅进入 Phase 2.29a：freeze checklist / freeze report dry-run，不进入 repair executor、production rollout 或新一轮能力扩展。
4. facts 继续保持 auxiliary context / read-only 边界，`facts_as_answer=false` 不可放松。
5. linkage summary、review audit、readiness audit 继续作为 freeze 证据链的一部分，但不默认扫描真实 reports / reviews。
6. Phase 2.29 planning baseline 收口后，下一轮入口切换为 Phase 2.29a freeze checklist / freeze report dry-run。

## 32. Phase 2.29a freeze report dry-run

1. Phase 2.29a 已新增只读 freeze report dry-run runner。
2. runner 仅读取显式传入的 JSON 证据，不默认扫描真实 reports / reviews，不默认运行 full eval。
3. 输出固定保留 `dry_run=true`、`destructive_actions=[]`、`rollout_ready=false`、`production_rollout=false`、`repair_executed=false`。
4. 目标测试 `8 passed`，临时目录 smoke 通过。
5. 下一步建议 Codex B review 后执行 Phase 2.29a Git baseline。
6. Phase 2.29a baseline 收口后，下一步进入 Phase 2.29b readiness freeze baseline decision planning。

## 33. Phase 2.29b readiness freeze baseline decision planning

1. Phase 2.29b 已完成路线规划：只生成 readiness freeze decision record，不执行 rollout、repair 或 DB mutation。
2. `pass` 可进入 MVP freeze candidate 评审，但仍不等于 production ready。
3. `warn` 不自动进入 MVP candidate，必须人工确认或补充证据。
4. `fail` 必须 No-Go。
5. No-Go 条件包括 production rollout、repair executor、facts 替代 retrieval evidence、默认扫描真实 reports/reviews、真实 DB mutation。
6. 下一步建议进入 Phase 2.29b 最小实现：读取显式 freeze report JSON，输出 decision record / no-go reasons。
7. Phase 2.29b planning baseline 后，下一轮入口切换为 decision record dry-run 最小实现。

## 34. Phase 2.29b decision record dry-run

1. Phase 2.29b 最小实现已完成：新增 `scripts/phase229b_freeze_decision_dry_run.py` 与目标测试。
2. runner 只读取显式 freeze report JSON，不默认扫描真实 reports / reviews，不写 DB。
3. `pass` 映射为 `approved_for_mvp_freeze_candidate`；`warn` 映射为 `needs_manual_review`；`fail` 映射为 `no_go`。
4. `production_rollout=true`、`repair_executed=true` 或非空 `destructive_actions` 会强制 No-Go。
5. 输出恒定保留 `dry_run=true`、`production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`。
6. 验证结果：py_compile 通过，目标 pytest `8 passed`，临时目录 pass / warn / fail dry-run smoke 通过。
7. 下一步建议 Codex B review 后进入 Phase 2.29b Git baseline；production rollout 与 repair executor 继续后置。
8. Phase 2.29b Git baseline 已准备收口：提交范围限定为 decision dry-run runner、测试与阶段文档；不提交 ignored `latest.json` 或真实 reports / reviews 产物。

## 35. Phase 2.29d release candidate checklist planning

1. Phase 2.29d 已完成路线规划：只规划 MVP freeze candidate 人工复核与 release candidate checklist，不进入 production rollout。
2. MVP freeze candidate 被限定为“可人工审阅的候选状态”，不等于 production ready、repair approved 或 facts 可替代 retrieval evidence。
3. release candidate checklist 草案已覆盖 evidence completeness、safety invariants、data governance、sign-off fields 与 Go / No-Go 条件。
4. Codex B 审核重点：freeze report / decision record 状态、warnings、`production_rollout=false`、`repair_approved=false`、`destructive_actions=[]`、`facts_as_answer=false` 与 sanitized linkage。
5. Codex C 仅在后续需要声明“真实 Hermes 终端 MVP candidate 已通过”时做抽样复验；Phase 2.29d planning 本身不需要 live terminal 验收。
6. 当前 known risks 必须继续保留：stale confirmed fact `9f98384b-5053-4a8f-9b83-35983b28b38e`、soft policy 非完整 RBAC/ABAC、专用 `ALIYUN_RERANK_API_KEY` smoke 可选尾项、facts 不得作为 final answer。
7. 下一步建议先做 Phase 2.29d planning Git baseline；baseline 后再由 Codex B 决定是否进入 Phase 2.29e checklist dry-run 最小实现。

## 36. Phase 2.30a practical MVP pilot pack

1. Phase 2.30a 已整理内部受控 MVP Pilot Pack，目标是支持标书审查、企业文件内容提取、公司未来发展方向辅助分析三类真实使用。
2. MVP 被限定为人工监督的内部试运行版本，不等于 production rollout、自动审标、自动经营决策或 repair executor。
3. 新增 playbook 要求所有结论必须带 retrieval evidence / citation；无 evidence 时必须明确缺失，不得凭 facts 或历史记忆作答。
4. 标书审查模板覆盖项目基础信息、投标资格、商务 / 合同风险、缺失信息识别，并要求输出风险等级与待人工确认项。
5. 文件提取模板覆盖标书 / Word / PDF、Excel sheet/cell、PPTX slide、会议纪要 action / decision / risk、A/B compare 防污染。
6. 发展方向分析模板强制 Evidence / Interpretation / Recommendation / Risk / Missing Evidence 分离，并标明“辅助建议，需人工决策”。
7. Pilot 验收清单包含 12 条真实终端 query，建议 Codex C 做抽样验收；本轮未写代码、脚本或测试。
8. Phase 2.30b 已完成 alias/session 最小修复：标题类 alias bind resolver 未命中时允许同轮 retrieval fallback，再由唯一检索文档完成绑定。
9. Phase 2.30b 已通过 Codex C 真实终端复验：12 条 Pilot query 为 `10/12 pass, 2/12 partial, 0 failed`，alias/session 修复有效。
10. Phase 2.30b follow-up 已补齐 runbook 原文 alias 绑定：`把会议纪要文件设为 @会议纪要`、`把硬件清单设为 @硬件清单`、`把C塔方案设为 @C塔方案`、`把当前主标书设为 @主标书`、`把当前标书设为 @主标书`。
11. 下一步建议先做 Phase 2.30a / 2.30b Git baseline，再进入 Phase 2.31 内部受控 MVP Pilot 试用操作规划。
12. 已知试用风险：深层字段召回仍需人工复核，经营建议必须人工决策，当前不进入 production rollout。

## 37. Phase 2.31 internal controlled MVP Pilot operations

1. Phase 2.31 已完成 docs-only planning，新增内部受控 MVP Pilot 操作规划、使用者指南、反馈模板与 known risk checklist。
2. Pilot 范围限定为标书审查 / 风险提取、企业文件内容提取与 citation 定位、公司未来发展方向辅助分析。
3. Pilot 明确不覆盖 production rollout、自动审标定论、自动经营决策、repair executor、facts 自动抽取或 facts 替代 retrieval evidence。
4. 每次试用必须检查 `/health`、建立 Hermes CLI session、绑定 `@主标书` / `@会议纪要` / `@硬件清单` / `@C塔方案`，并保存输出。
5. 人工复核必须检查 document_id / version_id、citation、`facts_as_answer=false`、`transcript_as_fact=false`、contamination_flags 与 Missing Evidence。
6. 最高投标限价、业绩要求、付款节点、工期节点、质保 / 违约等深层字段仍需人工复核。
7. 经营建议只能作为辅助建议，必须人工决策；无 evidence 的内容必须进入 Missing Evidence 或 Assumption。
8. 下一步建议 Codex B review Phase 2.31 文档；通过后再做文档 baseline，不自动进入 production rollout。
9. Codex B review 已确认 Phase 2.31 文档方向可进入 docs baseline。
10. 已补充 `docs/NIGHTLY_CODEX_A_PROMPT.md`，明确 Nightly Sprint 需要 Codex A 会话被启动，Markdown 本身不会自动运行。
11. `NIGHTLY_SPRINT_QUEUE.md` 已从“等待 B review 无可执行项”调整为：Item 1 docs-only baseline，Item 2 Phase 2.32 feedback intake planning。

## 38. Phase 2.32 MVP Pilot feedback intake

1. Phase 2.32 已完成 docs-only planning，新增 MVP Pilot feedback intake / triage loop。
2. 反馈来源限定为 feedback template、真实 Hermes 输出、人工复核结论、Codex C 复验记录与业务影响说明。
3. triage 字段覆盖场景、query、期望 / 实际、pass / partial / fail、document_id / version_id、citation、问题类型、业务影响、优先级、是否需要 Codex C、是否需要新 phase。
4. 已定义问题类型：alias/session、retrieval recall、citation、contamination、facts boundary、transcript boundary、UX / prompt、latency / runtime、environment、other。
5. 已定义 P0/P1/P2/P3：P0 包括 facts 替代 evidence、transcript 误作 fact、compare 第三文件污染、无 citation 确定结论、alias/session 大面积失效。
6. 已定义 Go / No-Go：P0 为 0 且 P1 可人工规避时可继续试用；任一 P0 或连续未解释 fail 应暂停或降级。
7. 当前不自动修复、不自动写 DB、不自动创建 Linear / GitHub issue、不进入 rollout。
8. 下一步建议 Codex B review Phase 2.32 文档；通过后再做 docs-only baseline。
9. Phase 2.32 docs-only baseline 已完成：commit `160ce62`，tag `phase-2.32-feedback-intake-plan-baseline`。
10. 下一步建议 Phase 2.33：整理 Day-1 run sheet 与最小 query set，让内部试用可以直接执行。

## 39. Phase 2.33 MVP Pilot Day-1 execution packet

1. Phase 2.33 已完成 docs-only planning，新增 `docs/MVP_PILOT_DAY1_RUN_SHEET.md`。
2. Day-1 run sheet 覆盖目标 / 非目标、角色、时间表、环境检查、alias 绑定、最小 query set、输出保存规则、人工复核、问题分级与 Go / Pause。
3. 最小 query set 覆盖 `@主标书` 基础信息与风险、缺失风险检查、`@硬件清单` Excel sheet/cell、`@C塔方案` PPTX slide、`@会议纪要` action / decision / risk、A/B 防污染、facts 边界与公司方向辅助分析。
4. 每条输出必须保存 query、原始输出、document_id/version_id、citation、`facts_as_answer`、`transcript_as_fact`、contamination_flags、pass/partial/fail、issue_type 与 priority。
5. Go 条件：P0 为 0、alias/session 不成为主要阻塞、partial / Missing Evidence 可人工记录、使用者理解输出只是辅助建议。
6. Pause 条件：facts 替代 evidence、无 citation 给确定结论、compare 混入第三文件、alias/session 大面积失效、使用者要求自动决策 / repair / rollout。
7. 当前不写代码、不运行 pytest、不进入 production rollout、不自动创建 issue。
8. 下一步建议 Codex B review Phase 2.33 run sheet；通过后再做 docs-only baseline。
9. Codex B 已审核 Day-1 run sheet，可执行 Phase 2.33 docs-only Git baseline；baseline 后停止等待检查。

## 40. Phase 2.34 Day-1 compare false-positive fix

1. Codex C Day-1 Pilot 结果：10 条 query 为 `7 pass / 3 partial / 0 fail`，P0 为 `0`；四个 alias 均稳定。
2. 当前 P1/P2 分流：Q1/Q2 主标书深层字段召回进入 P1 backlog；Q7/Q10 长输出延迟进入 P2 backlog；本轮只修 Q8 compare false-positive。
3. 已完成最小修复：最终 `retrieval_evidence_document_ids` 均属于 `compare_document_ids` 时，trace/context 稳定输出 `third_document_mixed=false`。
4. 已保留真实污染检测：最终 evidence 出现 compare 外 document_id 时仍输出 `third_document_mixed=true` 与 `unexpected_document_id`。
5. 候选过滤诊断改为 `out_of_scope_document_ids_filtered`，不再在最终 `contamination_flags` 中误导为第三文件混入。
6. Codex C 真实终端复验已通过：Q8 compare 输出 `third_document_mixed=false`、`third_document_mixed_document_ids=[]`、`contaminationflags=none`，无实际第三文件 evidence。
7. Facts / transcript 抽样通过：`facts_context_used=false`、`facts_context_fact_ids=[]`、`facts_as_answer=false`、`transcript_as_fact=false`。
8. Phase 2.34 已完成 baseline，Q8 compare false-positive 收口；后续转入 Phase 2.35 主标书深层字段召回专项。

## 41. Phase 2.35 tender deep-field retrieval

1. 已完成 diagnostic-first 最小实现，限定在 Hermes_memory retrieval 层。
2. 新增 / 增强 metadata snapshot fields：
   - `price_ceiling`
   - `qualification_requirement`
   - `project_manager_requirement`
   - `consortium_requirement`
   - `performance_requirement`
   - `personnel_requirement`
3. 已扩展最高投标限价 / 招标控制价 / 投标报价上限的触发词、section hints 与 phrase boosts。
4. 已扩展资质 / 项目经理 / 联合体 / 业绩 / 人员要求的触发词、section hints 与 phrase boosts。
5. 已新增 additive trace：`deep_field_profile`、`deep_field_section_hints`、`deep_field_query_aliases`、`metadata_deep_field_profile`。
6. `snapshot_as_answer=false` 与 `evidence_required=true` 保持不变，snapshot 只做导航，不替代 retrieval evidence。
7. 测试结果：py_compile 通过，目标 pytest `22 passed`。
8. 未做真实 Hermes CLI 复验；下一步需 Codex B review，必要时交 Codex C 复验 Day-1 Q1/Q2。
9. 当前仍不进入 production rollout，不做自动审标，不写 DB，不改索引。
10. Codex C 复验结果：Q1 基础字段通过，但最高投标限价 / 招标控制价 / 投标报价上限仍 Missing Evidence；Q2 投标资质 fail，项目经理 / 联合体 / 业绩 / 人员要求 partial。
11. 安全边界通过：未编造金额、资质、业绩或人员数量；`snapshot_as_answer=false`、`facts_as_answer=false`、`transcript_as_fact=false`。
12. 当前暂不 baseline，进入 Phase 2.35b bounded follow-up。
13. Phase 2.35b 代码层 review 通过，但 Codex C 真实 CLI 复验显示正式 Q1/Q2 被 alias/session 阻断：`alias_missing=true / retrieval_suppressed=true`。
14. Phase 2.35c 下一步只修 Hermes 主仓库 alias/session 首次绑定后丢失；修复后再由 Codex C 重跑 Q1/Q2。
15. Phase 2.35c 已完成主仓库最小修复：`上一轮已锁定的当前文件` 等说法会进入 current-document bind / current retrieval fallback，并持久化 alias 供后续同 session query 使用。
16. Codex C 真实终端复验通过：正式 Q1/Q2 不再丢 alias，不再 suppressed，可进入 Phase 2.35c baseline。
17. deep-field recall 仍 partial：限价具体金额、资质具体等级 / 类别、类似业绩、人员要求仍为后续尾项；`metadata_deep_field_profile=null` 与 `deep_field_profile=single_pass` 属 trace / 展示尾项。

## 42. Phase 2.36 tender deep-field recall tail planning

1. Phase 2.36 已完成路线规划：只做文档规划，不写代码、不运行真实 API / CLI smoke、不提交 Git。
2. 已按字段分类剩余缺口：
   - 最高投标限价 / 招标控制价 / 投标报价上限。
   - 投标资质等级 / 类别。
   - 项目经理等级 / B 证。
   - 联合体。
   - 类似业绩。
   - 人员数量 / 专业 / 证书。
   - trace display / profile fields。
3. 缺口分类使用 A/B/C/D：真实缺字段、章节召回不足、trace 展示问题、需人工确认。
4. 推荐 Phase 2.36a 最小实现：trace polish + section-targeted retrieval diagnostics + fixture-based concrete field tests。
5. 继续保留 Missing Evidence 口径；不得编造限价金额、资质等级、业绩或人员数量。
6. 不进入自动审标、production rollout、repair、DB / OpenSearch / Qdrant 变更。
7. Phase 2.36a 已完成 retrieval-layer 最小实现：顶层 trace 稳定输出 deep-field profile / section hints / query aliases / Missing Evidence reason / diagnostics。
8. 新增 fixture tests 覆盖具体限价、占位限价、具体资质等级+类别、证照清单；目标 pytest `17 passed`。
9. 下一步需 Codex B review；如终端仍显示 `metadata_deep_field_profile=null` 或 `deep_field_profile=single_pass`，需单独授权检查 Hermes 主仓库 adapter/context 展示层。
10. Phase 2.36b 已完成主仓库消费层最小实现：adapter / kernel / context_builder 提升并渲染 deep-field trace；alias parser 支持 `锁定“标题”，并绑定为 @alias`。
11. Phase 2.36b 主仓库目标测试：py_compile 通过，`59 passed`。
12. 下一步需 Codex B review 与 Codex C 真实终端复验；不能把本轮写成 deep-field recall 完全收口。
13. Codex C 复验确认 Phase 2.36b 的 alias binding 与 terminal-visible trace 已基本通过，但发现 diagnostics 与答案边界语义不一致：Q1 限价 diagnostics 可能显示 concrete found，而最终答案仍 Missing Evidence。
14. Phase 2.36c 已完成 Hermes_memory 最小修复：concrete evidence 需经最终 retrieval evidence 校正；metadata anchor 命中但最终 evidence 无具体金额时，trace 保守输出 `missing_concrete_price_amount` 与 `concrete_evidence_present=false`。
15. Phase 2.36c 已约束项目经理等级表述：仅电子证书 / 证照材料 / 格式条款不得推断为“项目经理=一级注册建造师”；需明确“项目经理须具备 X级注册建造师”才算 explicit level evidence。
16. Phase 2.36c 目标测试 `33 passed`；Codex B review 已通过，Codex C 真实终端复验已通过。
17. Phase 2.36c 当前可执行 Git baseline：限价 diagnostics 与 Missing Evidence 语义一致，电子证书 / 材料条款不再推断为项目经理等级；deep-field recall 仍 partial，真实限价金额、具体资质等级 / 类别、业绩、人员数量继续后置，不能宣称完整自动审标收口。

## 43. Phase 2.37 MVP Pilot issue intake / triage planning

1. Phase 2.36c baseline 已完成：commit `d491a44`，tag `phase-2.36c-tender-deep-field-diagnostics-baseline`。
2. 下一阶段建议先做 Pilot issue intake / triage，而不是继续盲修单个 deep-field recall 问题。
3. issue intake 应记录 query、expected / actual、document_id、citation、issue_type、priority、source_phase 与 human_review_required。
4. P0 必须覆盖编造、facts/transcript 替代 evidence、跨文件污染、权限泄露、自动决策越界。
5. Phase 2.37 规划已完成，新增 `docs/PHASE237_PILOT_ISSUE_TRIAGE_PLAN.md`。
6. 推荐 Phase 2.37a 做 local issue intake schema / templates / dry-run validator or summary generator。
7. Phase 2.37a 非目标：不自动修复 issue，不写 DB / facts / document_versions，不修改 OpenSearch / Qdrant，不进入 rollout，不做自动审标结论。
8. Phase 2.37 planning baseline 已完成：commit `8fd10b7`，tag `phase-2.37-pilot-issue-triage-plan-baseline`。
9. Phase 2.37a 最小实现已完成：新增 local intake dry-run 工具与测试，支持 template、single / directory input、schema 校验、summary、strict invalid exit。
10. Phase 2.37a 验证通过：py_compile 通过，`tests/test_phase237a_pilot_issue_intake.py` 为 `9 passed`，临时 dry-run smoke 通过；下一步需 Codex B review 后再 baseline。
11. Phase 2.37a Git baseline 已完成：commit `1e1ca45`，tag `phase-2.37a-pilot-issue-intake-baseline`。
12. Phase 2.37b 最小 runbook / storage convention 已完成：新增 MVP Pilot issue intake runbook，规定 `reports/pilot_issues/*.json` 为本地敏感试用记录且默认 ignored。
13. Phase 2.37b 验证通过：template / strict dry-run 命令通过，`reports/pilot_issues/example.json` ignore 策略通过；下一步需 Codex B review 后再 baseline。
14. Phase 2.37b Git baseline 已完成：commit `e8c0631`，tag `phase-2.37b-pilot-issue-intake-runbook-baseline`。
15. Phase 2.37c planning 已完成：新增 daily / per-round Pilot issue triage summary 规划，明确 P0 pause、P1 bounded fix planning 候选、P2 backlog / UX / latency、P3 polish。
16. Phase 2.37c 非目标：不创建真实 issue records，不写 DB / facts / versions / index，不自动创建外部 issue，不 repair，不 rollout，不自动审标。

## 44. Phase 2.40 PRD Acceptance Matrix / MVP Evidence Pack planning

1. Phase 2.40 已完成 docs-only planning，新增 `docs/PHASE240_PRD_ACCEPTANCE_MATRIX_PLAN.md`。
2. acceptance matrix 最小字段为 `prd_item`、`capability_area`、`status`、`evidence_type`、`evidence_ref`、`known_gap`、`next_phase_candidate`、`not_claimable`。
3. 状态口径固定为 `done` / `partial` / `planned` / `deferred`，避免把 partial、dry-run 或 docs-only 能力误写成 done。
4. MVP evidence pack 优先收集 citation、Top-K / rerank / trace、permission deny behavior、`facts_as_answer=false`、`transcript_as_fact=false`、Pilot query pass rate 与 Missing Evidence / 人工复核边界。
5. 当前不可宣称能力包括 production rollout ready、自动审标 / 自动经营决策、repair executor ready、facts 自动抽取或替代 evidence、Data Steward 已实现、TB BIM 全量解析、完整知识图谱 / 多 agent / 完整 RBAC。
6. Phase 2.40a 候选方向：只读 matrix / evidence pack artifact 或 generator；不得写 DB、跑真实 API、进入 rollout、启动 Data Steward 实现或新增 schema / scheduler。

## 45. Phase 2.40a PRD Acceptance Matrix / MVP Evidence Pack artifact

1. Phase 2.40a 已完成 docs-only artifact，新增 `docs/PRD_ACCEPTANCE_MATRIX.md`。
2. Matrix 覆盖 ingestion、structured chunking、sparse/dense/hybrid retrieval、rerank、citation/trace、alias/session、Excel/PPTX、meeting transcript、facts governance、access/audit、version governance、readiness / repair dry-run、review workflow、Pilot issue intake、tender deep-field retrieval、Data Steward deferred product line。
3. 每行包含 PRD item、capability area、status、evidence、known gap、next phase candidate、not claimable。
4. 当前落地判断：可进入内部受控 MVP Pilot / Day-1 试用，但不是 production rollout。
5. 当前必须人工复核：限价、具体资质等级 / 类别、项目经理等级、类似业绩、人员数量、经营判断和所有 Missing Evidence。
6. 当前不可宣称：production ready、自动审标、自动经营决策、repair executor ready、facts 自动抽取或替代 evidence、Data Steward 已实现、TB BIM 全量解析、Neo4j / PostGIS / 空间索引 / scheduler 已落地。
7. Phase 2.40a docs baseline 已完成：commit `e6f7fc2`，tag `phase-2.40a-prd-acceptance-matrix-artifact-baseline`。

## 46. Phase 2.41 MVP Pilot Evidence Review / Go-No-Go planning

1. Phase 2.41 已完成 docs-only planning，新增 `docs/PHASE241_MVP_PILOT_EVIDENCE_REVIEW_PLAN.md`。
2. 规划目标：把 PRD acceptance matrix 转成内部受控 MVP Pilot 的人工 evidence review、Go / Pause / No-Go 与 P0 / P1 / P2 / P3 handling policy。
3. Go 条件要求 P0 为 0、alias/session 不阻塞核心流程、citation / document_id / version_id 可人工核验、`facts_as_answer=false` / `transcript_as_fact=false` / `snapshot_as_answer=false` 稳定，且 Missing Evidence 被正确记录。
4. Pause / No-Go 条件覆盖编造金额、资质、业绩、人员数量或经营结论，facts / transcript / snapshot 替代 retrieval evidence，跨文件污染，权限泄露，alias/session 核心阻断，以及无法保存人工复核记录。
5. human review requirement 覆盖限价、资质等级 / 类别、项目经理等级 / B 证、类似业绩、人员数量、经营判断和所有 Missing Evidence。
6. 当前仍不进入 production rollout、自动审标、自动经营决策、repair executor、Data Steward 实现、DB schema / Neo4j / PostGIS / 空间索引 / scheduler。
7. 后续候选：Phase 2.41a 只读 Pilot evidence review checklist artifact，或 Phase 2.41a Pilot evidence review dry-run report。
8. 下一步建议 Codex B review；通过后只做 docs-only baseline，不直接进入新能力开发。

# TODO 最新状态

- 当前 phase：Phase 2.85 Controlled Evidence Write Dry-run Planning。
- 当前目标已完成：新增 controlled evidence write dry-run planning 文档，明确 future local temp SQLite / in-memory simulated write 模型。
- 当前仍未实现：Phase 2.85a dry-run runner、真实 evidence write、Agent answer integration。
- 当前禁止：`documents/chunks`、platform DB / Hermes DB、OpenSearch、Qdrant、MinIO 写入，parser，真实文件复制，raw content 读取，NAS scan，repair/backfill/reindex/delete/migration，production rollout。
- 下一步：Codex B review Phase 2.85 planning；通过后只做 docs-only Git baseline。

## 47. Phase 2.41a MVP Pilot Evidence Review Checklist Artifact

1. Phase 2.41a 已新增只读人工审阅 artifact：`docs/MVP_PILOT_EVIDENCE_REVIEW_CHECKLIST.md`。
2. Checklist 覆盖 reviewer、reviewed_at、pilot_round、source_sessions、evidence_refs、decision、decision_reason 等人工填写字段。
3. Checklist 明确 P0 / P1、evidence policy、citation、governance、human review、not-claimable 与 Go / Pause / No-Go 结论模板。
4. `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`、Missing Evidence not hidden 继续作为 Pilot evidence review 必查项。
5. 当前 artifact 只用于内部受控 MVP Pilot 人工审阅，不是 production rollout approval，不是自动审标批准，不是 repair / cleanup / reindex 授权。
6. Data Steward 仍是后置产品线；当前未实现 Data Steward、TB BIM 全量解析、Neo4j / PostGIS / 空间索引或 scheduler。
7. 本轮不写代码、不新增脚本 / 测试 / migration、不运行 pytest / API / CLI、不提交 Git。
8. 下一步建议 Codex B review Phase 2.41a artifact；若通过，再按 Baseline Gate 单独执行 docs-only baseline。

## 48. Phase 2.42 MVP Pilot Review Dry-run Report Planning

1. Phase 2.42 已新增 docs-only planning：`docs/PHASE242_MVP_PILOT_REVIEW_DRY_RUN_PLAN.md`。
2. 规划目标：把 checklist、PRD acceptance matrix、Pilot issue records、Codex C sessions、readiness / repair dry-run reports 与人工复核记录汇总成后续只读 dry-run report。
3. 规划输出字段包括 report_id、generated_at、reviewer / reviewed_by、pilot_round、source_sessions、P0/P1/P2/P3 count、decision、decision_reason、evidence_policy_summary、citation_summary、missing_evidence_summary、known_risks、not_claimable_confirmed 与 next_phase_candidates。
4. Go / Pause / No-Go dry-run logic 明确：P0 任一命中即 no_go；P1 需人工复核或 bounded backlog；Go 只代表可继续内部受控 MVP Pilot，不代表 production rollout。
5. evidence policy 必查 `facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`、Missing Evidence not hidden、no production ready claim。
6. storage policy：后续真实 report 默认写入 ignored 的 `reports/mvp_pilot_reviews/`，本轮不创建真实 report。
7. 当前不写代码、不新增脚本 / 测试 / migration、不运行 pytest / API / CLI、不提交 Git。
8. Codex B review 已确认 Phase 2.42 planning 主线方向正确，baseline 前仅需同步 TODO 当前状态与 Nightly queue，避免旧 Phase 2.39 / Phase 2.37 口径误导。
9. 当前 docs sync review-fix 小修不 baseline；完成后等待 Codex B 再判断是否写入 Phase 2.42 docs-only baseline prompt。

## 49. Phase 2.42a MVP Pilot Review Dry-run Report Generator

1. Phase 2.42 baseline 已完成：commit `0e0d208`，tag `phase-2.42-mvp-pilot-review-dry-run-plan-baseline`。
2. Phase 2.42a 已新增本地只读 dry-run report generator：`scripts/phase242a_mvp_pilot_review_dry_run.py`。
3. generator 仅读取显式 `--input` JSON，不默认扫描真实 `reports/` 或 `reviews/`。
4. 输出固定保留 `dry_run=true`、`production_rollout=false`、`repair_authorized=false`、`destructive_actions=[]`、`data_mutation=false`、`facts_as_answer=false`、`transcript_as_fact=false`、`snapshot_as_answer=false`。
5. decision rules 覆盖 P0 / unsafe evidence policy / rollout / repair / destructive actions => `no_go`；Missing Evidence 未人工复核或 blocking P1 => `pause`；P1 已记录且可人工复核 => 内部受控 Pilot 的 `go`。
6. 已新增 `reports/mvp_pilot_reviews/.gitignore` 与 `README.md`；真实 report JSON / Markdown 默认 ignored，不入 Git。
7. 当前不运行 API / CLI smoke，不写 DB / facts / versions / OpenSearch / Qdrant，不进入 production rollout、repair 或 Data Steward 实现。
8. 下一步需 Codex B review Phase 2.42a；通过后再单独决定是否 Git baseline。

# Phase 2.56e Baseline Gate

1. Codex B review passed for Natural Import Real Upload Client + Real Smoke.
2. Next step is selective dual-repo Git baseline only.
3. Do not rerun real upload or cleanup the created test records.
4. After baseline, plan Phase 2.57 around natural import MVP evidence / operator usability, not DB/NAS/Data Steward implementation.

# Phase 2.57 Natural Import MVP Usability Planning

1. Phase 2.56e baseline complete; natural import real upload works for one authorized `.docx`.
2. Next is docs-only planning for evidence pack / Mac mini operator runbook.
3. No file upload, no code, no DB/index mutation, no Data Steward implementation in this phase.

# Phase 2.57a Natural Import Evidence Template / Runbook Dry-run

1. Phase 2.57 baseline 已完成；下一步做只读 evidence template / runbook dry-run runner。
2. 目标是减少 operator 手工复制字段，先生成可测试 JSON 模板，不执行真实上传。
3. 禁止 API/CLI smoke、真实 upload、DB/index 写入、repair/backfill/reindex、Data Steward / DB / NAS 实现。
4. Phase 2.57a 最小实现已完成：新增 dry-run runner 与 targeted tests。
5. 验证通过：py_compile 通过，`tests/test_phase257a_natural_import_evidence_template.py` 为 `7 passed`。
6. 当前等待 Codex B review；不自动 baseline，不进入 Phase 2.57b。

# Phase 2.57 Baseline Gate

1. Codex B review passed for Natural Import MVP Usability / Evidence Planning.
2. Next step is docs-only selective Git baseline.
3. No upload, no API/CLI smoke, no code, no DB/index writes.
4. After baseline, consider Phase 2.57a evidence template / runbook runner dry-run.

# Phase 2.58 Natural Import Operator Pack

1. Phase 2.57a runner 已完成但暂不单独 baseline，继续打包 review helper 与 Mac mini operator checklist。
2. 本轮目标是减少 operator 手工复制字段：生成 evidence template、复核 dry-run JSON、给出 Go/Pause/No-Go 前置判断。
3. Codex B review-fix：review helper 必须阻断 `plain_upload_bypass_used=true` 与 `real_file_uploaded=true`，避免 direct API upload 或已上传记录被误当作 dry-run 授权模板。
4. 禁止 API/CLI smoke、真实 upload、DB/index 写入、repair/backfill/reindex、Data Steward / DB / NAS 实现。
5. Phase 2.58 最小实现已完成：新增 `--review-json` dry-run review helper 与 Mac mini operator checklist。
6. Review-fix 已完成：`plain_upload_bypass_used=true` 与 `real_file_uploaded=true` 会被判为 `pause`，避免 direct API bypass / 已发生 upload 记录被当作 dry-run 授权模板。
7. 验证通过：py_compile 通过，targeted pytest `14 passed`。
8. 当前等待 Codex B review；不自动 baseline，不进入真实 upload smoke。

# Phase 2.58 Baseline Gate

1. Codex B review passed for Natural Import Operator Pack.
2. Next step is selective Git baseline only.
3. Do not upload files, run API/CLI smoke, or stage historical dirty / DB-NAS drafts.
4. After baseline, plan Phase 2.59; do not auto-upload.

# Phase 2.59 Natural Import Second Smoke Planning

1. Phase 2.58 baseline 已完成；下一步规划第二个用户授权小文件 natural import smoke。
2. 本轮只写授权门槛、Codex C 待授权模板和验收字段，不上传文件。
3. 真实 smoke 必须由用户提供文件路径并明确授权。
4. Phase 2.59 docs-only planning 已完成：新增第二真实文件授权 gate、Codex C 待授权模板、operator checklist 流程与 Phase 2.57 计划同步。
5. 下一步建议 Codex B review；通过后再做 docs-only baseline。
6. 第二真实文件 smoke 仍不得自动执行；必须等待用户提供小型非敏感文件路径并明确授权。

# Phase 2.60 Internal MVP Launch Readiness Pack

1. Phase 2.59 baseline 已完成：commit `2603a87`，tag `phase-2.59-natural-import-second-smoke-plan-baseline`。
2. Phase 2.60 已完成最小实现：新增只读 local readiness runner、目标测试与 Mac mini operator checklist 同步。
3. Runner 输出 `go` / `pause` / `no_go`，固定 `dry_run=true`、`read_only=true`、`destructive_actions=[]`、`real_upload_called=false`、`api_smoke_called=false`、`cli_smoke_called=false`、`db_or_index_written=false`、`production_rollout=false`。
4. 本轮未上传文件、未执行 API / CLI smoke、未写 DB / facts / versions / audit_logs / OpenSearch / Qdrant。
5. 下一步建议 Codex B review；通过后再 selective baseline。
6. 第二真实文件 smoke 仍保留为用户授权后 Codex C 任务，不阻塞 Phase 2.60 review。

# Phase 2.113 Hermes Memory Self-Awareness / Kernel Activation

1. Phase 2.113 runtime fix 已完成本地最小实现：Hermes 主仓库现在会向模型注入 Hermes Memory Kernel capability boundary。
2. 自然导入成功响应已补齐 import status、safe document/version id、chunk/index 状态、推荐 alias、后续提问建议与 evidence / Missing Evidence 边界。
3. 模糊找文件无安全候选时会 suppress retrieval，并要求澄清，不再落到无关普通检索。
4. 验证：py_compile 通过；Hermes 主仓库 natural import runtime `14 passed`、structured citation context `18 passed`、session document scope `67 passed`。
5. 下一步：Codex B review；通过后由 Codex C / 测试机验证 OpenWebUI / 8642 真实 self-awareness、natural import feedback 与 fuzzy file discovery。
6. 当前不 baseline、不宣布 Phase 2 complete、不进入 rollout。
# TODO 最新状态

- 当前 phase：Phase 2.112f Alias Continuity Restore Fix 已通过 Codex B review，待测试机复验。
- 完成：Hermes 主仓库 follow-up alias continuity restore diagnostics 已稳定进入 nested `alias_resolution`；same-owner restore 跨 store reload / 新 agent instance 已有测试覆盖。
- 验证：Codex B 复跑 py_compile 通过；full natural import / upload client / session scope regression `109 passed`；gateway stable-owner targeted tests `3 passed`。
- runtime candidate：Hermes agent `78eb77158` / `phase-2.112f-alias-continuity-restore-runtime-test-candidate`。
- 下一步：测试机复验 OpenWebUI / 8642 import -> follow-up `@建筑类数据样表` retrieval + citation。

- 当前 phase：Phase 2.112e API Server Stable Owner Bridge Fix 已实现，待 Codex B review。
- 结果：API server 已把 accepted `X-Hermes-Session-Id` / whitelisted OpenWebUI conversation header 转成 `gateway_session_key` 传入 `AIAgent`；无 stable owner 时继续 fail-closed 并输出 sanitized `stable_owner_missing`。
- 验证：py_compile 通过；API server owner bridge targeted tests `7 passed`；natural import / upload client / session scope regression `106 passed`。
- 下一步：Codex B review；通过后再考虑 selective runtime baseline 与测试机 OpenWebUI / 8642 验证。

- 当前 phase：Phase 2.65 Mac mini MVP Landing Acceleration Pack。
- 当前目标：准备 Mac mini 测试机安装 / 更新 / 回滚所需的 release manifest helper、quickstart、Codex Mac mini prompt。
- 当前 Hermes_memory 推荐安装 ref：`phase-2.64b-data-steward-selective-integration-baseline`。
- 当前仍需确认 hermes-agent reviewed ref；若缺失，Mac mini 安装流程应 Pause，而不是猜。
- 本阶段不执行真实部署、不启动服务、不上传、不连接真实 DB、不扫描 NAS、不写 DB / index、不进入 rollout。

# TODO 最新状态

- 当前 phase：Phase 2.64b Selective Data Steward DB Integration。
- 当前目标：将 DB 支线的 readonly asset catalog interface、contract docs、tests 选择性接入主线。
- 当前禁止：raw merge、真实 DB 连接、NAS 扫描、migration、`documents/chunks`、OpenSearch / Qdrant 写入、DB-5 / DB-6、PR 创建、commit/tag/push、production rollout。
- 合入策略：只接 `app/services/asset_catalog/**`、`tests/test_data_steward_*.py`、DB contract docs 与 feature flags 默认 off 的最小配置；排除 `.claude/**`、DB 支线交接文件、QA probe 与任何会回退主线 MVP 的文件。

# TODO 最新状态

- 当前 phase：Phase 2.64 Data Steward DB Branch Intake / PR Review。
- Phase 2.63 baseline 已完成：`fee1dcb` / `phase-2.63-operator-daily-summary-baseline`。
- 本阶段只做 DB 支线接收、PR / merge readiness review 与文档同步；不连接真实 DB，不扫描 NAS，不写 migration，不写 `documents/chunks`，不写 OpenSearch / Qdrant，不 merge 到 `main`。
- DB 支线当前 closeout baseline：`/Users/Weishengsu/Hermes_memory_db0`，`a272081` / `phase-db-branch-closeout-merge-readiness-baseline`。
- 后续真实 DB smoke 必须在测试机部署 Hermes Memory 后由用户单独授权，且只允许 structure-only 或 LIMIT 30 脱敏 smoke。

# Phase 2.112h Explicit Natural Import Alias Preservation Fix

1. Hermes 主仓库本地最小修复已完成：explicit natural-language alias parser 已覆盖 `别名 @...`、`别名为 @...`、`别名叫 @...`、`别名设为 @...`、`设定别名为 @...`、`我想叫它 @...`。
2. 用户请求 alias 优先于 generated alias；malformed alias 保持 `not_requested` / fail-closed。
3. 验证通过：targeted parser / flow / runtime tests `15 passed`；py_compile 通过；natural import / upload client / session scope regression `124 passed`。
4. Codex B review 已通过；Hermes agent runtime test-candidate 已 baseline 并推送：`e1d38e1ec` / `phase-2.112h-explicit-import-alias-runtime-test-candidate`。
5. 未执行真实 OpenWebUI / 8642 upload/import，未写 DB / facts / versions / OpenSearch / Qdrant；full natural import closeout 未完成。
6. 测试机 2.112h 复验已越过 alias gate：import alias 正确为 `@建筑类数据样表`，follow-up `alias_resolved`，`alias_missing=false`。
7. 当前最小阻塞点变更为测试机环境：Hermes_memory retrieval backend 无法解析 `postgres` 主机名，导致 `retrieval_backend_failed`、evidence 为空、citation 缺失。
8. 下一步：测试机修复 Hermes_memory API / DB hostname 运行环境后，重跑 follow-up retrieval + citation；不要再把该问题打回 alias parser / continuity 代码。

## Phase 2.113a Self-Awareness Review Fix

1. Phase 2.113 Codex B review returned; do not baseline current runtime fix.
2. Blocking issue: broad `帮我找/找一下` fuzzy file-discovery trigger suppresses normal retrieval questions.
3. Codex A must narrow file-discovery intent and add regression tests for ordinary retrieval not being suppressed.
4. Codex A should broaden safe self-awareness trigger wording.
5. Keep previous safety boundaries: no NAS scan, no DB CRUD/SQL, no raw path/content memory, no DWG/RVT/BIM overclaim, no production rollout.
6. Phase 2.113a bounded fix passed Codex B review: py_compile passed, target suite `102 passed`, and direct probes confirmed ordinary retrieval / fuzzy file-discovery / self-awareness boundaries.
7. Hermes agent runtime test-candidate is `a12d378e0` / `phase-2.113a-self-awareness-runtime-test-candidate`.
8. Next action is test-machine / OpenWebUI / 8642 validation using `docs/CODEX_TEST_MACHINE_PHASE2113A_SELF_AWARENESS_SMOKE_PROMPT.md`; no further Codex A implementation unless that validation returns a concrete blocker.
9. Test-machine / OpenWebUI-compatible 8642 validation returned Go for self-awareness, ordinary retrieval guard, fuzzy file-discovery safety, and side-effect boundaries.
10. Natural import feedback was skipped because no import was authorized in this smoke; this is not a blocker for the Phase 2.113a live gate.
11. Next action is Phase 2.113 closeout / Phase 2 final freeze checklist update; no more 2.113a coding unless a new live blocker appears.

## Phase 2.114 Final User-flow Acceptance

1. Phase 2.114 is the final controlled user-flow gate before Phase 2 stable MVP freeze.
2. Required flow: self-awareness -> natural-language import -> alias -> follow-up retrieval -> citation -> evidence boundary.
3. Test-machine prompt: `docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md`.
4. Required operator inputs: one authorized small non-sensitive `AUTHORIZED_FILE_PATH`, a safe `ALIAS`, and a safe `PROJECT_CONTEXT`.
5. No new Codex A runtime work is allowed unless the final user-flow smoke returns a concrete blocker.
# Phase 2.115 Workspace Context / Auto Alias Runtime Candidate

1. Hermes 主仓本地实现已完成：自然导入在没有手填 `PROJECT_CONTEXT` / 显式 alias 时可推断 safe `workspace_context`，并生成 / 绑定安全 alias。
2. C塔人力成本类文件名会生成 `@C塔人力成本测算表` 类 alias；显式 alias 仍优先。
3. session alias registry 已保存 workspace metadata，fuzzy file discovery 可按 alias / workspace / category 返回安全候选。
4. import success 响应显示 workspace / alias diagnostics，但明确 `workspace_context_as_retrieval_evidence=false`，且不展示 raw path。
5. 验证：Hermes 主仓 `git diff --check` 通过，py_compile 通过，natural import / runtime / session scope regression `129 passed`。
6. 下一步：发布 runtime test-candidate 后由 Codex B review 与 Codex C / 测试机复验；不得直接宣布 Phase 2.115 收口。

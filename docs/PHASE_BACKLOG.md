# Phase Backlog

## Phase 2.116 Natural Import User-facing Response Polish

1. 本地最小实现已完成：natural import 默认成功 / 失败回复改成用户可读文本，不再向普通用户展示大段 `Natural file import diagnostics`。
2. `response.diagnostics` 与显式 debug render 仍保留机器诊断，避免影响测试 / 排障链路。
3. Fuzzy discovery 默认候选展示 safe alias / workspace / category，不展示 `document_id`、`version_id`、`workspace_id`、`chunk_count` 等技术 ID。
4. 验证：Hermes 主仓 py_compile 通过；targeted suite `38 passed`；扩展回归 `130 passed`。
5. 当前未执行 OpenWebUI / 8642 live smoke，未上传文件，未写 DB / facts / versions / OpenSearch / Qdrant。
6. Codex B review 已通过，runtime candidate 已推送：Hermes main `e04cc6feb` / `phase-2.116-natural-import-response-polish-runtime-candidate`。
7. Codex C / 测试机验证返回 `No-Go`：Case 4 fuzzy discovery raw path output；Case 2 alias retrieval third-document contamination signal。
8. 下一步 Phase 2.116b 只修复 fuzzy discovery raw path 泄露与 alias retrieval contamination signal。
9. 禁止把本轮扩展为 upload、ingestion、retrieval、workspace inference、platform Gateway、NAS 或 rollout 改动。

## Phase 2.116b Natural Import Response Polish No-Go Fix

1. 本地最小修复已完成：fuzzy discovery default candidate display 不再把 `title/source_name/display_path` 的绝对路径原样暴露给用户。
2. 同会话 alias retrieval 的 contamination trace 现在会基于实际 returned evidence 覆盖 stale `third_document_contamination`，in-scope evidence 不再误报第三文件污染。
3. 验证通过：targeted regression `2 passed`；py_compile 通过；natural import / flow / session scope / structured citation / file steward regression `132 passed`。
4. Codex B review 通过，runtime candidate 已推送：Hermes main `f887d12bf` / `phase-2.116b-natural-import-response-polish-fix-runtime-candidate`。
5. Codex C 在正确 2.116b 版本上复验仍返回 `No-Go`：Case 2 `third_document_contamination=true`，Case 4 `raw_path_output=true` 且 `safe_candidates_present=false`。
6. 2.116b 不能 stable closeout；下一步进入 2.116c root-cause-first 修复。

## Phase 2.116c Natural Import Live No-Go Root Cause Fix

1. 目标：先定位 live No-Go 根因，再最小修复 Case 2 与 Case 4。
2. Case 2 必须证明最终暴露的 `third_document_contamination` 来自哪个 trace/context 字段，并只清除 stale false positive，不隐藏真实第三文件污染。
3. Case 4 必须找出 raw path 从哪个字段穿透到用户输出，并在有候选时输出 safe candidate，而不是空候选。
4. 禁止改 upload / ingestion / indexing / broad retrieval / workspace inference / platform Gateway / NAS / rollout。
5. 本地根因定位已完成：Case 2 可能由 nested `retrieval_trace` / `context_scope` stale contamination 字段穿透；Case 4 可能由 `source_uri`、`alias_source_name`、active document hint、retrieval evidence / citation source 等非 candidate title 字段穿透。
6. 本地最小修复已完成：contamination normalization 同步覆盖 top-level / nested trace；file candidate、active document、evidence / citation source 都做 safe display，`file://` / `nas://` / `smb://` / `/Users` / `/Volumes` 只显示 basename。
7. 验证：live-shape targeted tests `4 passed`；py_compile 通过；required regression `135 passed`。
8. Codex B review 通过，runtime candidate 已推送：Hermes main `ff11f177c` / `phase-2.116c-live-no-go-root-cause-runtime-candidate`。
9. 下一步：Codex C / 测试机重跑 Phase 2.116 live validation。

## Phase 2.115 Workspace Context / Auto Alias / Fuzzy Discovery

1. 本地 runtime candidate 已完成：Hermes 主仓支持从安全文件名 / folder label / query 推断 `workspace_context`，并在无显式 alias 时生成安全 alias。
2. Generated alias 可绑定到 imported `document_id/version_id`，并携带 workspace metadata 供后续 fuzzy file discovery 使用。
3. Fuzzy discovery 只返回 safe alias / workspace / category 候选；不输出 raw path、raw content、secret，不把 diagnostics 当 retrieval evidence。
4. 验证已通过：py_compile、`git diff --check`、natural import / runtime / session scope regression `129 passed`。
5. 当前仍需 Codex B review 与 Codex C / 测试机真实 OpenWebUI / 8642 复验；不得直接宣布 Phase 2.115 收口。
6. 禁止扩展到 NAS scan、DWG/RVT/BIM 内容理解、platform Gateway 改造、production rollout、repair/backfill/reindex/delete/migration。


## Phase 2.113 Hermes Memory Self-Awareness / Kernel Activation

1. 用户真实 OpenWebUI / 8642 使用暴露 P0 blocker：Hermes 可以打通 import / retrieval pipeline，但用户侧 Agent 不可靠地知道自己拥有 Hermes_memory / workspace / retrieval / evidence kernel。
2. 这不是单纯文案问题；如果不修，Hermes 会退化为普通聊天壳 + 外置记忆库，偏离 PRD 中“企业内核级 Agent”的定位。
3. Phase 2.113 目标：Codex A 最小 runtime 修复，让 Hermes 在能力说明、自然导入成功反馈、自动/推荐别名、模糊找文件、低敏 memory/workspace 边界上表现为公司内核 Agent。
4. 必须保持证据边界：alias / memory / workspace metadata 只能作为检索上下文，不能当 content evidence；回答仍需 retrieval citation 或 Missing Evidence。
5. 必须保持安全边界：不扫 NAS、不生产 rollout、不裸连 DB、不生成 SQL、不写 raw content/path/secret 到 memory、不承诺 DWG/RVT/BIM 内容理解。
6. Codex A 需要补 targeted tests：self-awareness、explicit alias、auto alias、fuzzy discovery、memory boundary、DWG/RVT/BIM overclaim guard。
7. Phase 2.112i scoped natural import Go 仍有效，但 Phase 2 full completion 继续 blocked，直到 2.113 P0 修复并通过 review / 测试机验证。

## Phase 2 Natural Import Closeout Review / Freeze Checklist Update

1. Phase 2.112i test-machine Go is now reflected as `passed_with_scope` for authorized small `.xlsx` natural-language import.
2. Accepted evidence: Hermes_memory health pass, 8642 health pass, real upload flag visible, explicit alias resolved, retrieval not suppressed, evidence IDs non-empty, citation present, and no third-document contamination.
3. Natural import no longer blocks closeout within this narrow scope.
4. Full Phase 2 completion remains blocked until remaining PRD / Roadmap P0/P1 acceptance gaps are closed or explicitly reclassified.
5. Stable platform Gateway path remains catalog-only and separate from standalone Hermes import/evidence path.
6. Hermes retains standalone enterprise kernel identity and future workspace/context/memory/evidence roadmap.
7. Out of scope: production rollout, NAS full scan, DWG/RVT/BIM content understanding, large-file parser/indexing, automatic long-term memory writes for file content, repair/reindex/cleanup automation, and unrestricted natural-language import.
8. Next action: Codex B review, then selective docs / manifest baseline if accepted.

## Phase 2.112i Test-machine Retrieval Backend Environment Fix

1. Phase 2.112h test-machine alias gate passed: requested `@建筑类数据样表` was preserved, follow-up alias resolved, `alias_missing=false`, and `stable_owner_missing=false`.
2. Remaining blocker is retrieval backend environment, not alias code: reported root cause was `retrieval_backend_failed_postgres_hostname_unresolved`.
3. Do not treat development-machine local service availability as the test-machine result. The trusted test-machine result is alias resolved plus retrieval backend DB hostname unresolved.
4. Do not modify Hermes agent alias parser / continuity code for this blocker.
5. Next required action is environment-level: make Hermes_memory API use a DB hostname that matches its run mode. Docker compose mode may use service hostname; host/launchd mode needs an approved host-accessible endpoint.
6. After services are healthy, rerun at most one follow-up retrieval for `@建筑类数据样表`; repeat import only if restart lost session continuity.
7. Completed on test machine: Hermes_memory health pass, 8642 health pass, `alias_resolved`, `retrieval_suppressed=false`, non-empty retrieval evidence IDs, and citation present.
8. Natural import closeout blocker is cleared for authorized small `.xlsx` scope; broader sample matrix / production rollout remains out of scope.

## Phase 2.112h Explicit Natural Import Alias Preservation Fix

0. Development fix completed on 2026-05-22: explicit natural-language alias parsing now preserves requested `@建筑类数据样表`; targeted parser / flow / runtime tests `15 passed`; py_compile passed; natural import / upload client / session scope regression `124 passed`.
1. Phase 2.112g test-machine validation returned Pause: stable-owner candidate was deployed, import succeeded, but the imported alias did not match the user-requested `@建筑类数据样表`.
2. Follow-up query used `@建筑类数据样表`; because that exact alias was not stored, retrieval still returned `alias_missing=true` and `retrieval_suppressed=true`.
3. Codex B read-only review indicates this is a natural import alias parsing / preservation bug, not another stable-owner restore bug.
4. Likely minimal root cause: `agent/memory_kernel/natural_file_import.py::_ALIAS_RE` does not cover common natural-language alias forms such as `别名 @...`, `别名为 @...`, `别名设为 @...`, or `设定别名为 @...`.
5. Phase 2.112h task status: implemented locally; requested alias wins over generated alias; malformed aliases remain `not_requested`; follow-up restore is covered by tests.
6. Keep all previous safety rules: no alias-global restore, no ordinary memory alias persistence, no raw path/owner/token/content diagnostics, no DB/index/NAS/rollout.
7. Codex B review passed on 2026-05-22; runtime test-candidate pushed: Hermes agent commit `e1d38e1ec`, tag `phase-2.112h-explicit-import-alias-runtime-test-candidate`.
8. Test-machine validation on 2026-05-22 proved the explicit requested alias gate passed: import alias was exactly `@建筑类数据样表`, follow-up returned `alias_resolution.status=alias_resolved`, `alias_missing=false`, and `stable_owner_missing=false`.
9. New blocker is environment / retrieval backend: `retrieval_suppressed=true`, reason `retrieval_backend_failed`, specifically `retrieval_backend_failed_postgres_hostname_unresolved`.
10. Full Phase 2 natural import closeout remains blocked until the test-machine Hermes_memory retrieval backend can reach its DB and follow-up returns non-empty retrieval evidence + citation.

## Phase 2.112g Header-only Stable Owner Restore Fix

1. Phase 2.112g development-machine 最小修复已完成：header-only `X-Hermes-Session-Id` 被纳入 gateway stable owner fallback。
2. accepted import turn 与 header-only follow-up 会生成同一 safe owner，避免 `retrieval_stable_owner_missing=true` 导致 alias continuity restore 失败。
3. 新增 gateway targeted tests 覆盖 header-only owner、owner equivalence、follow-up restore scoped filters 与 no `stable_owner_missing`。
4. 验证：py_compile 通过；targeted gateway tests `3 passed`；natural import / upload client / session scope regression `109 passed`。
5. 当前主仓 `.venv` 缺 async pytest 插件，完整 `tests/gateway/test_api_server.py` false-fail existing async tests；不得将该环境问题误判为 2.112g 代码回归。
6. Keep all previous safety rules: no alias-global restore, no ordinary memory alias persistence, no raw owner diagnostics, no DB/index/NAS/rollout.
7. Codex B review 已通过；runtime test-candidate 已推送：Hermes agent commit `20d9fb561`，tag `phase-2.112g-header-owner-restore-runtime-test-candidate`。
8. 下一步：测试机 OpenWebUI / 8642 真实复验 import -> follow-up `@alias` retrieval + citation。

## Phase 2.112f Alias Continuity Restore Fix

1. Phase 2.112e test-machine validation returned Pause: import succeeded and `alias_continuity_status=stored`, but follow-up `@建筑类数据样表` still returned `alias_missing=true` and `retrieval_suppressed=true`.
2. Read-only diagnostics confirmed `X-Hermes-Session-Id` was present, import owner source was `gateway_session_key`, and `stable_owner_missing` did not appear during import.
3. Follow-up response exposed `alias_resolution.status=alias_missing` but did not expose `alias_continuity_status`, `alias_continuity_owner_source`, `alias_continuity_persistent`, or `stable_owner_missing`.
4. Current root-cause category: `hermes_alias_store_restore_bug`.
5. Phase 2.112f Codex A task: fix owner-scoped alias continuity restore in the follow-up alias-missing branch and always emit sanitized continuity diagnostics.
6. Alias-global restore, ordinary memory alias persistence, DB/index writes, NAS scan, repair/reindex/rollout remain forbidden.
7. Full Phase 2 natural import closeout remains blocked until test-machine OpenWebUI / 8642 validates import -> `@alias` retrieval evidence + citation.

## Phase 2.112e API Server Stable Owner Bridge Fix

1. Codex A implemented the API server stable-owner bridge and Codex B review passed at development-machine level.
2. API server now passes accepted `X-Hermes-Session-Id` or whitelisted OpenWebUI conversation headers as `gateway_session_key` into `AIAgent`.
3. Owner values remain hashed by `SessionDocumentScopeStore`; diagnostics expose source labels only.
4. Missing stable owner remains fail-closed with sanitized `stable_owner_missing`; alias-global restore remains forbidden.
5. Runtime test-candidate pushed: Hermes agent commit `091fd7414`, tag `phase-2.112e-api-server-owner-bridge-runtime-test-candidate`.
6. Next blocker: test-machine OpenWebUI / 8642 natural import -> `@alias` retrieval + citation validation.

## Phase 2.112d Alias Continuity Scope Review Fix

1. Codex A 已完成 owner-scoped continuity 小修；Phase 2.112c alias-global blocker 已在代码侧解除。
2. Continuity registry 改为 safe owner key + alias 双层索引；stable owner key 哈希化，不输出 raw owner。
3. 无 stable owner 时只用 process-local non-persistent fallback；不会跨 store reload 恢复 unscoped alias。
4. TTL/stale cleanup、cross-owner denial、unscoped non-persistence、conflict fail-closed 均有目标测试覆盖。
5. 当前仍不允许 runtime baseline；先 Codex B review，再决定 selective test-candidate tag 与测试机 OpenWebUI / 8642 validation。

## Phase 2.112c OpenWebUI Alias Continuity Fix

1. Phase 2.112b test-machine validation paused because upload/index worked but follow-up `@建筑类数据样表` returned `alias_missing=true`, `retrieval_suppressed=true`, empty evidence, and no citation.
2. Root cause: OpenAI-compatible / OpenWebUI follow-up request may include only the latest user message and derive a different `api-*` backend session id, so previous assistant diagnostics are unavailable.
3. Codex A Phase 2.112c implementation is now complete in Hermes main: successful natural import stores bounded alias-continuity records outside ordinary memory; unambiguous follow-up `@alias` restores scoped `document_id/version_id`; conflicting candidates suppress retrieval.
4. Sanitized diagnostics now include `alias_continuity_status`, `alias_continuity_source`, `api_session_key_source`, and `history_message_count`; import diagnostics remain non-evidence and do not expose raw paths.
5. Development validation passed: py_compile; natural import / upload client / session scope regression `102 passed`; gateway latest-user drift test `1 passed`.
6. Current next step: Codex B review Phase 2.112c diff; if accepted, authorize selective runtime test-candidate baseline/tag.
7. After review/baseline, test machine must rerun real OpenWebUI / 8642 natural import follow-up and prove retrieval evidence + citation from imported document.
8. Phase 2 full closeout remains blocked until real OpenWebUI / 8642 alias + retrieval + citation validation passes.

## Phase 2.112b Natural Import Alias Binding / Retrieval Blocker Fix

1. 测试机真实 OpenWebUI / 8642 验收已证明 natural import upload/index 成功：`document_id=6e89bbe8-599f-47e3-9cca-d8e7b7ae4f1b`、`version_id=0df440d0-9f2b-4fd5-8a84-19435fdd1b2f`、`chunk_count=6`、`indexed_count=6`。
2. 当前 Pause 原因是 alias 链路：标题绑定 `alias_bind_failed`，follow-up `@建筑类数据样表` 返回 `alias_missing=true` 与 `retrieval_suppressed=true`。
3. Codex A 已完成最小 runtime fix：从同一 conversation history 的 natural import diagnostics 恢复 alias；已存在导入 alias 的 title rebind 不再因 resolver miss 失败。
4. 已验证开发侧目标测试：py_compile 通过，natural import / upload client / session scope regression `99 passed`。
5. Codex B review 已通过；Hermes agent runtime test-candidate 已推送：commit `1d02a7918`，tag `phase-2.112b-natural-import-alias-runtime-test-candidate`。
6. 下一步由测试机 Codex checkout 该 tag，并执行 Mac mini / OpenWebUI / 8642 真实 alias + retrieval + citation 验收。
7. Phase 2.112 仍不得 final runtime baseline，直到测试机真实验收通过。

## Phase 2.112 Codex B Review / Codex C Validation Pending

1. Codex A implementation 已完成，Codex B 复核 targeted tests：`97 passed`。
2. Review 通过，但不建议 baseline；必须先跑真实 OpenWebUI / 8642 natural import -> `@alias` same-session retrieval / citation。
3. 已更新 `docs/NEXT_CODEX_C_PROMPT.md`，覆盖 explicit alias import、auto alias import、bounded fuzzy file discovery、ordinary memory 不作为 alias persistence。
4. 主仓存在无关 dirty，Phase 2.112 baseline 必须 selective staging。


## Phase 2.112 Natural Import Workspace Retrieval Fix

1. 用户真实 OpenWebUI / 8642 测试已证明 natural import real upload path 可执行：`real_upload_enabled=true`、`upload_adapter_status=executed`、`ingestion_status=upload_succeeded`、`document_id=2baf5527-42c9-4467-8856-573e54c97121`、`version_id=b2efc465-cde8-4aef-a113-5c8615929719`、`chunk_count=6`、`indexed_count=6`。
2. Codex A 已完成最小实现：无 alias 导入会生成安全 alias；成功导入后 alias 持久化为 `alias_bound`；same-session `@alias` 查询带 `document_id/version_id` scoped filters；diagnostics 不再停留在 `alias_seeded`。
3. 已补 bounded safe fuzzy discovery：仅扫描当前 session aliases，返回候选并 `suppress_retrieval=true`，避免把模糊找文件请求误送普通 retrieval。
4. 主仓目标验证通过：py_compile 通过，natural import / upload adapter / session scope targeted regression `97 passed`。
5. 当前仍需 Codex B review 与 Codex C 真实验收：real upload 后必须证明 same-session retrieval evidence 只含 imported document 且 citation 真实存在。
6. Phase 2 full closeout 仍 blocked，直到 Phase 2.112 真实验收通过；global workspace metadata discovery、NAS scan、DB CRUD、Gateway contract、rollout 继续禁止 / 后置。


## Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack

1. Phase 2.110 baseline 已完成并推送：commit `1a07e42`，tag `phase-2.110-full-closeout-return-baseline`。
2. 已新增 `docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`、`eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json`、`docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md`。
3. Phase 2.111 结论：natural-language import 技术路径已有证明，但 full Phase 2 closeout 仍需 accepted Hermes CLI natural-language import smoke，或用户显式例外。
4. `proven`：intent detection、runtime hook、real upload path、feature flag authorization、sanitized evidence template、Mac mini checklist。
5. Updated after Phase 2.112i: Hermes / 8642 OpenWebUI-compatible natural-language import closeout smoke, same-session alias/retrieval/citation evidence, and third-document contamination check are `passed_with_scope` for authorized small `.xlsx`; broader non-developer usability remains future sample expansion.
6. 重点规则：direct API upload 不能替代 Hermes / 8642 OpenWebUI-compatible natural-language import；planning/mock evidence 不能替代 live usability evidence。
7. Codex B review 已通过；验证包括 matrix JSON parse、evidence template py_compile、目标 pytest `14 passed`。
8. 下一步：执行 selective docs / matrix baseline。真实 smoke 仍需用户授权具体小型非敏感文件。

## Phase 2.110 Phase 2 Full Closeout Return Plan

1. Phase 2.109 baseline 已完成并推送：commit `0156195`，tag `phase-2.109-final-freeze-checklist-baseline`。
2. Phase 2.110 目标是回答真实自然语言使用流程与完整 Phase 2 交付是否达标，并正式打回 full closeout。
3. 已新增 `docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md` 与 `eval/phase2_inventory/phase2_full_closeout_return_checklist.json`。
4. 当前真实自然语言流程是受控 operator / API / CLI / checklist 流程；还不是完全产品化的“一句话自动导入、入库、建别名、连续查询”体验。
5. 决策：stable platform baseline=`keep`；standalone kernel preservation=`keep`；full Phase 2 closeout=`returned`；Phase 2 completion announcement=`blocked`。
6. 仍需关闭或显式重分类：natural import usability、PRD 100+ / Roadmap 300+ eval、Top5 / citation 指标、structured fact spot-check、parser/source coverage、tender deep fields、version diff、full RBAC/ABAC、knowledge admin / human validation。
7. 下一步建议：Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack。不得宣布 full Phase 2 complete。

## Phase 2.109 Phase 2 Final Freeze Checklist

1. Phase 2.108 baseline 已完成并推送：commit `251a2f4`，tag `phase-2.108-standalone-kernel-freeze-contract-baseline`。
2. Phase 2.109 目标是 final freeze checklist，不是功能实现，也不是 production rollout。
3. 已新增 `docs/PHASE2109_PHASE2_FINAL_FREEZE_CHECKLIST.md` 与 `eval/phase2_inventory/phase2_final_freeze_checklist.json`。
4. 最终三段式判断：平台稳定集成 freeze=`go`；Hermes 独立内核保留=`go`；完整 Phase 2 PRD / Roadmap closeout=`pause`。
5. 平台 / 数据库团队可继续基于稳定 Hermes baseline 接入；Phase 3 planning 可带 known-gap carryover 进入。
6. 不得把 Phase 2 stable / final freeze 写成：生产 rollout、DWG/RVT/BIM 内容理解完成、Agent DB CRUD/SQL 完成、完整 PRD/Roadmap 指标完成。
7. 下一步：Codex B review Phase 2.109；通过后 selective docs / JSON baseline。

## Phase 2.108 Standalone Kernel Freeze Contract

1. 稳定平台集成基线已完成并推送：commit `fb3781a`，tag `phase-2-stable-hermes-platform-integration-baseline`。
2. Phase 2.108 目标是补齐 standalone Hermes kernel freeze contract，防止平台 catalog-only / Gateway 只读接入被误解为 Hermes 的产品上限。
3. 已新增 `docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md`，明确 Hermes=企业 Agent 内核，Platform=UI/Gateway/权限/数据表面，Data Steward/Catalog=Hermes 能力模块之一。
4. Phase 2 stable tag 继续代表平台安全集成基线：catalog-only、permission-aware、Missing Evidence、安全 IDs/traces、authorityHealth.orange、无 raw path/raw row/secret 泄露。
5. Phase 2.108 增加验收口径：即使测试机停在 Phase 2 stable tag，也不能阻塞后续平台逐步解锁 Hermes native session、Evidence Layer、Memory Layer、NAS governance 与 workspace 能力。
6. Phase 3+ 仍后置：production rollout、Agent DB CRUD/SQL、DWG/RVT/BIM 内容理解、NAS semantic collection、full Data Steward productization、orchestration runtime。
7. 下一步：Codex B review Phase 2.108；通过后 selective docs / checklist baseline。不得 stage 无关 `docs/digital-delivery-standards/`。

## Phase 2 Stable Hermes Platform Baseline Tag

1. Phase 2.107 baseline 已完成并推送：commit `3ef3966`，tag `phase-2.107-minimal-freeze-blocker-closure-baseline`。
2. 平台 0B Gateway hardening controlled live smoke 已回传 `Go`：`EXPECT_HERMES_AGENT_AVAILABLE=true`，`PASS=14 FAIL=0`。
3. 稳定平台集成 tag：`phase-2-stable-hermes-platform-integration-baseline`。
4. 当前稳定范围：catalog-only asset query、Gateway permission / redaction、Missing Evidence、安全 IDs / traces、authorityHealth.orange、responseId/queryId/traceId、safeMemoryCandidates=[]、sanitizedContextRefs=[]。
5. 当前不是 production rollout，不是 Phase 2 full PRD/Roadmap closeout，不是 Phase 3 transition。
6. known risk：native session/thread lifecycle、Evidence Layer、Memory runtime、target-scale metrics、natural import usability 仍后置或需业务决策。
7. 下一步：创建并推送 stable tag；测试机 checkout stable tag 后再决定 Phase 2 freeze 后续。

## Phase 2.107 Minimal Freeze Blocker Closure Plan

1. Phase 2.106 baseline 已完成：commit `fe2706d`，tag `phase-2.106-platform-stable-hermes-freeze-readiness-baseline`，pushed=true。
2. Phase 2 stable target 已定义为 `Phase 2 Stable Hermes for Platform Integration`，但还不能创建 stable tag 或声明 Phase 2 fully closed。
3. 已新增 `docs/PHASE2107_MINIMAL_FREEZE_BLOCKER_CLOSURE_PLAN.md` 与 `eval/phase2_inventory/minimal_freeze_blocker_closure_matrix.json`。
4. Codex B review 已纳入最新 Platform / DB Agent alignment report：当前外部 Hermes 接入仍是 OpenAI-compatible compatibility path，`architecture_authority_health=orange`，Gateway 安全边界接近 green。
5. 推荐最小 stable-tag blocker set：平台身份/权责 wording、Gateway 权限与 path redaction、catalog-only safe refs、Missing Evidence、shared contract sync、test-machine update、0B Gateway hardening、high-risk forbidden-field fail-closed、authority health orange、前端文案收束。
6. 可带风险冻结项：runtime session/thread refs、Evidence Layer、Memory runtime、feedback/scoring productization、eval count 与 Top5/citation target-scale gaps；runtime session/thread refs 只能在 0B Gateway 明示当前 `authority_health.orange` 与 placeholder fields 后冻结。
7. Phase 3+ 后置项：production rollout、full Data Steward productization、DWG/RVT/BIM content understanding、NAS semantic collection、Agent DB CRUD/SQL、repair executor。
8. 需要用户业务决策：natural language import / file governance usability 是否阻塞 stable tag。
9. 下一步：Codex B review Phase 2.107；通过后由用户显式授权 docs / matrix baseline。不得自动创建 stable tag 或进入 Phase 3。

## Phase 2.106 Platform Stable Hermes Freeze Readiness

1. Phase 2.105 baseline 已完成：commit `5cef214`，tag `phase-2.105-hermes-platform-authority-alignment-baseline`，pushed=true。
2. 共享 `DigitalDeliveryProject` 已同步 Hermes Kernel Authority Contract，避免平台 / 数据库 Agent 继续把 Hermes 当 stateless chat plugin。
3. 已新增 `docs/PHASE2106_PLATFORM_STABLE_HERMES_FREEZE_READINESS.md`、`docs/PLATFORM_STABLE_HERMES_CAPABILITY_BASELINE.md`、`docs/CODEX_TEST_MACHINE_UPDATE_TO_STABLE_HERMES_PROMPT.md`、`eval/phase2_inventory/platform_stable_hermes_freeze_checklist.json`。
4. 推荐冻结目标：`Phase 2 Stable Hermes for Platform Integration`，用于给平台一个稳定、功能清晰、边界可依赖的 Hermes baseline。
5. 冻结范围仅包含 catalog-only asset query、Gateway permission / redaction、Missing Evidence、安全 IDs、query / trace、共享契约、Hermes 内核权责边界与 known risk list。
6. 不进入冻结范围：production rollout、DWG/RVT/BIM 内容理解、NAS semantic collection、Agent DB CRUD、Agent SQL、自动 repair/reindex/cleanup、full Data Steward productization、Phase 2 full PRD/Roadmap closeout。
7. 当前已知风险：runtime session refs、Evidence Layer、Memory Layer、target-scale metrics、natural import usability 仍未完全产品化或需要业务裁决。
8. 下一步：Codex B review Phase 2.106；通过后由用户显式授权 docs / checklist baseline。不得自动进入 Phase 2.107 或 Phase 3。

## Phase 2.105 Hermes Kernel Authority / Platform Alignment Contract

1. Phase 2.104d baseline 已完成：commit `f0fabc4`，tag `phase-2.104d-feedback-scoring-linkage-contract-baseline`，pushed=true。
2. Phase 2.105 已新增 `docs/PHASE2105_HERMES_PLATFORM_AUTHORITY_ALIGNMENT.md`、`docs/PLATFORM_TEAM_HERMES_KERNEL_AUTHORITY_ALIGNMENT_HANDOFF.md`、`eval/phase2_inventory/hermes_platform_authority_alignment_examples.json`。
3. 核心结论：Hermes=enterprise agent kernel；Platform=UI + Gateway + permission/data surface；Data Steward/Catalog=Hermes 能力模块之一，不是 Hermes 全貌。
4. 最小修复原则：不推翻当前 Gateway 权限、path redaction、catalog-only 安全架构；只补 session / reasoning / orchestration ownership contract。
5. Contract 已说明：平台不能只把 Hermes 当 stateless endpoint；应传递 `session_id` / `thread_id` / sanitized context refs；Hermes 应返回 response/query/trace/context/tool-plan/memory-candidate 等内核语义。
6. Fixtures 共 9 条，覆盖 plugin mode pause、kernel session owner go、project switch revalidation、frontend history denied、Data Steward module boundary、memory ref Missing Evidence、Gateway redaction、tool orchestration summary、raw transcript rejected。
7. 本阶段仍只做 docs / contract fixtures；不改 runtime code、不改平台 repo、不改共享文件、不实现 Gateway/session runtime、不连接 DB/NAS/API、不跑 smoke。
8. 下一步：Codex B review Phase 2.105；通过后由用户显式授权 docs / fixture baseline。不得自动进入 runtime session implementation。

## Phase 2.104d Feedback / Scoring Linkage Contract Planning

1. Phase 2.104c baseline 已完成：commit `1bb9ca3`，tag `phase-2.104c-document-evidence-search-contract-baseline`，pushed=true。
2. Phase 2.104d 已新增 `docs/PHASE2104D_FEEDBACK_SCORING_LINKAGE_CONTRACT.md` 与 `eval/phase2_inventory/feedback_scoring_linkage_examples.json`。
3. 核心原则：feedback 是 evaluation signal，不是 evidence、permission proof、fact、repair trigger 或自动 metric pass。
4. Contract 已定义 feedback labels、sanitized input shape、linkage outcomes、scoring linkage rules、memory linkage rules。
5. Fixtures 共 9 条，覆盖 helpful positive signal、wrong document、citation problem、missing evidence、wrong boundary、permission problem、overclaim、sensitive note rejected、low-sensitive memory hint after review。
6. 官方 scoring effect 必须等待 reviewed sanitized result row；`helpful` 不能自动 pass，negative feedback 不能自动 repair。
7. 本阶段只做 docs / contract fixtures；不写 runtime code、不改 tests、不改 scoring scripts、不实现 feedback ingestion、不写 memory/facts/issues。
8. 下一步：Codex B review Phase 2.104d；通过后由用户显式授权 docs / fixture baseline。不得自动进入 Phase 2.104e。

## Phase 2.104c Governed Document Evidence Search Contract Planning

1. Phase 2.104b baseline 已完成：commit `d67d7ea`，tag `phase-2.104b-memory-continuity-permission-contract-baseline`，pushed=true。
2. Phase 2.104c 已新增 `docs/PHASE2104C_DOCUMENT_EVIDENCE_SEARCH_CONTRACT_PLAN.md` 与 `eval/phase2_inventory/document_evidence_search_contract_examples.json`。
3. 核心原则：没有当前 Platform permission proof、没有允许 evidence query 的 Evidence Availability、没有 citation-bearing governed evidence，就不能回答正文内容。
4. Contract 已定义 gate sequence：platform permission、catalog permission、evidence availability、memory candidate、document evidence query、citation response、Missing Evidence fallback。
5. Fixtures 共 9 条，覆盖 PDF citation、DWG catalog-only block、PDF parser-required block、permission denied、memory reference only、Excel structured citation、meeting transcript boundary、conflicting evidence、RVT component Missing Evidence。
6. `document_evidence_search` 仍是 future-only contract，不是当前 runtime tool。
7. 本阶段只做 docs / contract fixtures；不写 runtime code、不改 tests、不实现 `document_evidence_search`、不跑 DB/NAS/Gateway/API smoke。
8. 下一步：Codex B review Phase 2.104c；通过后由用户显式授权 docs / fixture baseline。不得自动进入 Phase 2.104d。

## Phase 2.104b Low-sensitive Memory Continuity + Permission Boundary Contract

1. Phase 2.104a baseline 已完成：commit `db15d5e`，tag `phase-2.104a-evidence-availability-contract-baseline`，pushed=true。
2. Phase 2.104b 已新增 `docs/PHASE2104B_MEMORY_CONTINUITY_PERMISSION_CONTRACT.md` 与 `eval/phase2_inventory/memory_continuity_permission_examples.json`。
3. 已拆清三层：Platform permission proof 是最终授权；catalog permission decision 只对当前目录响应有效；Hermes memory continuity 只能作为低敏 UX hint。
4. Contract 已明确允许低敏 memory 字段：`related_file_ids`、`related_model_ids`、`query_id`、`trace_id`、`feedback_label`、`last_safe_project_context_label`、`preferred_result_grouping`、`last_evidence_mode`、`last_permission_decision_summary`。
5. Contract 已明确 forbidden memory fields：raw `storage_path`、raw NAS path、raw DB/catalog row、文件正文、DWG/RVT/BIM 内容、客户敏感 note、secret/token/password、full permission proof、未授权 ACL snapshot。
6. Fixture cases 共 8 条，覆盖 current allowed、project switch denied、permission refresh、safe feedback label、raw path rejected、customer note rejected、catalog-only related model、denied no bypass。
7. 本阶段只做 docs / contract fixtures；不写 runtime code、不改 tests、不实现 memory runtime、不跑 DB/NAS/Gateway/API smoke。
8. 下一步：Codex B review Phase 2.104b；通过后由用户显式授权 docs / fixture baseline。不得自动进入 Phase 2.104c。

## Phase 2.104a Evidence Availability Contract Docs + Fixtures

1. Phase 2.104 baseline 已完成：commit `e2c1d3c`，tag `phase-2.104-platform-layered-capability-plan-baseline`，pushed=true。
2. Phase 2.104a 已新增 `docs/PHASE2104A_EVIDENCE_AVAILABILITY_CONTRACT.md` 与 `eval/phase2_inventory/evidence_availability_contract_examples.json`。
3. Contract semantics 已覆盖 `catalog_only`、`parser_required`、`evidence_indexed`、`unsupported_type`、`permission_denied`、`manual_review_required`。
4. Fixture cases 共 7 条：DWG catalog-only、RVT catalog-only、PDF parser-required、Office evidence-indexed、unsupported BIM model、permission denied、manual review required。
5. fixtures 使用 fake IDs，不包含真实项目名、真实文件名、raw path、raw row、asset_uid、source_id、secret 或客户敏感内容。
6. 本阶段只做 docs / contract fixtures；不写 runtime code、不改 tests、不实现新 tool、不跑 DB/NAS/Gateway/API smoke。
7. 当前仍禁止：`document_evidence_search` runtime、Agent DB CRUD、Agent SQL、NAS scan、DWG/RVT/BIM 内容理解、NAS semantic collection、DB/index/object-store/memory 写入、production rollout。
8. 下一步：Codex B review Phase 2.104a；通过后由用户显式授权 docs / fixture baseline。不得自动进入 Phase 2.104b。

## Phase 2.104 Platform Layered Capability Plan

1. Phase 2.103 baseline 已完成：commit `3c38a06`，tag `phase-2.103-test-machine-capability-handoff-baseline`，pushed=true。
2. 测试机已成功 checkout Phase 2.103；docs-only handoff 可用，pytest 因 runtime 缺依赖被允许记录为 skipped。
3. Phase 2.104 已新增 `docs/PHASE2104_PLATFORM_LAYERED_CAPABILITY_PLAN.md`：Catalog Layer=current，Evidence Layer=next，Memory Layer=next，Orchestration Layer=later。
4. 计划已明确需要的 platform / Gateway contracts：Evidence Availability、future Document Evidence Search、low-sensitive Memory Continuity、Feedback、Capability Response。
5. 共享 `DigitalDeliveryProject` 已核对：`agent-briefings/hermes_capability_handoff.md` 与 `docs/01_capability_matrix.md` 已有 Hermes layers 条目；本阶段未修改共享文件。
6. 本阶段只做 docs / contract planning，不写 runtime code、不改 tests、不实现新 tool、不跑 DB/NAS/Gateway/API smoke。
7. 当前仍禁止：Agent DB CRUD、Agent SQL、NAS scan、DWG/RVT/BIM 内容理解、NAS semantic collection、DB/index/object-store/memory 写入、production rollout。
8. 下一步：Codex B review Phase 2.104；通过后由用户显式授权 docs baseline。不得自动进入 Phase 2.104a。

## Phase 2.103 Test Machine Update + Hermes Capability Maximization Handoff

1. Phase 2.102b baseline 已完成：commit `5c37661`，tag `phase-2.102b-metric-scoring-pack-baseline`，pushed=true。
2. Phase 2.103 docs / handoff pack 已完成；Phase 2.103a 已修复 Codex B wording blocker。
3. 已新增测试机更新 prompt、数据库 / 平台团队 Hermes 能力最大化接入说明、Hermes 开发口号与阶段总结。
4. Hermes 当前对平台的定位：evidence-first enterprise memory kernel + permission-aware catalog agent，不是普通聊天框、SQL Agent、NAS reader 或 DWG/RVT/BIM 内容理解 Agent。
5. 当前必须坚持：catalog-only、read-only、permission-aware、Missing Evidence、low-sensitive related IDs memory；`related_file_ids` / `query_id` / feedback labels 不是 file正文 evidence。
6. Phase 2 closeout readiness 仍为否：仍缺 PRD 100+ / Roadmap 300+ eval cases、reviewed result JSON、真实 Top5 / citation scoring、structured fact manual spot-check。
7. 下一步：Codex B re-review Phase 2.103a；通过后由用户显式授权 selective docs baseline。

## Phase 2.102b Metric Scoring Pack

1. Phase 2.102b local/offline scorer implementation 已完成，等待 Codex B review。
2. 新增 `scripts/phase2102b_metric_scoring_pack.py`，读取 committed manifest 与显式输入的 sanitized results JSON，计算 Top5 / citation rate / forbidden behavior summary。
3. Scoring denominator 只包含 `metric_eligible=true` cases；`metric_eligible=false` cases 只进入 excluded summary。
4. 缺失 eligible result 输出 `status=incomplete`；任何 known result row 的 forbidden behavior 都输出 `status=blocked_for_review`，包括 `metric_eligible=false` cases。
5. Scorer 拒绝 raw text / raw rows / NAS path / storage path / secret 类结果字段。
6. 已通过目标测试与离线校验；Codex B review blocker 已修复；本阶段未运行 Hermes runtime、未连接 DB/NAS/Gateway、未写任何 DB/index/object-store/memory。
7. 当前 19-case starter inventory 仍不满足 PRD 100+ / Roadmap 300+；Phase 2 closeout readiness 仍为否。
8. 下一步：Codex B re-review Phase 2.102b；通过后由用户显式授权 selective baseline。

## Phase 2.102a Eval Inventory Manifest

1. Phase 2.102a 是 metric scoring 前置阶段：先建立 accepted eval inventory，后续 Phase 2.102b 才能计算 Top5 / citation accuracy。
2. Manifest 必须包含 schema、source refs、target counts、summary、cases、known gaps 与 safety boundaries。
3. 每个 case 必须包含 `case_id`、`group`、`question`、`source_category`、`expected_evidence_mode`、`expected_document_refs`、`expected_citation_fields`、`forbidden_behaviors`、`metric_eligible`、`metric_exclusion_reason`、`evidence_ref`、`notes`。
4. 如果 committed evidence 不足，case 应标 `metric_eligible=false`，不能编造 100+ / 300+ 数量或指标。
5. 既有 untracked `docs/digital-delivery-standards/` 仍不属于本阶段，默认不得 stage。


## Phase 2.102a Eval Inventory Manifest

1. Phase 2.102a docs/data-manifest step 已完成：新增 `eval/phase2_inventory/phase2_eval_inventory_manifest.json` 与 `docs/PHASE2102A_EVAL_INVENTORY_MANIFEST.md`。
2. Starter inventory 当前包含 19 个 accepted cases、15 个 metric-eligible cases、4 个 metric-ineligible cases，覆盖 12 个 required groups。
3. 当前明确未满足：PRD 100+、Roadmap 300+、Top5 80/85、citation 85/90、structured fact manual spot-check 90。
4. Gateway / Data Steward / Missing Evidence / natural import 当前作为 boundary / planning / smoke evidence 保留为 metric-ineligible，不得计入 Top5 / citation denominator。
5. 下一步：Codex B review Phase 2.102a manifest；通过后由用户显式授权 selective docs/data baseline。
6. 不得自动进入 Phase 2.102b scoring；scoring 前必须先确认 inventory boundary。

## Phase 2.102 Metric / Evaluation Evidence Pack

1. Phase 2.102 docs-only evidence pack 已完成：新增 `docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md`。
2. Evidence pack 已区分 `measured_pass`、`measured_fail`、`partial_evidence`、`smoke_only_not_metric`、`missing_metric`、`requires_user_decision`，避免把 smoke 误当百分比指标。
3. 当前结论：Phase 2 metric closeout decision=`not_ready`。
4. 主要 blocker：PRD 100+ / Roadmap 300+ eval inventory、Top5 80/85、citation 85/90、structured fact manual spot-check 90 均缺 committed numerator / denominator。
5. Permission、parser/source、Gateway/Data Steward、Mac mini / employee trial、natural import、Missing Evidence、facts/transcript/version boundary 已有 partial 或 smoke evidence，但不足以关闭 PRD/Roadmap metric。
6. 下一步：Codex B review Phase 2.102 evidence pack；通过后由用户显式授权 selective docs baseline。
7. Phase 3+ 仍后置：Data Steward productization、DWG/RVT/BIM content understanding、graph/spatial、production rollout、repair executor。


## Phase 2.101 PRD Acceptance Gap Closure Plan

1. Phase 2.101 已完成 docs-only gap closure planning：新增 `docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md`。
2. 该文档把 Phase 2.100a audit gap 分为：`phase2_closeout_blocker`、`phase2_evidence_pack_required`、`phase2_backlog_candidate_user_decision`、`phase3_plus_candidate_user_decision`、`already_satisfied_keep_evidence`。
3. 已覆盖结构化实体关系、结构化 facts、标书深层字段、权限、反馈闭环、评测指标、知识管理员、人审流程、parser/source evidence、Mac mini / employee trial、自然语言导入、Gateway、Data Steward catalog-only / Phase 3+ 产品化。
4. Phase 2 closeout readiness 当前仍为否；该计划只给出决策地图，不关闭任何 gap。
5. 下一步：Codex B review Phase 2.101；通过后由用户显式授权 selective docs baseline。
6. 后续优先路线：Phase 2.102 metric / evidence pack、Phase 2.103 tender deep-field closure or backlog decision、Phase 2.104 feedback/admin/human validation scope decision。
7. Phase 3+ 仍后置：Data Steward productization、BIM/DWG/RVT deep parsing、graph/spatial、multi-agent orchestration、production rollout、repair executor、complete auto facts extraction。


## Phase 2.100a Boundary Acceptance Audit Coverage Fix

1. Phase 2.100 audit document 已完成首版：`docs/PHASE2100_PHASE2_PHASE3_BOUNDARY_ACCEPTANCE_AUDIT.md`。
2. Codex B review blocker：PRD §13 MVP acceptance rows、Data Steward Phase 2 vs Phase 3+ split、automatic eval pipeline / retrieval quality dashboard rows、文档卫生需要修复。
3. 当前结论仍为：Phase 2 closeout readiness=否；当前可作为内部受控 MVP 候选继续治理，但不能声称已满足原始 Roadmap Phase 2 验收。
4. 下一步建议：Codex A 完成 Phase 2.100a coverage fix 后停止等待 Codex B review；通过后再考虑 selective docs baseline 或 Phase 2.101 PRD acceptance gap closure plan。
5. Phase 3+ 仍后置：Data Steward productization、BIM/DWG/RVT deep parsing、production rollout、repair executor、full RBAC/ABAC、raw audio ASR、complete auto facts extraction。

## Data Steward / NAS Catalog-only Risk Boundary

1. 新增 `docs/DATA_STEWARD_AGENT_RISK_BOUNDARY.md`，作为后续 Hermes Data Steward / NAS / DB catalog-only 接入的风险边界。
2. 项目内企业 Agent 正式名称统一为 Hermes，不使用 Jarvis。
3. 后续 Catalog Tool、Gateway、前端文案、prompt 与 feedback 设计必须遵守：catalog metadata 不等于正文 evidence；Hermes memory 不等于 NAS 内容索引；只读 Catalog Tool 不等于 SQL Tool。
4. Backlog 优先级：只读 `asset_catalog_search` tool 产品化、结构化输出 `query_id/file_id/model_id/source_view`、路径脱敏、Missing Evidence 模板、prompt/tool description 审计、feedback 不直接写 long-term memory、`related_file_ids` 低敏 memory 规则、未来 NAS semantic collection 独立设计。

## 最新状态

1. Phase 2.98 baseline 已完成：commit `40f71b9`，tag `phase-2.98-standard-agent-boundary-review-baseline`，pushed=true。
2. Phase 2.99 Standard Boundary Prompt / Tool Description Alignment 已完成首轮 implementation，新增 `app/services/asset_catalog/standard_answer_boundary.py` 与目标测试。
3. Phase 2.99a 已修复 Codex B review blocker：`docx` / `xlsx` 正文类问题现在返回 `missing_evidence` + `full_text_evidence`。
4. TDD RED/GREEN 已观察，目标测试已从 `9 passed` 扩展为 `11 passed`；explicit probe 中 `docx/xlsx/pptx/pdf` 均返回 expected Missing Evidence。
5. Phase 2.99 未连接 DB/NAS/API，未运行 Gateway smoke，未修改共享文档，未执行 parser/writer/scratch copy，未写 index/object-store/memory，未进入 rollout。
6. 下一步：Codex B review Phase 2.99a；通过后才做 selective baseline，不自动进入下一阶段。

## 最新状态

1. Phase 2.97 baseline 已完成：commit `05e7275`，tag `phase-2.97-frontend-gateway-readonly-trial-runbook-baseline`，pushed=true。
2. Phase 2.98 Digital Delivery Standard Agent Boundary Review 已完成 docs-only review，新增 `docs/PHASE298_STANDARD_AGENT_BOUNDARY_REVIEW.md`。
3. Review 已记录共享标准 v0.1 中 `R001-R043` current/backlog/future 规则对 Hermes Agent 回答边界、Missing Evidence 策略和 overclaim 风险的影响。
4. 当前结论：标准 v0.1 可作为 Hermes catalog-only answer boundary basis，但不是 DWG/RVT/BIM 内容理解能力证明。
5. Codex B review 已通过；下一步只做 Phase 2.98 selective docs baseline。
6. Phase 2.98 未改代码、未改数据库、未连接 DB/NAS/API、未运行 Gateway smoke、未修改共享文档、未进入 rollout。
7. 不得自动进入 Phase 2.99；后续如需修改 Hermes prompt / tool description，应同步共享契约文档。

## 最新状态

1. Phase 2.97 Frontend Gateway Read-only Trial Runbook / Operator Checklist 已完成 docs-only planning，Codex B review 已通过。
2. 新增 `docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md`。
3. Runbook 覆盖 limited internal trial、operator checklist、auth path、allowed endpoints、allowed query types、safe response fields、forbidden-field scan、side-effect checks、per-query template、Go/Pause/No-Go、feedback capture 与 escalation rules。
4. Phase 2.97 未运行真实 Gateway smoke，未连接 DB/NAS/API，未实现 Gateway code，未运行 parser/writer，未写 index/object-store，未进入 rollout。
5. 下一步只做 Phase 2.97 selective docs baseline；不得自动进入 Phase 2.98。
6. 仍禁止把 frontend trial Go 误解为 production rollout、Agent DB/NAS 执行授权或内容级 BIM/DWG/RVT 理解授权。

## 最新状态

1. Phase 2.96 baseline 已完成：commit `6fff43f`，tag `phase-2.96-gateway-controlled-smoke-result-review-baseline`，pushed=true。
2. 当前进入 Phase 2.97 Frontend Gateway Read-only Trial Runbook / Operator Checklist。
3. Phase 2.97 只做 docs-only runbook planning，目标是新增 `docs/PHASE297_FRONTEND_GATEWAY_READONLY_TRIAL_RUNBOOK.md`。
4. Runbook 应覆盖 limited internal trial、operator checklist、auth path、allowed endpoints、safe response fields、forbidden-field scan、side-effect checks、Go/Pause/No-Go、feedback capture 与 escalation rules。
5. Phase 2.97 不运行真实 Gateway smoke，不连接 DB/NAS/API，不实现 Gateway code，不运行 parser/writer，不写 index/object-store，不进入 rollout。
6. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md`，完成后停止等待 Codex B review。

## 最新状态

1. Phase 2.96 Gateway Controlled Smoke Result Review 已完成 docs-only / report-review，Codex B review 已通过。
2. 新增 `docs/PHASE296_GATEWAY_CONTROLLED_SMOKE_RESULT_REVIEW.md`，接受最新 Gateway controlled smoke `Go` 作为 read-only controlled smoke 通过证据。
3. 该 Go 基于正常平台 login、project switch、project-scoped bearer token；capabilities / health / chat / catalog search / compatibility / permission-denied / catalog-only content question 均通过。
4. Forbidden-field scan 与 side-effect flags 均保持安全：无 secret/token/password/bearer/credential 真值、NAS path、raw row、SQL、storage path、raw content 泄露；无 DB write、NAS scan/copy、parser、writer、index/object-store write 或 rollout。
5. 该 Go 不授权 production rollout、Agent DB CRUD、Agent SQL、NAS scan/copy、parser/writer/index 写入、DWG/RVT 内容理解、真实 `storage_path` 暴露、repair/migration 或 Agent answer integration。
6. 下一步只做 Phase 2.96 selective docs baseline；不得自动进入 Phase 2.97。
7. Phase 2.97 建议方向：Frontend Gateway Read-only Trial Runbook / Operator Checklist，仍应为 docs-only internal trial runbook，不是生产发布。

## 最新状态

1. Phase 2.95 baseline 已完成：commit `3d70626`，tag `phase-2.95-shared-contract-alignment-baseline`，pushed=true。
2. 当前进入 Phase 2.96 Gateway Controlled Smoke Result Review。
3. 最新 Gateway controlled smoke 已回传 `Go`：正常平台 login、project switch、project-scoped bearer token 后，capabilities / health / chat / catalog search / compatibility / permission-denied / catalog-only content question 均通过。
4. Forbidden-field scan 未发现 secret/token/password/bearer/credential 真值、NAS 路径、`/Volumes`、`nas://`、`smb://`、raw row、SQL、storage path、raw file content；`secretPrinted=false` 为安全状态字段，不计泄露。
5. Side effects 均为 no：DB write、NAS scan/copy、parser、writer、OpenSearch/Qdrant/MinIO write、rollout。
6. Phase 2.96 只做 docs-only result review，不重跑 smoke，不连接 DB/NAS/API，不实现代码。
7. 该 Go 只表示 read-only controlled Gateway smoke 通过，不代表 production rollout 或 Agent DB/NAS 执行授权。

## 最新状态

1. Phase 2.95 Shared Contract Alignment 已完成 docs-only / contract-alignment。
2. 新增 `docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md`，正式记录 Hermes 对共享 `DigitalDeliveryProject` 契约文件的采用、维护责任、sync rules 与当前 mismatch list。
3. 已读取 Phase 2.95 指定的 14 个共享文件；当前 required shared contract 未发现 mismatch。
4. 本轮未修改共享空间文件，未执行真实 smoke，未连接 DB / NAS / API，未实现 Gateway code，未运行 parser/writer，未写 index/object-store，未进入 rollout。
5. 下一步：Codex B review Phase 2.95 alignment；通过后才考虑 selective docs baseline。
6. 不得自动进入 Phase 2.96 或真实 frontend / Gateway smoke。

## 最新状态

1. Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack 已完成 docs-only handoff artifact。
2. 新增 `docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`，用于未来 Codex C / 数据库团队 Codex 在单独授权后执行 read-only controlled smoke。
3. Prompt 覆盖 required placeholders、sanitized inputs、endpoint matrix、safe fields、forbidden-field scan、permission-denied、catalog-only Missing Evidence / `asset_catalog_only`、Go / Pause / No-Go 与 final report template。
4. 本阶段未执行真实 smoke，未连接 DB / NAS / platform API / Hermes API，未实现 Gateway code，未运行 parser/writer，未写 index/object-store，未进入 rollout。
5. 下一步：Codex B review Phase 2.94a handoff prompt；review 通过后才考虑 selective docs baseline。
6. 仍不得自动进入 Phase 2.94b 或真实 frontend / Gateway smoke。

## 最新状态

1. Phase 2.95 Shared Contract Alignment 已完成，Codex B review 通过。
2. 新增 `docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md`，记录 Hermes 对共享 `DigitalDeliveryProject` 契约的采用、维护责任和同步规则。
3. 未发现 required shared contract mismatch，未修改共享空间文件。
4. 实际 Frontend / Gateway controlled smoke 已按正常平台登录流程重跑并回传 `Go`：login / project switch / capabilities / health / chat / catalog search / compatibility / permission-denied / catalog-only content question 均通过，未发现 forbidden-field 泄露或写入副作用。
5. 下一步：先做 Phase 2.95 selective docs baseline；baseline 后进入 Phase 2.96 Gateway controlled smoke result review。
6. 当前仍禁止 production rollout、Agent DB CRUD、Agent SQL、NAS scan、parser、scratch copy、writer、index/object-store write、Agent answer integration；Smoke Go 不等于生产发布许可。

## 最新状态

1. Phase 2.94a baseline 已完成：commit `712cd83`，tag `phase-2.94a-gateway-smoke-handoff-baseline`，pushed=true。
2. 当前进入 Phase 2.95 Shared Contract Alignment。
3. 共享文档空间路径：`/Users/Weishengsu/Library/Mobile Documents/com~apple~CloudDocs/数字化交付平台/DigitalDeliveryProject`。
4. Phase 2.95 目标：创建 `docs/PHASE295_SHARED_CONTRACT_ALIGNMENT.md`，记录 Hermes 与共享契约的对齐、维护责任、同步触发条件和当前红线。
5. 已确认当前共享契约方向：Hermes 为官方名称；`asset_catalog_search` read-only / fail-closed / catalog-only；`project_scope` 必须由 Platform Gateway 服务端生成或校验；路径类字段必须脱敏；catalog metadata 不得作为正文 evidence；DWG/RVT 内容问题必须 Missing Evidence。
6. 本阶段不执行真实 smoke，不连接 DB/NAS/platform API/Hermes API，不实现 Gateway code，不运行 parser/writer，不写 index/object-store，不进入 rollout。
7. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 Phase 2.95 shared contract alignment，然后停止等待 Codex B review。

## 最新状态

1. Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack 已完成，Codex B review 通过。
2. 新增 `docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`，可供 Codex C / 数据库团队 Codex 在后续单独授权时执行只读 controlled smoke。
3. Prompt 已覆盖 endpoint matrix、required placeholders、safe response fields、forbidden-field scan、permission-denied、Missing Evidence / `asset_catalog_only`、Go / Pause / No-Go 与 final report template。
4. 该 handoff prompt 不是 runtime authorization，不允许自动执行真实 Gateway smoke。
5. 下一步：只做 Phase 2.94a selective docs baseline，不自动进入 Phase 2.94b。
6. 当前仍禁止真实 smoke、Agent DB CRUD、Agent SQL、NAS scan、parser、scratch copy、writer、index/object-store write、Agent answer integration、production rollout。

## 最新状态

1. Phase 2.94 baseline 已完成：commit `b41bf9b`，tag `phase-2.94-frontend-gateway-smoke-plan-baseline`，pushed=true。
2. 当前进入 Phase 2.94a Frontend / Gateway Controlled Smoke Handoff Pack。
3. Phase 2.94a 目标：创建 `docs/CODEX_DB_TEAM_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PROMPT.md`，供 Codex C / 数据库团队 Codex 在后续单独授权时执行只读 controlled smoke。
4. 本阶段只做 docs / handoff，不执行真实 smoke，不连接 DB / NAS / platform API / Hermes API，不实现 Gateway code。
5. 交接 prompt 必须覆盖 sanitized inputs、endpoint matrix、safe fields、forbidden-field scan、permission-denied、Missing Evidence / `asset_catalog_only`、Go / Pause / No-Go 与 final report template。
6. 当前仍禁止 Agent DB CRUD、Agent SQL、NAS scan、parser、scratch copy、writer、index/object-store write、Agent answer integration、production rollout。
7. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 Phase 2.94a handoff-pack planning，然后停止等待 Codex B review。

## 最新状态

1. Phase 2.94 Frontend / Gateway Controlled Smoke Planning 已完成 docs-only planning，Codex B review 通过。
2. 新增 `docs/PHASE294_FRONTEND_GATEWAY_CONTROLLED_SMOKE_PLAN.md`。
3. 规划覆盖 capabilities、health、chat、catalog search、compatibility route、permission-denied、catalog-only content question。
4. 规划固定 safe fields：`query_id`、`trace_id`、`file_id`、`model_id`、`source_view`、`permission_decision`、`missingEvidence`、`evidenceMode`、Hermes 命名。
5. 规划固定 forbidden-field negative assertions：storage path / URI variants、NAS URI、raw row、SQL fragment、token、secret、bearer、raw file content、true NAS path。
6. 当前仍未执行真实 smoke，未实现 Gateway code，未连接 DB / NAS / platform API / Hermes API。
7. 下一步：只做 Phase 2.94 selective docs baseline，不自动进入 Phase 2.94a 或真实 smoke。
8. 当前仍禁止真实 Gateway smoke、Agent DB CRUD、Agent SQL、NAS scan、parser、scratch copy、writer、index/object-store write、Agent answer integration、rollout。

## 最新状态

1. Phase 2.93 Read-only Gateway Implementation Review 已完成，Codex B review 通过。
2. 新增 `docs/PHASE293_READONLY_GATEWAY_IMPLEMENTATION_REVIEW.md`；结论为 report-level `go` / `read_only_gateway_review_passed`。
3. 该 Go 不代表 production readiness，不授权 Agent DB CRUD、Agent SQL、NAS scan、content ingestion、writer/parser/index writes、Agent answer integration 或 rollout。
4. P1 follow-up：sanitized response schema samples、trace identifiers、safe catalog identifiers、permission-denied copy。
5. 下一步只做 Phase 2.93 selective docs baseline；baseline 后再规划 Phase 2.94 frontend controlled smoke planning。

## 最新状态

1. Phase 2.93 Read-only Gateway Implementation Review 已完成 docs-only review。
2. 新增 `docs/PHASE293_READONLY_GATEWAY_IMPLEMENTATION_REVIEW.md`，结论为 report-level `go`：数据库团队回传报告满足 Phase 2.92 P0 gates。
3. 该 `go` 只表示 `read_only_gateway_review_passed`，不是 production readiness，不授权 Gateway implementation、Agent DB CRUD、NAS scan、content ingestion 或 rollout。
4. P1 follow-up：response schema sample、`query_id` / `trace_id`、`file_id` / `model_id` / `source_view`、permission-denied safe copy 仍需 Phase 2.94 planning。
5. 当前仍禁止在 Hermes 仓库实现 Gateway code、连接真实 DB、运行平台 Gateway smoke、执行 Agent DB CRUD、NAS scan、parser、scratch copy、writer、index/object-store write 或 rollout。
6. 下一步：Codex B review Phase 2.93 文档；若通过，进入 Phase 2.94 frontend controlled smoke planning，默认仍不执行真实 smoke。

## 最新状态

1. Phase 2.91 baseline 已完成：commit `cf89e1e`，tag `phase-2.91-runtime-evidence-writer-smoke-gate-baseline`，pushed=true。
2. 当前进入 Phase 2.92 Read-only Gateway Acceptance Planning。
3. 新增 `docs/PHASE292_READONLY_GATEWAY_ACCEPTANCE_PLAN.md`，把数据库团队 read-only frontend Gateway access review 收束为 Hermes 主线验收 gates。
4. Phase 2.92 允许数据库团队继续平台后端 Gateway / 前端 Hermes 面板 / read-only catalog metadata preview / server-side permission proof；不允许 Agent DB CRUD、Agent-generated SQL、NAS scan、DWG/RVT 内容理解或 production rollout。
5. P0 gates：命名必须为 Hermes；前端不得直连 raw Hermes；`project_scope` 必须 server-side 生成；不得返回真实 `storage_path` / raw row / NAS path / raw content；无权限默认 `DENIED`。
6. 数据库团队已回传初步实现报告：Hermes 命名收束、Gateway endpoints、forbidden-field assertions、Missing Evidence / `asset_catalog_only` 口径、前后端构建与专项脚本均通过；Hermes 侧暂定 provisionally go。
7. 本阶段未实现 Gateway code，未运行 DB / API / CLI / Mac mini smoke，未写 DB/index/object-store，未运行 parser/scratch/writer。
8. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 selective docs baseline，然后停止；随后进入 Phase 2.93 review 数据库团队 Gateway implementation report。

## 最新状态

1. Phase 2.91 Runtime Evidence Writer Smoke Gate Implementation 已完成本地实现，并已通过 Codex B review。
2. 新增 smoke gate service / CLI / tests / docs；默认 gate-only 返回 `writer_smoke_ready_for_operator_stop`，不调用 writer。
3. 仅在目标测试 / temp SQLite / injected DB session 中允许 `EvidenceOnlyWriter.write()`，用于验证 `writer_smoke_executed`、created counts、idempotency duplicate 与 rollback dry-run。
4. 验证通过：TDD RED 已观察；目标测试 `12 passed`；py_compile 通过；writer + preflight + smoke 组合回归 `29 passed`。
5. 真实 developer DB / Mac mini DB writer invocation 仍未授权；真实 test-machine writer smoke 需要后续单独 prompt、operator approval 与 Codex B review。
6. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 selective Git baseline。不得自动进入真实 writer smoke 或 Phase 2.92。
7. 当前仍禁止 parser、scratch copy、NAS scan、OpenSearch/Qdrant/MinIO 写入、platform DB 写入、Agent answer integration、repair/reindex/rollout。

## 最新状态

1. Phase 2.90 test-machine update gate 已返回 `Go`：测试机 `/Users/hermes/code/Hermes_memory` 已 clean checkout 到 `4e0bd62` / `phase-2.89-test-machine-runtime-preflight-handoff-baseline`。
2. Phase 2.89 runtime preflight-only 已在测试机返回 `Go`：decision state `preflight_ready_for_operator_stop`。
3. Preflight 输出文件名为 `phase289-runtime-preflight-report-001.json`，prerequisite refs present/sanitized，worktree clean，expected commit matched。
4. 安全结果：writer 未调用、DB 未写入、parser 未运行、scratch copy 未发生、NAS 未扫描、OpenSearch/Qdrant/MinIO 未写入、Agent answer 未接入、未 rollout。
5. 当前建议先做 Phase 2.90 selective docs baseline，随后再规划 Phase 2.91 first controlled writer smoke execution gate。
6. `preflight_ready_for_operator_stop` 仍不是写入授权；真实 writer invocation 必须单独授权。

## 最新状态

1. Phase 2.89 baseline 已完成：commit `4e0bd62`，tag `phase-2.89-test-machine-runtime-preflight-handoff-baseline`，pushed=true。
2. 当前进入 Phase 2.90 Test-Machine Repository Update Gate。
3. 在测试机执行 Phase 2.89 preflight 前，必须先把测试机 Hermes Memory checkout 更新到 `phase-2.89-test-machine-runtime-preflight-handoff-baseline`。
4. 新增 `docs/CODEX_TEST_MACHINE_UPDATE_TO_PHASE289_PROMPT.md`，只允许 clean worktree 下 fetch tags / checkout exact tag / verify docs。
5. Phase 2.90 不运行 preflight runner，不调用 writer，不写 DB，不运行 parser，不复制/扫描 NAS，不写 index/object-store，不接 Agent answer。
6. 下一步：先用该 prompt 更新测试机仓库；成功后才能单独授权运行 `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md`。

## 最新状态

1. Phase 2.88 baseline 已完成：commit `b09c3d1`，tag `phase-2.88-runtime-evidence-write-preflight-baseline`，pushed=true。
2. Phase 2.89 Test-Machine Runtime Preflight Smoke Handoff 已完成 docs-only 交接包，Codex B review 通过。
3. 新增 `docs/PHASE289_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PLAN.md` 与 `docs/CODEX_TEST_MACHINE_RUNTIME_PREFLIGHT_SMOKE_PROMPT.md`。
4. 交接包让 Mac mini / 测试机只验证 operator approval、sanitized prerequisite report refs、git/worktree 状态和 ignored output report，并在 `preflight_ready_for_operator_stop` 停止。
5. Phase 2.89 未执行 preflight runner，未调用 `EvidenceOnlyWriter.write()`，未写真实 DB，未运行 parser，未复制/扫描 NAS，未写 OpenSearch / Qdrant / MinIO，未接 Agent answer。
6. 下一步：只做 Phase 2.89 selective docs baseline，不自动执行测试机 prompt。
7. 真实 runtime evidence write smoke、writer invocation、index/object-store 写入和 Agent answer integration 仍需后续单独授权。

## 最新状态

1. Phase 2.87d baseline 已完成：commit `3b01b0f`，tag `phase-2.87d-runtime-evidence-write-execution-pack-baseline`，pushed=true。
2. Phase 2.88 Runtime Evidence Write Preflight Runner 已完成首轮实现，等待 Codex B review。
3. 新增 `app/services/asset_catalog/evidence_write_runtime_preflight.py` 与 `scripts/phase288_runtime_evidence_write_preflight.py`，用于本地 preflight-only validation。
4. Preflight runner 校验 operator approval、report refs、feature flags、scope limits、idempotency、payload fingerprint、git commit 与 worktree status，并返回 `preflight_ready_for_operator_stop` / `preflight_pause` / `preflight_no_go`。
5. 验证通过：target tests `10 passed`，py_compile 通过，Data Steward regression `143 passed`，temp fixture CLI smoke 返回 `preflight_ready_for_operator_stop`。
6. `preflight_ready_for_operator_stop` 只表示必须停在 operator stop point，不授权 writer invocation。
7. 当前仍禁止调用 `EvidenceOnlyWriter.write()`、真实 DB 写入、parser、真实文件复制、raw content 读取、NAS scan、OpenSearch / Qdrant / MinIO 写入、platform DB 写入、Agent answer integration、Agent DB / NAS CRUD、repair/reindex/rollout。
8. Codex B review 已通过；下一步只做 Phase 2.88 selective Git baseline。不得自动进入 Phase 2.89 或真实 smoke。

## 最新状态

1. Phase 2.87c baseline 已完成：commit `490b5ca`，tag `phase-2.87c-runtime-evidence-write-smoke-plan-baseline`，pushed=true。
2. 当前进入 Phase 2.87d Runtime Evidence Write Smoke Execution Pack Planning。
3. Phase 2.87d 只创建未来 Mac mini / 测试机 runtime evidence write smoke 的执行交接包和 Codex C/test-machine prompt。
4. 本阶段仍不执行 writer，不写真实 DB，不接 API / CLI runtime，不运行 parser，不复制文件，不写 index/object-store，不接 Agent answer。
5. 规划重点：测试机前置条件、reviewed refs、env key names、operator approval JSON、prior report refs、feature flags、one-run write boundary、preflight-only commands、stop points、sanitized report、rollback/idempotency checks 与 Go / Pause / No-Go。
6. Codex B review 已通过；下一步只做 Phase 2.87d selective docs baseline。不得执行测试机 prompt，不得自动进入 Phase 2.88 或真实 smoke。

## 最新状态

1. Phase 2.87b Evidence-only Writer Service Implementation 已完成首轮实现，等待 Codex B review。
2. 新增 `app/services/asset_catalog/evidence_writer.py`，提供 `EvidenceOnlyWriter`、`EvidenceWriteDecision`、`EvidenceWriteRollbackPlan` 与 `build_evidence_write_result()`。
3. Writer 只允许通过注入 SQLAlchemy session 在 test-local DB 中创建 `Document`、`DocumentVersion`、`Chunk`、`CitationRecord`。
4. 已实现 fail-closed gates、1 document / 1 version / <=20 chunks 限制、forbidden raw-field 拒绝、idempotency duplicate / conflict 判定与 run-scoped rollback dry-run。
5. 验证通过：TDD RED 已观察；目标测试 `7 passed`；py_compile 通过；Data Steward regression `133 passed`。
6. 当前仍禁止真实 DB write、API / CLI runtime wiring、parser、真实文件复制、NAS scan、OpenSearch / Qdrant / MinIO 写入、audit table write、Agent answer integration、repair/reindex/rollout。
7. Codex B review 已通过；下一步只做 Phase 2.87b selective baseline。不得自动进入 Phase 2.87c 或真实 evidence write smoke。

## 最新状态

1. Phase 2.87a Exact Write Target Discovery 已完成 docs-only / read-only discovery。
2. 新增 `docs/PHASE287A_EXACT_WRITE_TARGET_DISCOVERY.md`，识别候选 evidence tables：`documents`、`document_versions`、`chunks`、`citations`，可选 bookkeeping `ingestion_jobs`。
3. 发现关键阻塞：现有 `DocumentIngestionService.ingest_uploaded_file()` 读取 file bytes、调用 parser/chunker、写 OpenSearch/Qdrant，不适合作为 first real evidence-only smoke 入口。
4. 当前 direct real write 仍为 `Pause`；Phase 2.87b 如后续授权，应先规划/实现 dedicated evidence-only writer service、idempotency metadata 与 run-scoped rollback dry-run。
5. 当前仍禁止 writer implementation、真实 `documents/chunks/document_versions` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. Phase 2.87a discovery 已完成，Codex B review 已通过；下一步只做 selective docs baseline。
7. 不得自动进入 Phase 2.87b；真实 evidence write 仍需 dedicated writer / idempotency / rollback 设计与单独 prompt。

## 最新状态

1. Phase 2.87 First Real Hermes Evidence Write Smoke Planning 已完成 docs-only 规划。
2. 新增 `docs/PHASE287_FIRST_REAL_EVIDENCE_WRITE_SMOKE_PLAN.md`，定义未来 Mac mini / 测试机第一次真实 Hermes evidence write smoke 的安全门槛。
3. 规划固定 tiny scope：最多 1 source asset、1 document version、20 chunks；Phase 2.87a 必须另行 explicit operator approval。
4. 规划包括 prerequisite chain、operator approval JSON、feature flags default off、exact write target gate、rollback boundary、sanitized report boundary、Go / Pause / No-Go 与 DB platform handoff。
5. 当前仍禁止 writer implementation、真实 `documents/chunks/document_versions` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. Phase 2.87 planning 已完成，Codex B review 已通过；下一步只做 selective docs baseline。
7. 不得自动进入 Phase 2.87a；真实 evidence write 仍需单独 prompt 与 operator approval JSON。

## 最新状态

1. Phase 2.86a baseline 已完成：commit `c5372fc`，tag `phase-2.86a-evidence-write-rehearsal-baseline`，pushed=true。
2. 当前进入 Phase 2.87 First Real Hermes Evidence Write Smoke Planning。
3. Phase 2.87 只规划未来 Mac mini / 测试机第一次真实 Hermes evidence write smoke，不实现 writer，不执行真实写入。
4. 规划重点：1 asset / 1 document version / 20 chunks tiny scope、operator approval JSON、feature flags default off、exact write targets、rollback boundary、sanitized report 与 Go / Pause / No-Go。
5. 当前仍禁止真实 `documents/chunks/document_versions` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. Phase 2.87 planning 已完成，Codex B review 已通过；下一步只做 selective docs baseline。
7. 不得自动进入 Phase 2.87a；真实 evidence write 仍需单独 prompt 与 operator approval JSON。

## 最新状态

1. Phase 2.86a Temp Evidence Write Rehearsal implementation 已完成目标验证。
2. 新增 rehearsal service / CLI / tests / ignored report directory / docs，从 ignored local `nas_evidence_write_dry_run.v0` 生成 ignored local `nas_evidence_write_rehearsal.v0`。
3. Rehearsal 仅使用 in-memory / temp SQLite repository，验证 temp-only document / version / chunk / citation insert ordering、idempotency、rollback dry-run 与 sanitized report。
4. Target tests `7 passed`，Data Steward regression `126 passed`，py_compile 与 CLI temp smoke 通过。
5. `rehearsal_go` 仍不授权真实写入，不代表 production evidence，不代表 Hermes 可回答 NAS 正文。
6. 当前仍禁止真实 `documents/chunks/document_versions` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
7. Codex B review 已通过；下一步只做 selective Git baseline。不要自动进入 Phase 2.87。

## 最新状态

1. Phase 2.86 baseline 已完成：commit `8455d4a`，tag `phase-2.86-controlled-real-evidence-write-plan-baseline`，pushed=true。
2. 当前进入 Phase 2.86a Temp Evidence Write Rehearsal Implementation。
3. 目标是从 ignored local `nas_evidence_write_dry_run.v0` report 生成 ignored local `nas_evidence_write_rehearsal.v0` report。
4. Rehearsal 只允许 temp SQLite / in-memory repository，验证 document / version / chunk / citation 写入顺序、idempotency、rollback dry-run 和 sanitized report。
5. 当前仍禁止真实 `documents/chunks` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 2.86a implementation，完成后交 Codex B review。

## 最新状态

1. Phase 2.86 Controlled Small-batch Real Hermes Evidence Write Planning 已完成 docs-only plan。
2. 新增 `docs/PHASE286_CONTROLLED_REAL_EVIDENCE_WRITE_PLAN.md`。
3. 规划边界：future first real write smoke 只能 test-machine-only，建议最多 1 source asset、1 document version、20 chunks。
4. 规划内容：permission proof、operator approval、feature flags default off、write target boundary、citation metadata、idempotency、locks、rollback dry-run、Go / Pause / No-Go、follow-up phase split。
5. 当前仍未授权 writer implementation、真实 `documents/chunks` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. Codex B review 已通过；下一步只做 Phase 2.86 docs baseline。不要自动进入 Phase 2.86a 或 Phase 2.87。

## 最新状态

1. Phase 2.85a baseline 已完成：commit `380e7a0`，tag `phase-2.85a-evidence-write-dry-run-baseline`，pushed=true。
2. 当前进入 Phase 2.86 Controlled Small-batch Real Hermes Evidence Write Planning。
3. Phase 2.86 只规划 future test-machine controlled real evidence write smoke，不实现 writer、不执行真实写入。
4. 规划重点：权限证明、operator approval、feature flags default off、deterministic refs、idempotency、locks、rollback dry-run、citation metadata、Go / Pause / No-Go。
5. 当前仍禁止真实 `documents/chunks` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. 下一步：Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 完成 docs-only planning，完成后交 Codex B review。

## 最新状态

1. Phase 2.85a Local Evidence Write Dry-run Runner implementation 已完成目标实现。
2. 新增 `evidence_write_dry_run` service 与 CLI：从 ignored local `nas_evidence_write_preflight.v0` report 生成 ignored local `nas_evidence_write_dry_run.v0` report。
3. Runner 仅使用 in-memory simulation，生成 deterministic simulated document/chunk/citation refs，并覆盖 idempotency duplicate detection 与 same-run rollback dry-run。
4. `write_dry_run_go` 仍不授权真实写入，不代表 document evidence，不代表 Hermes 可回答 NAS 正文。
5. 当前仍禁止真实 `documents/chunks` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
6. 下一步：完成 full validation 后 Codex B review；通过后只做 selective Git baseline。不要自动进入 Phase 2.86。

## 最新状态

1. Phase 2.85 Controlled Evidence Write Dry-run Planning 已完成。
2. 新增 `docs/PHASE285_CONTROLLED_EVIDENCE_WRITE_DRY_RUN_PLAN.md`。
3. 规划边界：future evidence write dry-run 只能使用 local temp SQLite / in-memory repository，不写真实 Hermes DB、platform DB、OpenSearch、Qdrant 或 MinIO。
4. 规划内容：ignored local `nas_evidence_write_preflight.v0` 输入、`write_preflight_ready_for_dry_run` gate、operator approval、feature flags default off、deterministic simulated document/chunk refs、idempotency、rollback dry-run、citation boundary 与 Go / Pause / No-Go。
5. 当前仍禁止 writer implementation、dry-run execution、parser、真实文件复制、raw content 读取、NAS scan、`documents/chunks` 写入、Agent answer integration、repair/reindex/rollout。
6. 下一步只建议 Codex B review；通过后做 docs-only baseline。不要自动进入 Phase 2.85a。

## 最新状态

1. Phase 2.84a baseline 已完成：commit `a006df3`，tag `phase-2.84a-evidence-write-preflight-dry-run-baseline`。
2. 当前进入 Phase 2.85 Controlled Evidence Write Dry-run Planning。
3. Phase 2.85 只规划 future controlled evidence write dry-run，不实现 writer，不执行 dry-run。
4. 规划重点：local temp SQLite / in-memory simulated write、deterministic refs、idempotency、rollback dry-run、citation coverage、feature flags default off、Go / Pause / No-Go。
5. 下一步候选：Phase 2.85a local temp DB / in-memory evidence write dry-run runner；Phase 2.86 以后才考虑 controlled small-batch real Hermes evidence write planning。
6. 当前仍禁止真实 `documents/chunks` 写入、DB/index/object-store 写入、parser、真实文件复制、NAS scan、Agent answer integration、repair/reindex/rollout。
7. 下一步 Codex A 只做 docs-only planning，完成后停止。

## 最新状态

1. Phase 2.84 baseline 已完成：commit `c554488`，tag `phase-2.84-evidence-write-preflight-plan-baseline`。
2. 当前进入 Phase 2.84a Evidence Write Preflight Dry-run Implementation。
3. 新增 `evidence_preflight` service 与 CLI：从 ignored local payload plan + operator approval JSON 生成 ignored local preflight report。
4. Preflight states：`write_preflight_not_allowed`、`write_preflight_ready_for_dry_run`、`write_preflight_no_go`。
5. `write_preflight_ready_for_dry_run` 仍不授权任何写入、索引、parser、copy 或 Agent answer；preflight report 仍不是 document evidence。
6. 当前仍禁止 parser、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
7. 下一步只允许 selective Git baseline，baseline 后停止。

## 最新状态

1. Phase 2.83a baseline 已完成：commit `4b3a9fb`，tag `phase-2.83a-evidence-payload-dry-run-baseline`。
2. 当前进入 Phase 2.84 Controlled Evidence Write Preflight Planning。
3. 新增 `docs/PHASE284_CONTROLLED_EVIDENCE_WRITE_PREFLIGHT_PLAN.md`。
4. 规划边界：preflight contract 是 planning-only，不是 write authorization；不得执行 preflight runner，不得写 `documents/chunks`。
5. 规划内容：operator approval、write scope、idempotency、rollback、citation coverage、locks、decision states 与 future Phase 2.84a gates。
6. 当前仍禁止 parser、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
7. 下一步只允许 selective docs baseline，baseline 后停止。

## 最新状态

1. Phase 2.83 baseline 已完成：commit `d3cedc9`，tag `phase-2.83-evidence-payload-contract-plan-baseline`。
2. 当前进入 Phase 2.83a Evidence Write Payload Dry-run Implementation。
3. 新增 `evidence_payload` service 与 CLI：从 ignored local eligibility report 生成 ignored payload plan。
4. Payload states：`payload_not_allowed`、`payload_ready_for_human_review`、`payload_ready_for_write_dry_run`、`payload_no_go`。
5. `payload_ready_for_write_dry_run` 仍不授权任何写入、索引或 Agent answer；payload plan 仍不是 document evidence。
6. 当前仍禁止 parser、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
7. 下一步只允许 selective Git baseline，baseline 后停止。

## 最新状态

1. Phase 2.82a baseline 已完成：commit `1838e3a`，tag `phase-2.82a-evidence-eligibility-dry-run-baseline`。
2. 当前进入 Phase 2.83 Evidence Write Payload Contract Planning。
3. 新增 `docs/PHASE283_EVIDENCE_WRITE_PAYLOAD_CONTRACT_PLAN.md`。
4. 规划边界：payload contract 是 planning-only，不是 document evidence；不得生成 payload artifact，不得写 `documents/chunks`。
5. 当前仍禁止 parser、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
6. Codex B review 已通过；下一步只允许 selective docs baseline，baseline 后停止。

## 最新状态

1. Phase 2.82 baseline 已完成：commit `931e6e1`，tag `phase-2.82-evidence-write-eligibility-plan-baseline`。
2. 当前进入 Phase 2.82a Evidence Write Eligibility Dry-run Implementation。
3. 新增 `evidence_eligibility` service 与 CLI：从 ignored local sanitized manifest 生成 ignored eligibility report。
4. Eligibility states：`not_eligible`、`eligible_for_human_review`、`eligible_for_evidence_write_planning`、`no_go`。
5. `eligible_for_evidence_write_planning` 仍不授权任何写入、索引或 Agent answer；缺少权限证明默认 `DENIED`。
6. 当前仍禁止 parser、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
7. 下一步只允许 selective Git baseline，baseline 后停止。

## 最新状态

1. Phase 2.81a baseline 已完成：commit `985a622`，tag `phase-2.81a-sanitized-evidence-manifest-dry-run-baseline`。
2. 当前进入 Phase 2.82 Evidence Write Eligibility Planning。
3. 新增 `docs/PHASE282_EVIDENCE_WRITE_ELIGIBILITY_PLAN.md`。
4. 规划边界：manifest 是 review-only，不是 document evidence；`approved` 不等于写入、索引或可回答。
5. 当前仍禁止 parser、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
6. Codex B review 已通过；下一步只允许 selective docs baseline，baseline 后停止。

## 最新状态

1. Phase 2.81 baseline 已完成：commit `804d069`，tag `phase-2.81-sanitized-evidence-manifest-plan-baseline`。
2. 当前进入 Phase 2.81a Sanitized Evidence Manifest Dry-run Implementation。
3. 新增 manifest builder / CLI：只从 sanitized parser preview metadata 生成 ignored local manifest。
4. Manifest 不包含 raw text、真实文件名、真实 NAS 路径、raw DB row、secret 或敏感业务数据。
5. 当前仍禁止 parser 执行、真实文件复制、DB / `documents/chunks` / OpenSearch / Qdrant / MinIO 写入、Agent answer integration 与 rollout。
6. Codex B review 已通过；下一步只允许 selective Git baseline，baseline 后停止。

## 最新状态

1. Phase 2.80a Mac mini / 测试机 controlled scratch parser dry-run 已返回 `Go`。
2. 验证结果：3 个小型非敏感样本完成 copy、parser dry-run preview 与 cleanup，`cleanup_status=all_deleted`。
3. 安全结果：未输出 raw text / secret / raw row / 真实文件名 / 真实 NAS 路径 / 敏感业务数据；未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO；未接入 Agent final answer；未 rollout。
4. 当前能力边界：Hermes 只证明了“权限证明 + 小批 scratch copy + parser dry-run preview + cleanup”，还不能基于 NAS 正文回答。
5. 当前进入 Phase 2.81 Sanitized Evidence Manifest Planning。
6. Phase 2.81 只规划 manifest；不得生成真实 manifest artifact，不得写 DB / index / object store，不得接入 Agent final answer。
7. Codex B review 已通过；下一步只允许 selective docs baseline，baseline 后停止。

## 最新状态

1. Phase 2.80 Controlled Scratch Parser Dry-run Planning 已完成。
2. 新增 `docs/PHASE280_CONTROLLED_SCRATCH_PARSER_DRY_RUN_PLAN.md`。
3. Phase 2.80a 只能在 Phase 2.79a 权限证明、1-3 小样本、scratch copy、hash、cleanup 边界内运行 parser dry-run。
4. Parser 输出只能生成 local sanitized preview / manifest，不得写 `documents`、`chunks`、OpenSearch、Qdrant、MinIO、platform DB 或 Hermes DB。
5. 本轮未执行 parser、未复制真实文件、未读取真实正文、未写 DB/index/object-store、未进入 Agent final answer 或 rollout。
6. Codex B review 已通过；下一步只做 Phase 2.80 docs baseline。Phase 2.80a parser dry-run implementation 必须单独授权。

## 最新状态

1. Phase 2.79a Mac mini / 测试机 small batch NAS scratch-copy smoke 已返回 `Go`。
2. 验证结果：3 个小型非敏感样本均完成 copy、sha256 与 cleanup，`cleanup_status=all_deleted`。
3. 安全结果：未输出 secret / raw row / 真实 NAS 路径 / 敏感业务数据；未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO；未调用 parser；未进入 Agent final answer integration 或 rollout。
4. 当前能力边界：Hermes 只证明了“权限证明 + 小批 scratch copy + hash + cleanup”，还不能基于 NAS 正文回答。
5. 当前进入 Phase 2.80 Controlled Scratch Parser Dry-run Planning。
6. Phase 2.80 只规划 parser dry-run；不得执行 parser，不得读取真实正文，不得写 DB / index / object store。

## 最新状态

1. Phase 2.78 Controlled Local Scratch Runtime 已完成本地 fixture runtime 首轮实现。
2. 新增 `AssetScratchRuntime`，支持 explicit authorization + feature flags 双门槛；只处理 `would_copy` item；只允许 local path / `file://` fixture；执行 copy -> sha256 -> sanitized run record -> cleanup。
3. 当前仍不连接真实 NAS，不复制真实企业文件，不调用 parser，不写 DB / `documents` / `chunks` / OpenSearch / Qdrant / MinIO，不启用 runtime flags 默认值。
4. 验证通过：py_compile 通过，scratch copy plan + runtime 目标测试 `10 passed`，Data Steward asset catalog regression `87 passed`，`git diff --check` 通过，latest JSON 校验通过。
5. 下一步需要 Codex B review；通过后再写 selective baseline prompt。
6. Phase 2.79 才能规划 Mac mini / 测试机显式授权下的 1-3 个小型非敏感样本真实 smoke。

## 最新状态

1. Phase 2.79 Small Batch Real Smoke Planning 已完成。
2. 新增 `docs/PHASE279_SMALL_BATCH_REAL_SMOKE_PLAN.md`，明确 Phase 2.79a 的前置条件、样本选择、允许动作、禁止动作、stop conditions、sanitized report 与 Go / Pause / No-Go。
3. 新增 `docs/CODEX_MAC_MINI_SMALL_BATCH_NAS_SMOKE_PROMPT.md`，作为后续显式授权后给 Mac mini / 测试机的执行 prompt。
4. 本轮未执行真实 NAS copy、未读取真实企业文件、未调用 parser、未写 DB / `documents/chunks` / OpenSearch / Qdrant / MinIO。
5. 下一步必须先 Codex B review；通过后再决定 Phase 2.79 docs baseline 或另开 Phase 2.79a small batch real smoke。
6. Phase 2.79a 仍必须单独授权；不得由 planning 文档自动触发。

## 最新状态

1. Phase 2.78 baseline 已完成：commit `5da558e`，tag `phase-2.78-local-scratch-runtime-baseline`。
2. 当前进入 Phase 2.79 Small Batch Real Smoke Planning。
3. 已写入 `docs/NEXT_CODEX_A_PROMPT.md`，要求只规划 Mac mini / 测试机 1-3 个小型非敏感样本真实 smoke，不执行真实 copy。
4. Phase 2.79 planning 必须定义权限证明、样本大小、文件类型白名单、stop conditions、sanitized report 与 No-Go 条件。
5. 真实 NAS copy、parser、DB / `documents/chunks` / OpenSearch / Qdrant 写入、Agent CRUD、rollout 仍禁止。
6. 数据库团队二期可以继续围绕 REST/API Key `project_scope`、权限证明、资产目录 UI 与 Agent 查询入口推进；真实正文联调等 Phase 2.79a 授权。

## 最新状态

1. Phase 2.76 / 2.77 baseline 已完成：commit `8aa94f3`，tag `phase-2.76-2.77-nas-scratch-copy-dry-run-baseline`。
2. 当前进入 Phase 2.78 Controlled Local Scratch Runtime。
3. 已写入 `docs/NEXT_CODEX_A_PROMPT.md`，要求 Codex A 实现本地 fixture runtime：copy -> sha256 -> sanitized run record -> cleanup。
4. Phase 2.78 仍不连接真实 NAS，不解析真实企业文件，不写 DB / `documents/chunks` / OpenSearch / Qdrant，不启用默认 runtime flags。
5. 数据库团队二期前半段可以继续推进：REST/API Key `project_scope`、权限证明、资产目录 UI、Agent 查询入口和 v1.1 DTO 不再被 Hermes 阻塞。
6. Phase 2.79 才进入 Mac mini 显式授权的 1-3 个小型样本真实 smoke。

## 最新状态

1. Phase 2.76 / 2.77 进入 NAS Scratch Copy Pipeline dry-run 主线实现。
2. 新能力边界：Hermes 只生成“按项目小批量、权限前置、临时 scratch copy”的 dry-run plan，不连接真实 NAS、不复制、不解析、不删除任何真实文件。
3. 新增 `AssetScratchCopyPlanner`、`AssetScratchCopyPlanRequest`、`AssetScratchCopyPlanItem`、`AssetScratchCopyPlanSummary`，默认 feature flags 仍关闭：`PLATFORM_ASSET_SCRATCH_COPY_ENABLED=false`、`PLATFORM_ASSET_BATCH_COPY_ENABLED=false`。
4. 默认限制：最多 10 个文件，总大小不超过 2GB，单文件不超过 512MB；Office / PDF / text 小文件可进入 `would_copy`，RVT / DWG / IFC / NWD 等 BIM 大模型仍为 metadata-only / requires review。
5. 当前仍禁止真实 DB 写入、NAS scan / copy、scratch runtime、文档正文写入 `documents/chunks`、OpenSearch / Qdrant 写入、Agent CRUD、repair、reindex、rollout。
6. 下一步 Codex B review；通过后再做 selective baseline。Phase 2.78 真实 scratch runtime 必须另获 Mac mini / 测试机显式授权。

## 最新状态

1. Phase 2.75 进入 Data Steward catalog query preview 主线实现。
2. 当前结论：Phase 2.74 已完成真实 DB v1.1 结构 / 脱敏统计 / Hermes adapter contract 级耦合，但不是完整 Data Steward runtime 耦合。
3. 新增 preview 层目标：只返回资产目录元数据，不生成 prompt evidence；正文回答请求返回 `asset_catalog_only` Missing Evidence。
4. Phase 2.75 本地验证通过：py_compile 通过，Data Steward 目标 pytest `77 passed`，`git diff --check` 通过。
5. 当前仍禁止 runtime enable、mirror、selective indexing、NAS scan、DB CRUD、Agent 直接改 MySQL / NAS、production rollout。
6. 下一步 Codex B review；之后再规划 REST/API Key `project_scope` 权限证明。

## 最新状态

1. Phase 2.74 已准备测试机 reviewed-ref 复验 prompt。
2. 新增 `docs/PHASE274_TEST_MACHINE_V11_ADAPTER_SMOKE_PLAN.md` 与 `docs/CODEX_TEST_MACHINE_V11_ADAPTER_SMOKE_PROMPT.md`。
3. 复验目标：确认包含 Phase 2.73 的 Hermes ref 在测试机仍满足 v1.1 structure-only / redacted stats / fail-closed。
4. 下一步由用户交给测试机 Codex 执行；本仓库不直接连接真实 DB。
5. 历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty 仍与当前阶段无关，baseline 必须排除。

## 最新状态

1. Phase 2.72a 已准备 `LIMIT 30` 脱敏统计 smoke prompt：`docs/CODEX_DB_LIMIT30_REDACTED_SMOKE_PROMPT.md`。
2. 该 prompt 只允许最多 30 行的聚合统计输出，不允许 raw row、真实业务标识、ID 原值、`permission_tags` 原值、secret 或任何写操作。
3. 本仓库未执行 `LIMIT 30`，未读取真实行，未写 DB / index。
4. 下一步由用户决定是否把 prompt 交给测试机 Codex 执行；若返回 Go，再规划 Hermes v1.1 readonly adapter contract update。

## 最新状态

1. 测试机 v1.1 structure-only smoke 已返回 `Go`：DB 可达、database 匹配、四个 View 存在、v1.1 字段均存在、四个 `WHERE 1 = 0` 通过。
2. 已新增 `docs/PHASE272_DB_V11_STRUCTURE_SMOKE_RESULT.md`，固化 v1.1 structure-only smoke 结果。
3. 当前结论：Hermes 与真实 DB 已完成 v1.1 结构级只读耦合；完整 Data Steward 耦合仍未完成。
4. 下一步候选：`LIMIT 30` 脱敏统计 smoke planning，或 Hermes 侧 v1.1 readonly adapter contract update。
5. 当前仍不授权 `LIMIT 30` 执行、真实行读取、mirror migration、DB CRUD、NAS scan、selective indexing 或 production rollout。

## 最新状态

1. 数据库团队已返回 `DB Schema Gap Sanitized Response`，未连接数据库、未读取真实行、未输出 secret / 真实业务数据。
2. 当前进入 Phase 2.71 DB v1.1 Contract Alignment。
3. 已新增 `docs/DB_SCHEMA_GAP_SANITIZED_RESPONSE.md`，固化数据库团队脱敏回复。
4. 已新增 `docs/PHASE271_DB_V11_CONTRACT_ALIGNMENT_PLAN.md`，明确 `delivery_platform.asset_views.v1.1` 字段范围、Hermes fail-closed 策略与后续 smoke 顺序。
5. 已新增并按数据库团队第 6 节回复更新 `docs/CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md` 与 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`，用于加速数据库团队字段确认和测试机 v1.1 structure-only 复验。
6. v1.1 候选字段：`ModelAssetView.project_id`、粗粒度 `permission_tags`、`confidentiality_level`、`last_seen_at`、`lifecycle_status`、`index_eligibility`、`AuditEventView.event_id` checkpoint 语义。
7. 当前仍不授权 `LIMIT 30`、真实样本读取、mirror migration、DB CRUD、NAS scan、selective indexing 或 production rollout。
8. 下一步建议把 `docs/CODEX_DB_V11_FIELD_CONFIRMATION_PROMPT.md` 交给数据库团队；v1.1 落地后再把 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md` 交给测试机 Codex。
9. 数据库团队已回传 v1.1 脱敏部署报告：`V17__asset_views_v1_1.sql` 已应用到目标 DB，后端测试实例健康检查 `UP`，测试机 contract version key 已安全更新。
10. 已更新 `docs/DB_V11_DEPLOYMENT_BLOCKER_STATUS.md`，当前状态改为 Go for Hermes structure-only smoke。
11. 下一步让测试机 Codex 执行 `docs/CODEX_DB_V11_STRUCTURE_ONLY_SMOKE_PROMPT.md`；仍不授权 `LIMIT 30`、真实行读取、mirror、indexing 或 Agent CRUD。

## 最新状态

1. 测试机 DB `structure_only` smoke 已返回 `Go`：DB 可达、database 匹配、四个 View 存在、字段结构可读、四个 `WHERE 1 = 0` 通过。
2. 当前进入 Phase 2.70 DB Schema Contract Gap Review。
3. 已新增 `docs/PHASE270_DB_SCHEMA_CONTRACT_GAP_REVIEW.md`，基于真实 View 字段结构梳理 P0 / P1 / P2。
4. 已新增 `docs/DB_SCHEMA_GAP_REQUEST_TO_DB_TEAM.md`，用于发给数据库团队确认 P1 字段补齐方向。
5. 已新增 `docs/DB_LIMIT30_REDACTED_SMOKE_PLAN.md`，仅规划脱敏样本 smoke，不授权执行。
6. 当前 P1 缺口：`permission_tags`、`project_scope`、`confidentiality_level`、`ModelAssetView.project_id`、`last_seen_at`、explicit lifecycle / missing / moved / stale、index eligibility、`AuditEventView.event_id` 单调递增确认。
7. 下一步建议先让数据库团队评审 `DB_SCHEMA_GAP_REQUEST_TO_DB_TEAM.md`；`LIMIT 30` 脱敏样本 smoke 必须另获用户显式授权。
8. 仍禁止真实样本读取、mirror migration、DB CRUD、NAS scan、selective indexing、production rollout。

## 最新状态

1. 用户已确认：后续 DB / Data Steward prompt 与测试机前置检查不再经由 Codex A，由 Codex B 直接与用户 / 数据库团队 / 测试机 Codex 对接。
2. 新增 `docs/DB_TEAM_DIRECT_HANDOFF_PROTOCOL.md` 固化该流程。
3. Codex A 继续负责主线功能实现；DB 测试机 prompt / precondition / smoke report 由 Codex B 直接维护和审核。
4. 当前可直接把 `docs/CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md` 交给测试机 Codex / operator 执行前置条件检查。
5. 若前置条件返回 Go，仍需用户显式授权后才可重新执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`。
6. 仍禁止真实行读取、secret 输出、NAS scan、DB CRUD、migration、index 写入和 rollout。

## 最新状态

1. Phase 2.69b DB Structure-only Precondition Runbook 已完成 prompt 规划。
2. 新增 `docs/CODEX_DB_STRUCTURE_ONLY_PRECONDITION_PROMPT.md`，用于测试机 Codex / operator 在不连接 DB、不执行 SQL、不安装工具的情况下确认 Hermes_memory install / version、secure env key names、readonly credential key name、contract version、MySQL client 或 Hermes readonly tooling。
3. 结论：`ready_for_test_machine_precondition_check`。
4. 下一步必须先由 Codex B review；通过后用户可把 precondition prompt 交给测试机 Codex。
5. 即使前置条件返回 Go，也不得自动执行 DB smoke；必须等待用户显式指令重新运行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`。
6. 本阶段未连接真实 DB、未执行 SQL、未读取真实行、未扫描 NAS、未写 DB/index、未启用 Data Steward runtime features。
7. 历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty 仍与本阶段无关，继续排除。

## 最新状态

1. 测试机执行 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md` 后返回 `Pause`，且安全边界正确：未连接 DB、未执行 SQL、未读取真实行、未输出 secret 或真实业务数据、未写入任何系统。
2. Pause 原因：Hermes_memory install / version 未确认；DB host / port / database / readonly credential 未出现在已检查的 secure env keys；direct mysql client 不可用。
3. 当前进入 Phase 2.69b DB Structure-only Precondition Runbook。
4. Phase 2.69b 目标：生成测试机前置条件检查 prompt，先确认安装版本、secure env key names、readonly credential 注入状态、MySQL client 或 Hermes readonly tooling。
5. 本阶段仍不连接真实 DB、不执行 SQL、不读取真实行、不扫描 NAS、不写 DB/index、不启用 Data Steward runtime features。
6. 若 Phase 2.69b 前置条件 Go，再重新执行 Phase 2.69 structure-only smoke。
7. 历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty 仍与本阶段无关，继续排除。

## 最新状态

1. Phase 2.69 DB Structure-only Smoke Runbook Planning 已完成。
2. 新增 `docs/CODEX_DB_STRUCTURE_ONLY_SMOKE_PROMPT.md`，可交给测试机 Codex 执行真实 DB `structure_only` smoke。
3. 结论：`ready_for_test_machine_structure_only_smoke`，但必须先经 Codex B review 与用户显式交付。
4. 允许 SQL 仅限 `SELECT 1`、`SELECT DATABASE()`、View 列表、四个 `SHOW COLUMNS`、四个 `WHERE 1 = 0` 空结构查询。
5. 禁止真实行读取、`LIMIT 1` / `LIMIT 30`、secret 输出、真实项目名 / 文件名 / NAS 路径 / raw row 输出、DB CRUD、migration、mirror write、NAS scan、index 写入、production rollout。
6. 测试机执行前仍需数据库团队 / 运维通过安全渠道提供 host / port / database / readonly credential；不得要求 secret 明文。
7. 下一步：Codex B review Phase 2.69 prompt；通过后由用户决定是否交给测试机 Codex 执行。

## 最新状态

1. Phase 2.68 Data Steward DB Branch Intake / Merge Readiness Review 已完成只读接收评审。
2. 结论：`ready_for_mainline_acceptance`。
3. 主线 Data Steward / asset catalog 低耦合接口已存在，feature flags 默认关闭，catalog-only 不进入 `documents` / `chunks` / OpenSearch / Qdrant，Missing Evidence 支持 `asset_catalog_only`，权限缺失路径保持 deny / fail-closed。
4. DB 支线 closeout baseline 已确认：`/Users/Weishengsu/Hermes_memory_db0` branch `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
5. 验证结果：Data Steward target tests `71 passed`，MVP runner regression target `32 passed`，`git diff --check` passed。
6. 风险：DB 支线仍有 12 个未跟踪 QA probe 文件，后续 raw merge / PR 必须排除。
7. 下一步建议：Codex B review；通过后进入 Phase 2.69 测试机真实 DB `structure_only` smoke planning。
8. 仍禁止真实 DB 内容读取、`LIMIT 30` 样本、NAS scan、DB CRUD、migration、mirror write、OpenSearch / Qdrant 写入、repair/backfill/reindex/delete、production rollout。

## 最新状态

1. Phase 2.66e Mac mini HTTP/API retrieval smoke 已回传 `Go`，内部受控 MVP 可继续试用。
2. 当前进入 Phase 2.68 Data Steward DB Branch Intake / Merge Readiness Review。
3. DB 支线 closeout baseline：`/Users/Weishengsu/Hermes_memory_db0`，branch `codex/data-steward-db0-contract`，commit `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
4. 本阶段目标是接收评审与合并准备，不是连接真实 DB、扫描 NAS 或实现 DB CRUD。
5. Codex A 下一步执行 `docs/NEXT_CODEX_A_PROMPT.md`，只读检查主线 Data Steward 接入、feature flags 默认关闭、catalog-only / document evidence 分层、权限缺失默认 deny 与测试覆盖。
6. 若 Phase 2.68 通过，下一阶段才规划测试机真实 DB `structure_only` smoke。
7. 数据库团队配合点后置到 Phase 2.69：测试机 DB 网络路径、只读账号 / API key 安全传递方式、View contract 版本、`structure_only` 授权。
8. 仍禁止 production rollout、DB/NAS 写操作、migration、OpenSearch / Qdrant 写入、repair/backfill/reindex/delete、Agent 直接增删改查 MySQL 或 NAS。
9. 历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty 仍与本阶段无关，继续排除。

## 最新状态

1. Phase 2.65 Mac mini MVP landing baseline 已完成：commit `0262640`，tag `phase-2.65-mac-mini-mvp-landing-baseline`。
2. 当前进入 Phase 2.66 Mac mini Controlled Install Planning。
3. 已新增 `docs/PHASE266_MAC_MINI_CONTROLLED_INSTALL_PLAN.md`，建议下一步先做 Mac mini 侧 preflight-only。
4. Phase 2.66a 只应检查 Mac mini 机器依赖、目录、Git remote/ref、env key 名称；不启动 Docker，不运行 API/CLI smoke，不上传文件，不写 DB/index。
5. 不建议直接 full install；必须先拿到 Mac mini preflight Go / Pause / No-Go。
6. 历史 `docs/PHASE238_TENDER_P1_RECALL_FIX_PLAN.md` dirty 仍与本阶段无关，继续排除。

## 最新状态

1. Phase 2.65 reviewed-ref fix 已完成，等待 Codex B review。
2. hermes-agent reviewed ref 已 pin 为 `phase-2.56e-natural-import-real-upload-smoke-baseline`。
3. reviewed-ref manifest 结果：`ready_for_operator_review`，`pause_reasons=[]`。
4. placeholder-ref manifest 结果：`pause`，`pause_reasons=["missing_reviewed_hermes_agent_ref"]`，保留未来缺 ref fail-closed 语义。
5. 验证结果：py_compile 通过，Phase 2.65 / 2.60 / 2.63 / 2.62 / 2.61a 目标测试 `41 passed`，diff check / latest JSON check 通过。
6. 本阶段仍未执行真实 Mac mini deployment，未启动 Docker，未运行 API / CLI smoke，未连接真实 DB，未扫描 NAS，未上传文件，未写 DB / OpenSearch / Qdrant，未进入 rollout。
7. 下一步：Codex B review Phase 2.65 reviewed-ref fix；通过后写 selective Git baseline prompt。

## 最新状态

1. Phase 2.65 Mac mini MVP Landing Acceleration Pack implementation 已完成，等待 Codex B review。
2. 新增只读 release manifest helper：`scripts/phase265_mvp_release_manifest.py`。
3. 新增 Mac mini install/update quickstart：`docs/MAC_MINI_MVP_INSTALL_UPDATE_QUICKSTART.md`。
4. 当前 manifest sample 为 `Pause`：Hermes_memory ref 已明确为 `phase-2.64b-data-steward-selective-integration-baseline`，hermes-agent reviewed ref 仍为 `NEEDS_REVIEWED_AGENT_REF`。
5. 验证结果：py_compile 通过，Phase 2.65 / 2.60 / 2.63 / 2.62 / 2.61a 目标测试 `40 passed`，manifest sample / diff check / latest JSON check 通过。
6. 本阶段未执行真实 Mac mini deployment，未启动 Docker，未运行 API / CLI smoke，未连接真实 DB，未扫描 NAS，未上传文件，未写 DB / OpenSearch / Qdrant，未进入 rollout。
7. 下一步：Codex B review Phase 2.65；通过后再写 selective Git baseline prompt。

## 最新状态

1. Phase 2.64b Selective Data Steward DB Integration baseline 已完成：commit `da84197`，tag `phase-2.64b-data-steward-selective-integration-baseline`。
2. 当前进入 Phase 2.65 Mac mini MVP Landing Acceleration Pack。
3. 目标：把当前 reviewed Hermes 内核版整理成 Mac mini 测试机可安装 / 可更新 / 可回滚的 landing pack。
4. 本阶段允许新增只读 release manifest helper、Mac mini install/update quickstart 与 Codex Mac mini prompt 更新。
5. 本阶段不执行真实 Mac mini deployment，不启动服务，不上传文件，不运行 API / CLI smoke，不连接真实 DB，不扫描 NAS，不写 DB / index，不进入 rollout。
6. 完成后交 Codex B review；通过后再决定 baseline 与 Mac mini 实机安装。

## 最新状态

1. Phase 2.64b Selective Data Steward DB Integration 已完成首轮实现，等待 Codex B review。
2. 已选择性接入 `app/services/asset_catalog/**`、`tests/test_data_steward_*.py`、Data Steward / DB contract docs 与默认关闭的 feature flags。
3. 未执行 raw merge，未合入 `.claude/**`、DB 支线交接文件、未跟踪 QA probe，未删除或回退 Phase 2.57-2.63 MVP 文件。
4. 验证结果：Data Steward pytest `71 passed`，target ruff `All checks passed!`，Phase 2.63 / 2.62 / 2.61a regression `28 passed`。
5. 本阶段不连接真实 DB，不扫描 NAS，不写 migration，不写 `documents/chunks`，不写 OpenSearch / Qdrant，不创建 PR，不 commit / tag / push。
6. 下一步：Codex B review Phase 2.64b；通过后再决定 selective Git baseline、测试机 DB smoke 或 PR / merge plan。

## 最新状态

1. Phase 2.64 Data Steward DB Branch Intake / PR Review 已完成首轮执行，等待 Codex B review。
2. DB 支线 `/Users/Weishengsu/Hermes_memory_db0` 当前 branch `codex/data-steward-db0-contract`，HEAD `a272081`，tag `phase-db-branch-closeout-merge-readiness-baseline`。
3. DB 支线 branch 与 tag 已推送到 origin，远端均指向 `a272081f1ddd5c71086c488c3f9142eb39e3efa6`。
4. 验证结果：`npm test` 为 `71 passed`，`npm run lint` 为 `All checks passed!`，DB 支线与主线 `git diff --check` 均通过。
5. DB 支线仍有 12 个 expected untracked QA probe 文件，已明确不 stage、不删除、不随 PR 合入。
6. 本阶段未连接真实 DB，未扫描 NAS，未写 migration / `documents` / `chunks` / OpenSearch / Qdrant，未 merge 到 `main`，未创建 PR。
7. 下一步：Codex B review `docs/PHASE264_DATA_STEWARD_DB_BRANCH_INTAKE_PLAN.md` 与 DB 支线 push 结果；通过后再决定是否创建 PR、写 merge plan 或等待测试机真实 DB smoke。

## 最新状态

1. Phase 2.63 Internal MVP Operator Daily Summary Workflow 已完成 implementation，并通过 Codex B review。
2. 新增 `scripts/phase263_mvp_operator_daily_summary.py` 与目标测试，复用 Phase 2.62 summary / issue input 语义。
3. runner 可生成脱敏 JSON / Markdown daily summary，帮助 operator / Codex B 判断 `ready` / `pause` / `no_go`。
4. 目标验证通过：py_compile passed，targeted pytest `28 passed`，`git diff --check` passed，latest JSON check passed。
5. 下一步只执行 selective Git baseline；baseline 后停止。
6. Phase 2.64 建议切到 Data Steward DB Branch Intake / PR Review，以支持数据库团队对接测试机真实 DB。

## 最新状态

1. Phase 2.63 Internal MVP Operator Daily Summary Workflow 已完成首轮 implementation，等待 Codex B review。
2. 新增 `scripts/phase263_mvp_operator_daily_summary.py` 与目标测试，复用 Phase 2.62 summary 逻辑，输出每日 `ready` / `pause` / `no_go` operator summary。
3. 验证通过：py_compile 通过，Phase 2.63 / 2.62 / 2.61a 目标测试 `28 passed`。
4. 本轮未读取真实 issue records、未创建外部 issue、未调用 API/CLI、未上传文件、未写 DB/index、未执行 repair 或 rollout。
5. 下一步：Codex B review Phase 2.63；通过后再写 selective Git baseline prompt。
6. DB / NAS / Data Steward 支线接收任务后置到独立阶段，不打断当前 Mac mini internal MVP operator workflow 收口。

## 最新状态

1. Phase 2.62 Internal MVP Issue Triage Summary Runner 已完成 implementation，并通过 Codex B review。
2. 新增 `scripts/phase262_mvp_issue_triage_summary.py` 与目标测试，复用 Phase 2.61a validator 语义。
3. runner 可读取显式 `--input-json` 或一层 `--input-dir` JSON，输出脱敏 P0/P1/P2/P3 与 ready/pause/no_go summary。
4. 本轮未读取真实 issue records，未创建外部 issue，未调用 API/CLI，未写 DB / facts / versions / audit_logs / OpenSearch / Qdrant。
5. 下一步只执行 selective Git baseline；baseline 后停止，不自动进入 Phase 2.63。
6. 历史无关 dirty 与 DB/NAS 草稿继续排除，不得随 Phase 2.62 baseline 混入。
7. DB / NAS / Data Steward 支线是主线后续组成部分，不再视为无关旁支；但不得打断当前 Phase 2.62 MVP issue triage 收口。
8. DB 支线当前接收状态：`/Users/Weishengsu/Hermes_memory_db0` 分支 `codex/data-steward-db0-contract`，closeout baseline `a272081` / `phase-db-branch-closeout-merge-readiness-baseline`。
9. 后续主线路线需加入 DB 支线接收阶段：先做 PR / merge readiness review，再决定是否合入主线；合入前必须确认 feature flags 默认 off、catalog-only 不进入 `documents/chunks`、不写 OpenSearch / Qdrant、权限缺失默认 deny、probe 文件不合入。
10. DB-5 selective indexing、DB-6 operation plan / approval、真实 DB smoke、真实 NAS / BIM 扫描仍为后置授权事项，不属于 Phase 2.62。

## 最新状态

1. Phase 2.61c baseline 已完成：commit `959ac78`，tag `phase-2.61c-internal-mvp-issue-storage-baseline`。
2. 当前进入 Phase 2.62 Internal MVP Issue Triage Summary Runner。
3. 目标：实现本地只读 triage summary runner，聚合 ignored issue JSON，输出脱敏 P0/P1/P2/P3 与 Go / Pause / No-Go summary。
4. 本轮只读处理人工显式输入或 ignored issue 目录，不创建外部 issue，不写 DB，不 repair，不 rollout。
5. Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 后停止，交 Codex B review。
6. 历史无关 dirty 与 DB/NAS 草稿不得被纳入本阶段。

## 最新状态

1. Phase 2.61c Local Issue Storage Artifact 已完成实现并通过 Codex B review。
2. 新增 `reports/internal_mvp_issues/.gitignore` 与 `README.md`，真实 operator issue JSON / Markdown / 截图 / 日志 / 表格 / 文档默认 ignored。
3. 本轮未生成真实 issue records，未创建外部 issue，未调用 API/CLI，未写 DB / facts / versions / audit_logs / OpenSearch / Qdrant。
4. 下一步执行 Phase 2.61c selective Git baseline；baseline 后再继续 Mac mini internal MVP operator polish / issue triage。
5. 历史无关 dirty 与 DB/NAS 草稿继续排除，不得随 Phase 2.61c baseline 混入。

## 最新状态

1. Phase 2.61b baseline 已完成：commit `d62b8a6`，tag `phase-2.61b-issue-storage-policy-baseline`。
2. 当前进入 Phase 2.61c Local Issue Storage Artifact。
3. 目标：提交 `reports/internal_mvp_issues/.gitignore` 与 `README.md`，让真实 operator issue records 默认 ignored。
4. 本轮不生成真实 issue records，不读取真实 reports，不创建外部 issue，不写 DB，不 repair，不 rollout。
5. Codex A 执行 `docs/NEXT_CODEX_A_PROMPT.md` 后停止，交 Codex B review。
6. 历史无关 dirty 与 DB/NAS 草稿不得被纳入本阶段。

## 最新状态

1. Phase 2.61a baseline 已完成：commit `b60d4d7`，tag `phase-2.61a-mvp-issue-intake-baseline`。
2. Phase 2.61b Local Issue Storage Policy Planning 已完成并通过 Codex B review。
3. 规划建议真实 operator issue records 默认存放在 `reports/internal_mvp_issues/` 并 ignored。
4. 真实 JSON / Markdown 不入 Git；Phase 2.61c 可只提交 `.gitignore` 与 `README.md`。
5. 本轮只做文档规划，未写代码、未写 DB、未创建外部 issue、未 repair、未 rollout。
6. 下一步执行 Phase 2.61b selective docs-only Git baseline；baseline 后才可进入 Phase 2.61c artifact。
7. 历史无关 dirty 与 DB/NAS 草稿不得被纳入本阶段。

## 最新状态

1. Phase 2.61 planning 已完成并经 Codex B review 通过。
2. Phase 2.61a Internal MVP Issue Intake Runner 已完成 implementation，等待 Codex B review。
3. 新增只读本地 issue template / validator / summary generator，把 Mac mini 真实试用问题结构化回收。
4. 目标测试覆盖 template、P2 ready、P1 pause、P0 no_go、dangerous flags、缺 operator judgement、批量统计和 explicit output path。
5. 后续候选：Codex B review 后 selective baseline；或规划本地 ignored issue records 存储策略。
6. 本阶段不得写 DB、不得自动创建外部 issue、不得生成真实业务结论、不得进入 repair 或 rollout。
7. 当前仍禁止真实上传、API/CLI smoke、DB/index 写入、repair/backfill/reindex、Data Steward、production rollout。

## 历史状态

1. Phase 2.60 Internal MVP Launch Readiness Pack 最小实现已完成并 baseline。
2. 新增只读本地 readiness runner：`scripts/phase260_mvp_local_readiness_pack.py`。
3. 该 runner 只输出 Go / Pause / No-Go，不上传文件、不启动服务、不运行 Hermes CLI smoke、不写 DB/index、不执行 repair。
4. 目标测试已覆盖 skip API health go、latest 缺失 pause、危险 env flag no_go、API health failure pause、显式 output JSON、固定 safety fields。
5. baseline 后进入 Phase 2.61 planning，不进入真实 upload、Data Steward 或 production rollout。

## 历史状态

1. Phase 2.59 baseline 已完成：commit `2603a87`，tag `phase-2.59-natural-import-second-smoke-plan-baseline`。
2. 用户决定暂不做第二真实文件 smoke，优先推进 Mac mini 内部 MVP 可用版本。
3. 当前进入 Phase 2.60 Internal MVP Launch Readiness Pack。
4. Phase 2.60 目标：实现只读本地 readiness runner + 测试 + 文档同步，帮助 operator 判断是否可进入内部受控 MVP 使用。
5. 本阶段继续禁止真实上传、API/CLI smoke、DB/index 写入、repair/backfill/reindex、Data Steward、production rollout。

## 历史状态

1. Phase 2.59 docs-only planning 已完成：第二真实文件 natural import smoke 的授权 gate、Codex C 待授权模板与 operator checklist 已同步。
2. 当前不得自动上传文件、运行 API/CLI smoke、写 DB/index 或进入 Data Steward / rollout。
3. 第二真实文件 smoke 必须等待用户提供小型非敏感文件路径并明确授权。
4. Codex C 只可在授权后执行 `docs/NEXT_CODEX_C_PROMPT.md`；direct API upload 不能替代 Hermes / 8642 OpenWebUI-compatible natural-language import path。
5. 下一步建议 Codex B review Phase 2.59；通过后再做 docs-only baseline。

## 历史状态

1. Phase 2.58 baseline 已完成：commit `4a2c57e`，tag `phase-2.58-natural-import-operator-pack-baseline`。
2. 当前进入 Phase 2.59 Natural Import Second Smoke Planning。
3. 本轮只规划第二个小型非敏感文件真实 natural import smoke 的授权门槛、Codex C 模板和验收字段。
4. 当前不上传文件、不运行 API/CLI smoke、不写 DB/index、不进入 Data Steward。
5. 真实第二文件 smoke 必须等待用户提供路径并明确授权。

## 最新状态

1. Phase 2.58 已通过 Codex B review，下一步执行 selective Git baseline。
2. 复核证据：py_compile 通过，targeted pytest `14 passed`，git diff/check 与 latest JSON 校验通过。
3. baseline 白名单限定 operator pack 脚本、测试、Mac mini checklist 与交接文档。
4. 严禁 stage 历史无关 `PHASE238...`、DB/NAS 草稿、ignored latest。
5. baseline 后停止；Phase 2.59 才可规划第二个真实自然语言导入 smoke 或进一步 operator runbook。

## 最新状态

1. Phase 2.58 review-fix 已完成：dry-run review helper 已阻断 `plain_upload_bypass_used=true` 与 `real_file_uploaded=true`。
2. `phase257a_natural_import_evidence_template.py` 已扩展 `--review-json` dry-run review helper。
3. 新增 `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md`，覆盖 preflight、授权、执行、evidence record、Go/Pause/No-Go 与禁止事项。
4. 验证通过：py_compile 通过，targeted pytest `14 passed`。
5. 当前仍不允许真实 upload、API/CLI smoke、DB/index 写入、repair/backfill/reindex 或 rollout；下一步只建议 Codex B review / selective baseline。

## 历史状态

1. Phase 2.57a evidence template runner 已实现并通过目标测试，但按新节奏暂不单独 baseline。
2. Phase 2.58 Natural Import Operator Pack 已完成 operator checklist 与 review helper。
3. Codex B review-fix 已补齐 bypass/upload 阻断：`plain_upload_bypass_used=true` 与 `real_file_uploaded=true` 会 pause。
4. 当前等待 Codex B review；若通过再做一次 selective baseline，减少人工确认和碎片化 baseline。
5. Data Steward / DB / NAS / TB 文件池仍不进入当前主线实现。

## 最新状态

1. Phase 2.57a Natural Import Evidence Template / Runbook Dry-run 最小实现已完成，等待 Codex B review。
2. 新增只读脚本 `scripts/phase257a_natural_import_evidence_template.py` 与测试 `tests/test_phase257a_natural_import_evidence_template.py`。
3. 验证通过：py_compile 通过，Phase 2.57a targeted pytest `7 passed`。
4. 本轮未上传文件、未调用 API / CLI、未写 DB / facts / versions / OpenSearch / Qdrant。
5. 下一步只建议 Codex B review；通过后再 selective baseline，不自动进入 Phase 2.57b。

## 历史状态

1. Phase 2.57 baseline 已完成：commit `ae71f51`，tag `phase-2.57-natural-import-mvp-usability-plan-baseline`。
2. 当前进入 Phase 2.57a Natural Import Evidence Template / Runbook Dry-run。
3. Phase 2.57a 允许新增只读脚本和测试，用于生成 / 校验 natural import evidence pack 模板。
4. 严禁真实 upload、API/CLI smoke、读取文件正文、DB/index 写入、repair/backfill/reindex、DB/NAS/Data Steward 实现。
5. 完成后停止等待 Codex B review，不自动 baseline。

## 历史状态

1. Phase 2.57 planning 已通过 Codex B review，下一步执行 docs-only selective Git baseline。
2. baseline 白名单仅包含 `PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md` 与交接文档。
3. 不得 stage 历史无关 `PHASE238...`、DB/NAS 草稿或 ignored latest。
4. baseline 后停止；Phase 2.57a 才可规划 evidence template / runbook runner dry-run。
5. 继续禁止真实 upload、API/CLI smoke、DB/index 写入、Data Steward 实现和 rollout。

## 最新状态

1. Phase 2.57 Natural Import MVP Usability / Evidence Planning 已完成 docs-only 规划。
2. 新增 `docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md`。
3. 规划覆盖 operator flow、evidence pack、Go / Pause / No-Go、Mac mini runbook outline 与非目标。
4. 本轮未上传文件、未运行 API / CLI、未写代码、未写 DB / OpenSearch / Qdrant。
5. 下一步需要 Codex B review；通过后再做 docs-only baseline。

## 最新状态

1. Phase 2.56e baseline 已完成：Hermes 主仓 `be4b3a375`，Hermes_memory `7e07e4b`，tag `phase-2.56e-natural-import-real-upload-smoke-baseline`。
2. 当前进入 Phase 2.57 Natural Import MVP Usability / Evidence Planning。
3. Phase 2.57 只做 docs-only planning：自然语言导入 evidence pack、Mac mini operator runbook、Go/Pause/No-Go。
4. 不上传文件、不运行 API / CLI smoke、不写代码、不写 DB / index、不进入 DB/NAS/Data Steward。
5. 完成后交 Codex B review，不自动 baseline。

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
44. Phase 2.112e API server stable owner bridge 已实现：accepted `X-Hermes-Session-Id` 与 whitelisted OpenWebUI conversation headers 会传入 `AIAgent.gateway_session_key`，无 stable owner 时继续 fail-closed 并输出 sanitized `stable_owner_missing`；下一步等待 Codex B review，之后才可考虑 runtime baseline / 测试机 OpenWebUI 验证。
45. Phase 2.113 runtime fix 已完成本地最小实现：Hermes 主仓库新增 self-awareness capability boundary、自然导入成功响应强化、无安全文件候选时的 Missing Evidence / suppress retrieval 边界；目标测试通过。
46. Phase 2.113 尚未 baseline；下一步必须 Codex B review，并由 Codex C / 测试机验证 OpenWebUI / 8642 真实用户侧是否稳定呈现 Hermes_memory / workspace / retrieval / evidence kernel 能力。
47. Phase 2.113a 已完成 Codex B review fix：file-discovery intent 收窄，普通内容检索不再因“找一下 / 帮我找”被 suppress；明确候选文件查找仍 fail-closed。
48. Phase 2.113a 已补 self-awareness trigger 自然问法覆盖，目标验证 `102 passed`。
49. Phase 2.113a Codex B review 已通过；Hermes agent runtime test-candidate 已推送：`a12d378e0` / `phase-2.113a-self-awareness-runtime-test-candidate`。
50. 测试机 / OpenWebUI / 8642 live validation 已返回 Go：self-awareness、ordinary retrieval guard、fuzzy file discovery 与安全边界通过；可选 natural import feedback 因未授权导入而跳过。
51. 下一步为 Phase 2.113 closeout / Phase 2 final freeze checklist 更新；不得把该 Go 解释为 production rollout、NAS 全量扫描、DWG/RVT/BIM 内容理解或无限制 memory 写入。
52. Phase 2.114 规划已启动：最终验收必须用一个授权小文件跑通 self-awareness -> natural-language import -> alias -> retrieval -> citation -> evidence boundary。
53. Phase 2.114 通过前不得发布 Phase 2 stable MVP freeze tag；通过后仍不得宣称 production rollout、NAS 全量扫描、DWG/RVT/BIM 内容理解或 PRD/Roadmap 300+ eval closeout。
54. Phase 2.114a 已完成 natural import path parser 最小修复：中文全角冒号、中文句号、中文路径、目录空格和 alias 同 prompt 均已覆盖；多路径仍 fail-closed。
55. Phase 2.114a runtime test-candidate 已推送：Hermes 主仓库 commit `c8ed29a83c441f58939f64b6b175ae4cac980ea3`，tag `phase-2.114a-natural-import-path-parser-runtime-test-candidate`。
56. 下一步必须由测试机 / OpenWebUI / 8642 复跑 Phase 2.114 final user-flow acceptance；不得跳过真实 import -> alias -> retrieval -> citation 验收。
57. Phase 2.114a 测试机 / OpenWebUI / 8642 复验已 Go：授权小样本 path extraction、natural import、same-session alias retrieval、evidence IDs、citation 与 safety flags 均通过。
58. Phase 2 final user-flow acceptance gate 已在 `eval/phase2_inventory/phase2_final_freeze_checklist.json` 标记为 `go`；下一步是 Phase 2 stable MVP closeout / Phase 3 known-gap carryover，不再继续扩 Phase 2 功能。
59. 用户确认 `PROJECT_CONTEXT` 不应作为最终用户必填输入；应由 Hermes 从文件名、目录标签、会话与已有 workspace/alias 自动推断。
60. Phase 2.115 启动：Workspace Context Inference / Auto Alias / Fuzzy File Discovery，目标是让用户只说“帮我导入这个文件”，Hermes 自动放入工作区、生成安全别名并支持后续模糊找文件。
61. 2.115 仍禁止 raw path/raw content/secret 写 memory，禁止把 workspace metadata 当 retrieval evidence，禁止平台 Gateway 改动、NAS 全量扫描、DWG/RVT/BIM 内容理解与 production rollout。
62. Phase 2.115 本地实现候选已通过 Codex B review：Hermes 主仓 `1ac8099e4` / `phase-2.115-workspace-auto-alias-runtime-test-candidate`，targeted regression `129 passed`。
63. 下一步必须由测试机 / OpenWebUI / 8642 验证无 `PROJECT_CONTEXT`、无显式 `ALIAS` 的导入流、generated alias retrieval 与 fuzzy discovery。
64. Phase 2.115 用户实测已证明功能链路基本通过：文件导入、workspace inference、generated alias、alias retrieval citation、fuzzy discovery 均可用。
65. 新 UX blocker：默认导入成功/失败回复仍输出大段 `Natural file import diagnostics` 和技术字段，需 Phase 2.116 改成用户态自然语言回复。
66. Phase 2.116 只允许改 response rendering / tests，禁止改 upload、ingestion/indexing、retrieval、workspace inference、平台 Gateway 或 NAS。
67. Phase 2.116b 本地最小修复已完成：fuzzy discovery candidate display 现在会对 `title/source_name/display_path` 的绝对路径 fallback 做 basename-only 安全渲染；same-session alias retrieval 会用实际 in-scope evidence 覆盖 stale `third_document_contamination`。
68. Phase 2.116b 验证：targeted regression `2 passed`；py_compile 通过；natural import / flow / session scope / structured citation / file steward regression `132 passed`。
69. Phase 2.116b 仍未 baseline：下一步必须 Codex B review，随后 Codex C / 测试机重跑 Phase 2.116 live validation，确认 Case 2 contamination false positive 与 Case 4 raw path leak 均解除。

## 后置项

## Phase 2.112f 当前状态

1. Phase 2.112f 最小修复已完成并通过 Codex B review：follow-up alias continuity restore diagnostics 稳定进入 nested `alias_resolution`。
2. 已补 same-owner import -> follow-up restore 跨 store reload / 新 agent instance 测试。
3. 已补 stable owner missing、cross-owner denied、conflict denied 与 restored filters 覆盖。
4. Codex B 复跑验证：py_compile 通过；full natural import / upload client / session scope regression `109 passed`；gateway stable-owner targeted tests `3 passed`。
5. Hermes agent runtime test-candidate 已推送：commit `78eb77158`，tag `phase-2.112f-alias-continuity-restore-runtime-test-candidate`。
6. 本轮未重复真实导入，未写 DB / facts / document_versions / OpenSearch / Qdrant，未执行 repair/backfill/reindex。
7. 下一步必须测试机复验 OpenWebUI / 8642 import -> follow-up `@alias` retrieval + citation。

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

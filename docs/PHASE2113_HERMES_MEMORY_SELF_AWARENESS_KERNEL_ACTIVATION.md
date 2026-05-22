# Phase 2.113 Hermes Memory Self-Awareness / Kernel Activation

## 1. Purpose

Phase 2.113 records a P0 blocker discovered during real OpenWebUI / 8642 use:

```text
Hermes can execute the Hermes_memory import / retrieval pipeline, but the user-facing Agent persona does not reliably know or explain that Hermes itself owns a memory / workspace / retrieval / evidence kernel.
```

This is not a cosmetic prompt issue. It is a product-kernel blocker because Hermes must not become a generic chatbot sitting in front of a separately developed memory system.

Phase 2.113 is the next Codex A implementation handoff. This document does not modify runtime code by itself.

## 2. Root Cause Read

Observed symptoms:

1. User-facing Hermes did not naturally explain that it has a governed memory / document workspace / retrieval evidence system.
2. Natural import succeeded only after repeated operational steps, feature flag checks, alias debugging, and environment fixes.
3. After import, Hermes did not yet provide the expected product-level experience:
   - "文件我已经记下了";
   - "我给它设定别名为 `@xxx`";
   - "以后你可以直接问我这个文件";
   - "如果你模糊找文件，我会列出候选并请你确认".
4. Ordinary memory and document workspace are not clearly separated in the user-facing behavior.
5. The memory kernel has strong low-level pieces, but the Agent's self-description and action policy do not reliably activate them as native Hermes capabilities.

Likely implementation areas for Codex A to inspect:

1. `hermes-agent` OpenAI-compatible / 8642 gateway prompt construction.
2. `AIAgent` / memory-kernel context assembly.
3. Natural import success-response rendering.
4. Alias generation / alias persistence user-facing summary.
5. Fuzzy file-discovery and session document-scope behavior.
6. Low-sensitive memory candidate generation and rejection paths.

Do not assume the exact file names above are complete; Codex A must inspect the current runtime code before patching.

## 3. Required Product Behavior

### 3.1 Hermes Self-Awareness

When the user asks what Hermes can do, Hermes should answer as an enterprise memory-kernel Agent, not as a generic conversational assistant.

Required capabilities to mention, with boundaries:

1. It can help manage enterprise files that have been authorized for import or catalog access.
2. It can import supported files through the governed natural-language path when enabled.
3. It can bind and reuse safe aliases such as `@建筑类数据样表`.
4. It can retrieve from indexed document evidence and cite evidence.
5. It can say Missing Evidence when content, permission, parser, or index evidence is unavailable.
6. It can keep low-sensitive continuity hints such as aliases, document IDs, version IDs, project context, query IDs, and related file IDs.
7. It cannot store raw file content, raw NAS paths, secrets, raw DB rows, or customer-sensitive free text in ordinary memory.
8. It cannot claim DWG / RVT / BIM content understanding unless governed content evidence exists.

### 3.2 Natural Import User Experience

The target user experience is:

```text
User: 帮我导入这个文件：<authorized path>，这是 C塔项目人力配置及成本测算表。

Hermes: 文件我已经导入并建立检索索引。别名我设定为：@C塔项目人力配置及成本测算表。
你以后可以这样问我：
1. @C塔项目人力配置及成本测算表 里有哪些主要字段？
2. 帮我找 C塔项目人力配置相关文件。
3. 这份表和 C塔方案有什么关联？如果证据不足我会标 Missing Evidence。
```

If the user provides an explicit alias, that alias wins if it is safe and well-formed.

If the user does not provide an alias, Hermes should generate or recommend a safe alias from:

1. file title / source name;
2. user-provided project context;
3. supported suffix / document type;
4. collision-safe disambiguator if needed.

Generated aliases must be bounded and safe:

1. no raw path;
2. no secret;
3. no unbounded free text;
4. no content claim;
5. no global cross-user binding.

### 3.3 Fuzzy File Discovery

When the user asks:

```text
C塔项目的招标要求文件你帮我找出来
```

Hermes should not immediately hallucinate one exact file. It should:

1. search current safe workspace / alias / catalog candidates available to the session or authorized context;
2. return a bounded candidate list with alias, safe title, document_id / version_id or safe file_id when available;
3. ask the user to choose if multiple candidates match;
4. return Missing Evidence if no safe candidate exists;
5. never expose raw storage path or raw DB row.

If fuzzy discovery cannot be implemented fully in this phase, Codex A must implement a fail-closed fallback that explains the current limitation and does not pretend to have found files.

### 3.4 Memory / Workspace Boundary

Hermes may keep low-sensitive continuity hints:

1. alias;
2. document_id;
3. version_id;
4. project_context;
5. query_id / trace_id;
6. related_file_ids;
7. user-confirmed preference labels.

Hermes must not store in ordinary memory:

1. raw file content;
2. raw NAS path;
3. raw storage URI;
4. raw DB row;
5. secrets, tokens, credentials;
6. customer-sensitive text copied from documents;
7. unsupported inference such as "this RVT contains component X".

Workspace metadata is not content evidence. A document alias proves only which document to search; it does not prove the answer.

## 4. Required Codex A Implementation Scope

Codex A should implement the smallest runtime fix that activates Hermes's self-awareness and workspace behavior in the OpenWebUI / 8642 path.

Required:

1. Add or update kernel self-awareness instructions in the runtime prompt / context builder.
2. Add or update natural import success response so it reports:
   - import status;
   - alias used or generated;
   - document_id / version_id if safe;
   - chunk / index status if available;
   - suggested follow-up questions;
   - clear Missing Evidence boundary.
3. Ensure no-alias import generates or recommends a safe alias.
4. Ensure explicit alias remains preserved.
5. Add bounded fuzzy file-discovery behavior or fail-closed fallback.
6. Ensure low-sensitive continuity candidate behavior does not write forbidden memory.
7. Add diagnostics sufficient to distinguish:
   - alias bound;
   - alias generated;
   - alias reused;
   - fuzzy candidates found;
   - memory hint rejected;
   - retrieval evidence missing.

Not required in this phase:

1. full NAS scan;
2. DB CRUD;
3. Agent-generated SQL;
4. production rollout;
5. DWG / RVT / BIM content parsing;
6. platform native session migration;
7. full long-term memory productization;
8. broad employee usability matrix beyond targeted tests.

## 5. Tests Codex A Must Add or Update

Codex A should use TDD and add targeted tests before runtime changes.

Minimum test set:

1. Self-awareness answer:
   - prompt asks "你能做什么 / 你有没有记忆库 / 你能不能管理文件";
   - expected answer mentions Hermes_memory / workspace / retrieval evidence / alias / Missing Evidence;
   - forbidden answer: generic chatbot only, or overclaiming unrestricted NAS / BIM understanding.
2. Natural import with explicit alias:
   - import utterance contains a safe alias;
   - success response says the exact alias;
   - follow-up can resolve the exact alias.
3. Natural import without alias:
   - success response generates or recommends a safe alias;
   - generated alias has no raw path and is session/workspace scoped.
4. Fuzzy file discovery:
   - multiple safe candidates returns candidate list + clarification question;
   - no candidates returns Missing Evidence / no safe candidate;
   - unsupported scope does not run ordinary retrieval against unrelated docs.
5. Memory boundary:
   - allowed low-sensitive hint is accepted only as context;
   - raw path / file content / secret memory candidate is rejected;
   - memory reference is not treated as evidence.
6. Overclaim guard:
   - DWG / RVT / BIM content questions still return Missing Evidence unless governed evidence is present.

Recommended validation commands:

```bash
python3 -m py_compile <changed python files>
uv run pytest <targeted tests for self-awareness / natural import / session scope / memory boundary>
git diff --check
```

If `uv run pytest` is unavailable in a specific machine environment, Codex A must report the environment reason and run the closest existing targeted test command without installing dependencies unless authorized.

## 6. Hard Prohibitions

Do not:

1. scan NAS;
2. run production rollout;
3. expose raw file paths;
4. expose raw DB rows;
5. write secrets or raw document text into memory;
6. make platform Gateway broader than catalog-only;
7. change DB schema;
8. write OpenSearch / Qdrant / MinIO outside existing authorized import/index paths;
9. run repair / cleanup / backfill / reindex / delete / migration;
10. implement Agent DB CRUD or arbitrary SQL;
11. claim DWG / RVT / BIM content understanding;
12. turn diagnostics into retrieval evidence.

## 7. PRD Deviation Self-Audit

This phase also records current PRD deviations that remain open or need explicit reclassification.

### P0 blocker

1. **Hermes Memory Self-Awareness / Kernel Activation**: not complete before this phase. Hermes must know how to present and use its own memory / workspace / evidence kernel.

### P1 / closeout blockers

1. Accepted eval inventory remains far below PRD / Roadmap target scale.
2. Top5 and citation metrics are not computed at required scale.
3. Structured fact manual spot-check is still missing.
4. Natural import is `passed_with_scope`, not unrestricted production import.
5. Parser/source coverage is not consolidated into final metric evidence.
6. Tender deep-field behavior remains partial / Missing Evidence / manual-review dependent.
7. Version diff and incremental invalidation lifecycle remain partial.
8. RBAC / ABAC remains basic / contract-level, not complete enterprise permission product.
9. Knowledge-admin and human validation workflow remain partial.
10. Platform integration remains catalog-only / Gateway wrapped; it does not yet expose native Hermes session / Evidence Layer / Memory Layer.
11. Data Steward DB / NAS / BIM remains catalog-only plus controlled small-batch dry-run/smoke; it is not full model content understanding or full NAS semantic indexing.

### Correct interpretation

Phase 2 may keep a stable platform integration baseline and a scoped natural import acceptance result, but full Phase 2 completion must remain blocked until these items are closed or explicitly reclassified by the user.

## 8. Expected Final Report from Codex A

Codex A must report:

1. changed files;
2. self-awareness behavior implemented;
3. natural import alias / generated alias behavior;
4. fuzzy file discovery behavior;
5. memory boundary behavior;
6. tests run and results;
7. forbidden actions not performed;
8. whether Codex B review is required;
9. whether test-machine / OpenWebUI / 8642 validation is required.

Do not declare Phase 2 complete from this phase alone.

# Phase 2.112 Natural Import Workspace Retrieval Fix Plan

## 1. Background

Phase 2.111 live operator testing proved the natural-language import chain can reach the real upload adapter when the 8642 Hermes gateway process has `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true`.

Observed live evidence:

```text
natural_import_detected=true
real_upload_enabled=true
upload_adapter_status=executed
ingestion_status=upload_succeeded
document_id=2baf5527-42c9-4467-8856-573e54c97121
version_id=b2efc465-cde8-4aef-a113-5c8615929719
chunk_count=6
indexed_count=6
```

Remaining blocker:

```text
alias_resolution.status=bound_to_document
retrieval_evidence_document_ids=[]
citation=Missing Evidence
```

A manual attempt to remember the alias also hit ordinary long-term memory quota. That is useful evidence: file workspace state must not be stored as ordinary memory text.

## 2. User Experience Target

The intended company-kernel Agent experience is not an operator-heavy upload ceremony.

A normal user should be able to say:

```text
帮我导入这个文件。
```

Hermes should then:

1. Detect a single authorized file path or ask for the missing file if no path is available.
2. Run the real import path when explicitly enabled.
3. Generate a safe alias automatically if the user does not provide one.
4. Bind the imported document to session alias / active document state, not ordinary long-term memory.
5. Return a concise confirmation:

```text
文件我已经记下了。
别名我设定为：@建筑类数据样表
后续你可以用这个别名继续问我。
```

If the user later asks:

```text
C塔项目的招标要求文件你帮我找出来。
```

Hermes should perform safe fuzzy file discovery across known session/workspace aliases and governed file metadata, then return candidates:

```text
我找到几个可能相关的文件：
1. @C塔招标文件 —— ...
2. @C塔招标清单 —— ...
请问你说的是哪一个？
```

Hermes must not invent file contents or claim it has read unsupported evidence.

## 3. Phase 2.112 Goal

Implement the minimum runtime fix needed for Phase 2 closeout evidence:

1. Natural import success must seed session alias / active document state.
2. Same-session `@alias` follow-up retrieval must use scoped retrieval for the imported `document_id` / `version_id`.
3. Retrieval must return citation-bearing evidence from the imported document only.
4. If no alias is supplied, Hermes should generate a deterministic safe alias from filename / title / project context.
5. File alias / workspace state must not be written as ordinary long-term memory.
6. Fuzzy file discovery may be implemented as a bounded session/workspace helper or documented as a follow-up if runtime scope is too large, but it must be represented in diagnostics and tests.

## 4. Required Fix Boundaries

Allowed:

1. Hermes main repo runtime / tests related to natural import alias seeding, active document, and scoped retrieval.
2. Deterministic safe alias generation helper.
3. Session/workspace alias store updates after successful import.
4. Bounded fuzzy alias / file discovery helper over session/workspace known aliases and safe metadata.
5. Targeted unit tests and a small CLI / gateway-compatible smoke if available.
6. Hermes_memory docs / handoff sync.

Forbidden:

1. Do not write alias bindings to ordinary long-term memory as text.
2. Do not treat import diagnostics as retrieval evidence.
3. Do not bypass retrieval/citation by answering from upload metadata.
4. Do not use direct API upload as substitute evidence.
5. Do not scan NAS or folders.
6. Do not enable production rollout.
7. Do not repair, cleanup, backfill, reindex, delete, or migrate.
8. Do not change platform Gateway or DB/NAS Data Steward contracts.
9. Do not expose raw path, file content, secrets, raw DB rows, or raw answers.
10. Do not claim DWG/RVT/BIM content understanding.

## 5. Acceptance Criteria

A Phase 2.112 pass requires all of the following:

1. Import with explicit alias:
   - `natural_import_detected=true`
   - `real_upload_enabled=true`
   - upload succeeds
   - `document_id` and `version_id` are present
   - `chunk_count > 0`
   - `indexed_count > 0`
   - alias status is `alias_bound` or equivalent
   - subsequent `@alias` query returns `retrieval_evidence_document_ids=[imported_document_id]`
   - citation is present
2. Import without explicit alias:
   - Hermes generates a safe alias and reports it to the user.
   - The generated alias works in same-session retrieval.
3. Memory boundary:
   - No ordinary memory write is required for alias persistence.
   - If low-sensitive memory candidates are emitted, they contain only safe refs such as `document_id`, `version_id`, alias, query_id, and project label; no raw path or file content.
4. Fuzzy file discovery:
   - A query like `C塔项目的招标要求文件你帮我找出来` returns safe candidate aliases / safe file refs, or asks for clarification when multiple candidates exist.
   - It does not answer file content without retrieval evidence.
5. Safety:
   - `metadata_as_answer=false`
   - `facts_as_answer=false`
   - `snapshot_as_answer=false`
   - `transcript_as_fact=false`
   - `third_document_contamination=false`

## 6. Suggested Test Cases

1. Explicit alias import:

```text
请导入文件 /Users/hermes/import_samples/building_data_20260519.xlsx，别名 @建筑类数据样表，项目 自然语言导入测试
```

2. Same-session retrieval:

```text
围绕 @建筑类数据样表 总结这个文件的主要内容，必须给出 citation；请输出 alias_resolution、retrieval_evidence_document_ids、document_id、version_id。
```

3. Auto alias import:

```text
帮我导入 /Users/hermes/import_samples/building_data_20260519.xlsx，归到 自然语言导入测试。
```

Expected: Hermes reports the generated alias.

4. Fuzzy discovery:

```text
自然语言导入测试里的建筑类数据文件你帮我找出来。
```

Expected: Hermes lists safe candidate alias/file refs and asks for clarification if needed.

## 7. Closeout Decision

Phase 2 full closeout remains blocked until Phase 2.112 passes or the user explicitly moves natural import usability out of Phase 2.

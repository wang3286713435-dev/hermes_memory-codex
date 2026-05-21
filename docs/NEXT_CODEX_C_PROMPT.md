# NEXT_CODEX_C_PROMPT

## Phase 2.112 Natural Import Workspace Retrieval Validation

Codex B review has passed the Phase 2.112 targeted implementation at test level. Codex C should now validate the real user path through OpenWebUI -> 8642 Hermes backend.

Do not run this validation until the user/operator confirms the exact small non-sensitive file path and that the 8642 Hermes backend is running with:

```text
HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true
```

## Required Reviewed State

Hermes_memory docs baseline:

```text
/Users/hermes/code/Hermes_memory
phase-2.112-natural-import-workspace-retrieval-prompt-baseline
```

Hermes agent implementation must include the Phase 2.112 changes reviewed by Codex B:

```text
natural import success -> session alias / active document seed
same-session @alias -> document_id/version_id scoped retrieval
safe auto alias generation when alias is omitted
bounded session alias discovery for fuzzy file finding
```

If the implementation is not present, stop with `Pause`.

## Required User Inputs

Use one small non-sensitive file only:

```text
AUTHORIZED_FILE_PATH=<exact test-machine path>
PROJECT_CONTEXT=<short context label>
OPTIONAL_ALIAS=<optional; if omitted, Hermes should generate one>
```

Do not test folders, multiple files, NAS scan, BIM model pools, or sensitive files.

## Environment Preflight

1. Confirm 8642 is listening and is the Hermes backend expected by OpenWebUI.
2. Confirm 8642 health/model endpoint works without printing tokens/secrets.
3. Confirm `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` is visible to the 8642 backend process.
4. Confirm Hermes_memory API `/health` is OK if the upload adapter requires it.
5. Confirm the source file exists, is regular, small, and non-sensitive.
6. Confirm no production rollout / cleanup / repair / backfill / reindex / migration is authorized.

## Smoke A: Explicit Alias Import

If `OPTIONAL_ALIAS` is provided, use it. Otherwise choose a safe alias such as `@建筑类数据样表`.

In OpenWebUI, ask Hermes:

```text
请导入文件 <AUTHORIZED_FILE_PATH>，别名 <ALIAS>，项目 <PROJECT_CONTEXT>
```

Expected import result:

```text
natural_import_detected=true
real_upload_enabled=true
upload_adapter_status=executed/succeeded
ingestion_status=upload_succeeded/completed
document_id present
version_id present
chunk_count > 0
indexed_count > 0
alias_resolution.status=alias_bound or alias_resolved
alias_persisted=true or equivalent
```

Then ask in the same OpenWebUI conversation:

```text
围绕 <ALIAS> 总结这个文件的主要内容，必须给出 citation；请输出 alias_resolution、retrieval_evidence_document_ids、document_id、version_id。如果证据不足，请明确 Missing Evidence。
```

Expected retrieval result:

```text
retrieval_evidence_document_ids=[imported document_id]
citation present
third_document_contamination=false
metadata_as_answer=false
facts_as_answer=false
snapshot_as_answer=false
transcript_as_fact=false
```

## Smoke B: Auto Alias Import

Use a second small non-sensitive file only if the user explicitly authorizes one. If not authorized, mark Smoke B as skipped.

Ask:

```text
帮我导入 <AUTHORIZED_FILE_PATH>，归到 <PROJECT_CONTEXT>。
```

Expected:

```text
Hermes reports a generated safe alias, e.g. `别名我设定为：@xxx`
generated alias works in same-session retrieval
ordinary long-term memory write is not required for alias persistence
```

## Smoke C: Bounded Fuzzy File Discovery

After at least one alias exists in the same session, ask:

```text
<PROJECT_CONTEXT> 里的相关文件你帮我找出来。
```

Expected:

```text
Hermes lists safe candidate aliases / file refs from session alias workspace
Hermes asks for clarification if multiple candidates exist
Hermes does not answer file content without retrieval evidence
Hermes does not expose raw path or file content
```

## Stop Conditions

Stop and report `Pause` if:

1. 8642 backend does not have real upload enabled.
2. Import does not return document_id/version_id.
3. `chunk_count` or `indexed_count` is missing or zero.
4. Alias does not bind or generated alias is missing.
5. Same-session `@alias` retrieval returns empty `retrieval_evidence_document_ids`.
6. Citation is missing after retrieval.
7. Retrieval returns a document other than the imported document.
8. Import diagnostics or metadata are used as answer evidence.
9. Any raw path, file content, secret, token, raw DB row, or raw answer would be printed.
10. Any cleanup, repair, backfill, reindex, delete, migration, NAS scan, DB CRUD, or rollout is attempted.

## Report Format

Return a sanitized report:

```text
API / 8642 health:
Hermes_memory health:
real_upload_flag_visible_to_backend:
session_id / conversation id if available:
source_file_preflight: exists / regular / size bucket / suffix only
explicit_alias_import: pass / partial / fail / skipped
document_id:
version_id:
chunk_count:
indexed_count:
alias_status:
same_session_retrieval: pass / partial / fail
retrieval_evidence_document_ids:
citation_present:
auto_alias_import: pass / partial / fail / skipped
fuzzy_file_discovery: pass / partial / fail / skipped
third_document_contamination:
metadata_as_answer:
facts_as_answer:
snapshot_as_answer:
transcript_as_fact:
ordinary_memory_write_required_for_alias:
forbidden_action_attempted:
Go / Pause / No-Go:
blocking_reason:
```

Do not commit, tag, push, upload extra files, scan NAS, mutate DB/index/object store, or print secrets/raw content.

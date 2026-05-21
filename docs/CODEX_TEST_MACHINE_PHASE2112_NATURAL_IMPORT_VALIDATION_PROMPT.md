# Test-machine Codex Prompt — Phase 2.112 Natural Import Validation

## Role

You are the **test-machine operator Codex** running on the Mac mini / test machine. You are not Codex C.

Your job is to validate the real user path through:

```text
OpenWebUI -> 8642 Hermes OpenAI-compatible backend -> Hermes Memory upload / retrieval
```

Codex C is a separate development-machine testing session. Codex C may build or review test code, but must not be treated as the test-machine operator.

## Current Pause Evidence

The latest real OpenWebUI / 8642 run against the Phase 2.112b candidate reached import success but still paused at alias / retrieval:

```text
natural import succeeded
document_id=2baf5527-42c9-4467-8856-573e54c97121
version_id=b2efc465-cde8-4aef-a113-5c8615929719
chunk_count=6
indexed_count=6
import initially alias_bound
follow-up @建筑类数据样表 retrieval alias_missing=true
retrieval_suppressed=true
retrieval_evidence_document_ids=[]
citation_present=false
```

Do not repeat imports until a new reviewed Hermes agent fix is available. The next validation should focus on alias continuity / same-session retrieval after Codex A fixes the OpenAI-compatible / OpenWebUI runtime.

## Required Reviewed State

Before validation, confirm the test-machine Hermes agent checkout has been updated to the latest Codex B-reviewed Phase 2.112c candidate. The failed Phase 2.112b candidate was:

```text
/Users/hermes/code/hermes-agent
tag: phase-2.112b-natural-import-alias-runtime-test-candidate
commit: 1d02a7918
remote: backup2 / hermes_repo
```

Do not treat that Phase 2.112b tag as sufficient for the next Go decision; it is now the known failed baseline for same-session alias retrieval.

Also confirm Hermes_memory handoff checkout is at or after:

```text
/Users/hermes/code/Hermes_memory
tag: phase-2.112b-codex-b-review-pass-baseline
```

If the test machine still points to the old Phase 2.112 implementation or an unreviewed dirty worktree, stop with `Pause`.

## Required User Authorization

Use only one explicitly authorized small non-sensitive file:

```text
AUTHORIZED_FILE_PATH=<exact test-machine path>
PROJECT_CONTEXT=<short context label>
OPTIONAL_ALIAS=<optional; if omitted, Hermes should generate one>
```

Do not test folders, multiple files, NAS scan, BIM model pools, or sensitive files.

## Environment Preflight

1. Confirm 8642 is listening and is the backend OpenWebUI is using.
2. Confirm `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` is visible to the 8642 backend process.
3. Confirm Hermes Memory API `/health` is OK if the upload adapter requires it.
4. Confirm the source file exists, is regular, small, and non-sensitive.
5. Confirm no production rollout / repair / cleanup / backfill / reindex / migration is authorized.
6. Do not print token, secret, raw file content, or full raw file path in final output.

## Smoke A — Natural Import With Alias

In the same OpenWebUI conversation, ask Hermes:

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
ordinary_memory_write_required_for_alias=false
```

Then ask:

```text
围绕 <ALIAS> 总结这个文件的主要内容，必须给出 citation；请输出 alias_resolution、retrieval_evidence_document_ids、document_id、version_id。如果证据不足，请明确 Missing Evidence。
```

Expected retrieval result:

```text
alias_resolution.status=alias_resolved
retrieval_suppressed=false
retrieval_evidence_document_ids=[imported document_id]
citation present
third_document_contamination=false
metadata_as_answer=false
facts_as_answer=false
snapshot_as_answer=false
transcript_as_fact=false
```

## Smoke B — Auto Alias

Only if the user authorizes a second small file, ask:

```text
帮我导入 <AUTHORIZED_FILE_PATH>，归到 <PROJECT_CONTEXT>。
```

Expected:

```text
Hermes reports a generated safe alias, e.g. `别名我设定为：@xxx`
generated alias works in same-session retrieval
ordinary long-term memory write is not required for alias persistence
```

If no second file is authorized, mark this smoke as `skipped`.

## Smoke C — Bounded Fuzzy File Discovery

After at least one alias exists in the same session, ask:

```text
<PROJECT_CONTEXT> 里的相关文件你帮我找出来。
```

Expected:

```text
Hermes lists safe candidate aliases / file refs from the session workspace
Hermes asks for clarification if multiple candidates exist
Hermes does not answer file content without retrieval evidence
Hermes does not expose raw path or file content
```

## Stop Conditions

Stop and report `Pause` if:

1. 8642 backend does not have real upload enabled.
2. Import does not return `document_id` / `version_id`.
3. `chunk_count` or `indexed_count` is missing or zero.
4. Alias bind returns `alias_bind_failed`.
5. Follow-up retrieval returns `alias_missing=true`.
6. Follow-up retrieval returns `retrieval_suppressed=true` for the imported alias.
7. Same-session `@alias` retrieval returns empty `retrieval_evidence_document_ids`.
8. Citation is missing after retrieval.
9. Retrieval returns a document other than the imported document.
10. Import diagnostics or metadata are used as answer evidence.
11. Any raw path, file content, secret, token, raw DB row, or raw answer is printed.
12. Any cleanup, repair, backfill, reindex, delete, migration, NAS scan, DB CRUD, or rollout is attempted.

## Report Format

Return a sanitized report:

```text
backend_port:
backend_health:
real_upload_flag_visible_to_backend:
source_file_preflight: exists / regular / size bucket / suffix only
explicit_alias_import: pass / partial / fail / skipped
document_id:
version_id:
chunk_count:
indexed_count:
alias_status:
same_session_retrieval: pass / partial / fail
alias_missing:
retrieval_suppressed:
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

# Codex C Natural Import Acceptance Smoke Prompt

## Status

This prompt is a placeholder for a future authorized smoke.

Do not execute it until the user explicitly provides:

```text
<AUTHORIZED_FILE_PATH>
<ALIAS>
<PROJECT_CONTEXT>
```

The file must be one small non-sensitive file. Authorization for one file does not authorize folders, NAS scan, cleanup, repair, backfill, reindex, migration, rollout, or unrelated uploads.

## Goal

Validate the Hermes CLI natural-language import path:

```text
请把 <AUTHORIZED_FILE_PATH> 导入 Hermes，归到 <PROJECT_CONTEXT>，并绑定为 <ALIAS>
```

Direct API upload is not valid substitute evidence.

## Required Preflight

1. Confirm user authorization names the exact file path.
2. Confirm file is a regular small non-sensitive file.
3. Confirm Hermes_memory API `/health`.
4. Confirm Hermes CLI availability.
5. Run the natural import dry-run evidence template and review helper if applicable.
6. Confirm cleanup / delete / repair / backfill / reindex / migration / rollout remain unauthorized.

## Required Smoke

1. Run the import through Hermes CLI natural-language path.
2. Capture sanitized values only:
   - `session_id`
   - `document_id`
   - `version_id`
   - `chunk_count`
   - `indexed_count`
   - alias resolution status
   - returned document ids
   - citation presence
   - third-document contamination status
3. Ask a same-session follow-up query using `<ALIAS>`.
4. Confirm returned document ids only include the imported document.
5. Confirm citation exists.
6. Confirm:
   - `metadata_as_answer=false`
   - `facts_as_answer=false`
   - `snapshot_as_answer=false`
   - `transcript_as_fact=false`

## Stop Conditions

Stop immediately if:

1. API or CLI is unavailable.
2. Authorization is incomplete.
3. Direct API upload is used.
4. The path is missing, multiple, directory-like, NAS/network/bulk, unsupported, unreadable, or too large.
5. Import fails or returns no `document_id` / `version_id`.
6. Alias does not persist in the same session.
7. Follow-up retrieval has no citation.
8. Third-document contamination appears.
9. Raw path, raw text, secret, raw DB row, raw answer, or customer-sensitive material would be printed.
10. Continuing would require cleanup / repair / backfill / reindex / delete / migration / rollout.

## Report Format

Return a sanitized table:

```text
API status:
CLI status:
session_id:
natural_import_path_used:
direct_api_upload_used:
document_id:
version_id:
chunk_count:
indexed_count:
alias_status:
retrieval_evidence_document_ids:
citation_present:
third_document_contamination:
metadata_as_answer:
facts_as_answer:
snapshot_as_answer:
transcript_as_fact:
Go/Pause/No-Go:
blocking_reason:
```

Do not commit real smoke JSON, source files, raw path, raw file content, local latest pointers, or sensitive notes.

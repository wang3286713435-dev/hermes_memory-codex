# Mac Mini Natural Import Operator Checklist

This checklist is for internal controlled MVP natural-language single-file import on Mac mini.

It is not production rollout approval, bulk import approval, Data Steward activation, repair authorization, cleanup authorization, or direct API upload evidence.

## 1. Operator Metadata

- Operator:
- Date / time:
- Session id:
- Source file path:
- Intended alias:
- User authorization reference:

## 2. Preflight

- Confirm the file is a single small non-sensitive file.
- Confirm the source path exists and is a regular file.
- Confirm file size and suffix are reasonable for a controlled MVP smoke.
- Confirm Hermes_memory API health is available.
- Confirm Hermes CLI is available.
- Confirm no cleanup, delete, repair, backfill, reindex, migration, or rollout is authorized.

## 3. Dry-run Evidence Template

Run the local dry-run helper before asking for real upload authorization:

```bash
uv run python scripts/phase257a_natural_import_evidence_template.py \
  --source-path "<file>" \
  --alias "<alias>" \
  --session-id "<session>" \
  --operator "<operator>"
```

Expected dry-run fields:

- `dry_run=true`
- `real_upload_called=false`
- `plain_upload_bypass_used=false`
- `cleanup_authorized=false`
- `repair_authorized=false`
- `backfill_authorized=false`
- `reindex_authorized=false`
- `rollout_authorized=false`
- `go_pause_no_go=ReadyForAuthorizedSmoke` or `Pause`

`ReadyForAuthorizedSmoke` only means the operator may request explicit authorization for a future real smoke. It is not upload success.

## 4. Dry-run Review

Review an existing evidence JSON before requesting real smoke authorization:

```bash
uv run python scripts/phase257a_natural_import_evidence_template.py \
  --review-json "<evidence-json>"
```

Expected review status:

- `ready_for_operator_authorization`: dry-run evidence is complete and no dangerous authorization flags are set.
- `pause`: required metadata is missing, real upload already occurred, or the record is not a clean dry-run authorization template.
- `no_go`: cleanup, repair, backfill, reindex, or rollout authorization appears in the record.

## 5. Real Natural Import Smoke

Only proceed after explicit user authorization.

The real smoke must use the Hermes CLI natural-language import path. A direct API upload is not valid evidence that natural-language import works.

Record at minimum:

- `document_id`
- `version_id`
- `chunk_count`
- `indexed_count`
- `alias`
- alias persisted in same session
- retrieval smoke returned document ids
- citation present
- third-document contamination status
- `metadata_as_answer=false`
- `facts_as_answer=false`
- `snapshot_as_answer=false`
- `transcript_as_fact=false`

## 6. Go / Pause / No-Go

### Go

- User explicitly authorized real smoke.
- Natural-language CLI import path was used.
- Upload returned document/version/chunk/index metadata.
- Alias persisted in the same session.
- Retrieval smoke returned only the imported document.
- Citation was visible.
- No metadata/facts/snapshot/transcript replaced retrieval evidence.

### Pause

- API or CLI unavailable.
- Evidence template missing required metadata.
- Authorization unclear.
- Alias did not persist.
- Retrieval smoke lacked citation.

### No-Go

- Direct API upload is used as substitute evidence.
- Cleanup, repair, backfill, reindex, delete, migration, or rollout is attempted.
- Third-document contamination appears.
- Output claims production readiness.

## 7. Storage Policy

Sanitized local run records may be saved under ignored internal MVP report paths. Do not commit real evidence JSON, source files, local latest pointers, or operator notes containing sensitive paths or business details.

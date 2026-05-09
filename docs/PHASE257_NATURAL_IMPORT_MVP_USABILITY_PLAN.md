# Phase 2.57 Natural Import MVP Usability / Evidence Plan

## 1. Goal

Phase 2.57 turns the Phase 2.56e technical proof into an internal MVP operating pattern for natural-language single-file import.

This phase is docs-only. It does not upload files, call the real upload API, write DB/index data, or enter rollout.

## 2. Current Baseline

- Hermes main commit: `be4b3a375`
- Hermes_memory commit: `7e07e4b`
- Tag: `phase-2.56e-natural-import-real-upload-smoke-baseline`
- Proven capability: a CLI natural-language import command can call the real Hermes_memory upload path, return document/version/chunk/index metadata, persist a session alias, and retrieve the new document in the same session.
- Proven smoke document:
  - `document_id=ee54b72c-b88b-4fad-be54-007240285356`
  - `version_id=950da5fe-dd7c-4eba-8764-916b556d14ce`
  - `chunk_count=1`
  - `indexed_count=1`

## 3. Natural Import MVP Operator Flow

1. Operator selects one small, non-sensitive file.
2. Operator confirms the file path, size, type, and that real import is authorized.
3. Operator checks Hermes_memory API health and Hermes CLI availability.
4. Operator enables real natural import explicitly:
   - `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true`
   - `HERMES_MEMORY_API_BASE_URL=http://127.0.0.1:8000`
5. Operator runs a natural-language import command through Hermes CLI.
6. The agent output must include `document_id`, `version_id`, `chunk_count`, `indexed_count`, and alias diagnostics.
7. In the same session, operator runs at least one alias retrieval smoke.
8. Operator saves a sanitized ignored run record under `reports/internal_mvp_runs/`.

Direct API upload is not acceptable as evidence for natural-language import success.

## 4. Evidence Pack Fields

- `source_path_exists`
- `source_file_size_bytes`
- `source_file_type`
- `api_health_status`
- `hermes_cli_available`
- `session_id`
- `import_command_sanitized`
- `natural_import_path_used`
- `plain_upload_bypass_used`
- `document_id`
- `version_id`
- `chunk_count`
- `indexed_count`
- `alias`
- `alias_persisted`
- `retrieval_smoke_passed`
- `returned_document_ids`
- `citation_present`
- `third_document_contamination`
- `metadata_as_answer=false`
- `facts_as_answer=false`
- `snapshot_as_answer=false`
- `transcript_as_fact=false`
- `cleanup_authorized=false`
- `repair_authorized=false`
- `backfill_authorized=false`
- `reindex_authorized=false`
- `rollout_authorized=false`

Evidence pack storage remains local and ignored by Git by default.

## 5. Go / Pause / No-Go

### Go

- API health is available.
- Hermes CLI is available.
- Natural import parser triggers.
- Real upload succeeds through the natural-language path.
- Required IDs and counts are present.
- Alias is persisted in the same session.
- Alias retrieval returns only the newly imported document.
- Citation is visible.
- No third-document contamination.
- Metadata, facts, snapshot, and transcript do not replace retrieval evidence.

### Pause

- API or CLI is unavailable.
- Parser does not trigger.
- Upload fails.
- Response lacks required IDs or counts.
- Alias is not persisted.
- Retrieval has no citation.
- Output cannot be recorded into an ignored sanitized run record.

### No-Go

- Someone bypasses natural import with plain upload and claims success.
- Cleanup, repair, backfill, reindex, delete, or migration is performed.
- Third-document evidence appears.
- Metadata, facts, snapshot, or transcript replaces retrieval evidence.
- The run is described as production rollout or Data Steward readiness.

## 6. Mac Mini Operator Runbook Outline

1. Confirm current baseline tag.
2. Confirm API health with `curl http://127.0.0.1:8000/health`.
3. Confirm Hermes CLI with `hermes chat --help`.
4. Confirm file is small and non-sensitive.
5. Confirm explicit user authorization for real import.
6. Run natural import command with feature flag enabled.
7. Copy required diagnostic fields into ignored run record.
8. Run alias retrieval smoke in the same session.
9. Mark Go / Pause / No-Go.
10. If Pause or No-Go, do not repair automatically; create or update issue intake.

Operators must not directly edit DB, OpenSearch, Qdrant, facts, versions, or audit logs.

## 7. Non-Goals

- No directory recursive scan.
- No NAS / TB / BIM file pool.
- No Data Steward / DB integration.
- No cleanup / delete / repair / backfill / reindex.
- No production rollout.
- No automatic issue creation.
- No automatic facts extraction.

## 8. Follow-Up Candidates

- Phase 2.57a: natural import evidence template / runbook runner dry-run. Completed implementation pending Codex B review.
- Phase 2.57b: second small-file real import validation, only with fresh explicit user authorization.
- Phase 2.58: Mac mini MVP operator checklist update for natural import.

## 9. Current Recommendation

Proceed to Codex B review. If accepted, baseline Phase 2.57 as docs-only planning.

## 10. Phase 2.57a Dry-run Evidence Template

Phase 2.57a adds `scripts/phase257a_natural_import_evidence_template.py`, a read-only local template generator for natural import evidence packs.

The runner only checks source file metadata with `Path.is_file()`, file size, file name, and suffix. It does not read file body content, upload files, call Hermes_memory API, call Hermes CLI, write DB/index data, or authorize cleanup/repair/backfill/reindex/rollout.

The dry-run output includes `dry_run=true`, `real_upload_called=false`, `plain_upload_bypass_used=false`, `cleanup_authorized=false`, `repair_authorized=false`, `backfill_authorized=false`, `reindex_authorized=false`, `rollout_authorized=false`, source metadata, alias, session id, operator, `go_pause_no_go`, missing fields, and required next steps.

`ReadyForAuthorizedSmoke` only means a future real natural-language CLI smoke has enough preflight metadata to ask for explicit user authorization. It is not upload success, production readiness, rollout readiness, or direct API upload evidence.

## 11. Phase 2.58 Natural Import Operator Pack

Phase 2.58 extends the dry-run template into an operator pack:

- `--review-json` reads an existing evidence template JSON and emits a sanitized review summary.
- Review mode is local and read-only; it does not upload, call API, call Hermes CLI, write DB/index data, or execute cleanup/repair/backfill/reindex.
- Review status can be `ready_for_operator_authorization`, `pause`, or `no_go`.
- Dangerous authorization flags such as cleanup, repair, backfill, reindex, or rollout force `no_go`.
- `real_upload_called=true` forces `pause` because review mode is meant for dry-run authorization templates, not post-upload success evidence.
- `docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md` provides the Mac mini operator checklist for preflight, authorization, evidence recording, and Go/Pause/No-Go.

Phase 2.58 still does not run real upload, API smoke, CLI smoke, Data Steward, DB/NAS/TB file pool, repair, or rollout.

# Phase 2.59 Natural Import Second Smoke Plan

## Goal

Plan a second controlled real natural-language file import smoke for the internal MVP.

This phase is planning-only. It does not upload files, call Hermes_memory API, run Hermes CLI, write DB/index data, or perform rollout.

## Authorization Gate

The second real smoke is blocked until all gate checks are true:

1. User provides one concrete small non-sensitive file path.
2. User explicitly authorizes a real natural-language import smoke for that file.
3. Phase 2.58 dry-run evidence template returns `ReadyForAuthorizedSmoke`.
4. Phase 2.58 `--review-json` returns `ready_for_operator_authorization`.
5. Operator confirms direct API upload will not be used as substitute evidence.
6. Operator confirms cleanup, delete, repair, backfill, reindex, migration, and rollout remain unauthorized.
7. Codex C owns the terminal validation and records Go / Pause / No-Go.

Until the gate is satisfied, this phase is planning-only and must not trigger upload, API smoke, CLI smoke, DB/index writes, or data cleanup.

## Execution Owner

Codex C should run the real terminal validation after authorization. Codex A should not auto-upload during planning or baseline phases.

Codex C should use `docs/NEXT_CODEX_C_PROMPT.md` as a pending authorization template. The template intentionally contains placeholders and must not be executed until the user replaces them with an authorized file path, alias, and operator.

## Authorized Execution Flow

1. Verify Hermes_memory API `/health`.
2. Verify Hermes CLI availability.
3. Preflight the authorized source path: exists, regular file, size, suffix.
4. Generate dry-run evidence with Phase 2.58 template.
5. Review the dry-run JSON with `--review-json`.
6. If review status is not `ready_for_operator_authorization`, stop at `Pause`.
7. Run the Hermes CLI natural-language import path in one session.
8. Capture `document_id`, `version_id`, `chunk_count`, and `indexed_count`.
9. Bind or verify the requested alias in the same session.
10. Run same-session retrieval using the alias.
11. Confirm returned document ids only include the new document.
12. Confirm citation is visible and safety flags remain false.
13. Save a sanitized run record only under an ignored reports path.
14. Report Go / Pause / No-Go without committing the real evidence JSON.

## Required Evidence

- API `/health` status.
- Hermes CLI availability.
- `session_id`.
- source file metadata: exists, size, suffix.
- dry-run template output summary.
- review-json output summary.
- natural import command used through Hermes CLI path.
- `document_id`, `version_id`, `chunk_count`, `indexed_count`.
- alias persistence status.
- same-session retrieval result ids.
- citation presence.
- third-document contamination status.
- safety flags: `metadata_as_answer=false`, `facts_as_answer=false`, `snapshot_as_answer=false`, `transcript_as_fact=false`.
- ignored sanitized run record path.
- confirmation that no direct API upload was used.
- confirmation that no cleanup, delete, repair, backfill, reindex, migration, or rollout was attempted.

## Go / Pause / No-Go

### Go

- Real natural import path succeeded through Hermes CLI.
- Required ids/counts are present.
- Alias persisted.
- Retrieval returns only the new document.
- Citation is visible.
- No third-document contamination.
- Safety flags remain false.

### Pause

- API or CLI unavailable.
- Parser does not trigger.
- Upload fails.
- Alias not persisted.
- Retrieval lacks citation.
- Run record cannot be saved.
- Dry-run template or `--review-json` is missing, incomplete, or not ready for authorization.

### No-Go

- Direct API upload is used as substitute evidence.
- Cleanup, delete, repair, backfill, reindex, migration, or rollout is attempted.
- DB/index mutation beyond the authorized upload occurs.
- Third-document contamination appears.
- Output claims production readiness.

## Non-goals

- No bulk upload.
- No directory or NAS scan.
- No TB/BIM file pool.
- No Data Steward / DB integration.
- No cleanup or repair of Phase 2.56e test records.
- No production rollout.
- No automatic issue creation.
- No claim that a second-file smoke equals production readiness.

## Artifact Policy

- Real source files are never committed.
- Real smoke evidence JSON remains ignored.
- `reports/internal_mvp_runs/` or another ignored report path may store sanitized local records.
- `docs/NEXT_CODEX_C_PROMPT.md` is the only committed handoff artifact for Codex C.
- If authorization is unclear, the test must stop before upload.

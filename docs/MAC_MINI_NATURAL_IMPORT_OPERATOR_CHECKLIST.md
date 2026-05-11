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

## 8. Second-file Smoke Authorization

Before any second real natural import smoke, run the dry-run evidence template and `--review-json` helper. Only request user authorization when the review status is `ready_for_operator_authorization`. Do not substitute direct API upload for the Hermes CLI natural-language path.

Second-file authorization flow:

1. Fill source path, alias, session id, and operator in the dry-run template.
2. Confirm `go_pause_no_go=ReadyForAuthorizedSmoke`.
3. Review the dry-run JSON and confirm `review_status=ready_for_operator_authorization`.
4. Ask the user to authorize the concrete file path; do not infer authorization from previous smoke runs.
5. Hand off to Codex C using `docs/NEXT_CODEX_C_PROMPT.md`.
6. During real smoke, record whether returned document ids contain only the newly imported document.
7. If any Pause / No-Go condition appears, stop without cleanup, repair, backfill, reindex, or rollout.

The second-file smoke should produce an ignored sanitized run record. Real evidence JSON and source files must remain untracked.

## 9. Internal MVP Launch Readiness

Before internal controlled MVP use, run the Phase 2.60 local readiness pack:

```bash
uv run python scripts/phase260_mvp_local_readiness_pack.py --skip-api-health
```

If the API should be checked and is already running:

```bash
uv run python scripts/phase260_mvp_local_readiness_pack.py \
  --api-url http://127.0.0.1:8000
```

Readiness output is a dry-run gate only:

- `go`: internal controlled MVP use may proceed under human operator supervision.
- `pause`: fix prerequisites and rerun; do not upload or repair automatically.
- `no_go`: stop for Codex B / human owner review.

This runner does not start services, upload files, run Hermes CLI smoke, write DB/index state, execute repair, or approve production rollout.

## 10. Issue Intake After Internal MVP Use

When internal controlled MVP use exposes an issue, create a local issue template:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py \
  --new-template \
  --output-json /tmp/hermes_issue_template.json
```

After filling the local JSON, validate and summarize it:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py \
  --input-json /tmp/hermes_issue_template.json
```

To summarize multiple ignored local issue records for Codex B review:

```bash
uv run python scripts/phase262_mvp_issue_triage_summary.py \
  --input-dir reports/internal_mvp_issues
```

The Phase 2.62 summary is read-only and redacts raw query text, notes, local full paths, expected behavior, and actual behavior from shareable issue refs.

The issue intake helper is dry-run and read-only. It does not upload files, create external issues, write DB/index state, repair data, or approve rollout.

Escalation guide:

- `no_go`: stop affected workflow and send to Codex B / human owner.
- `pause`: request Codex B triage before continuing that workflow.
- `ready`: keep the issue for Codex B review while continuing controlled use if Phase 2.60 readiness remains `go`.

## 11. Daily Operator Summary

After one day of internal controlled MVP use, summarize local issue records with the Phase 2.63 daily summary runner:

```bash
uv run python scripts/phase263_mvp_operator_daily_summary.py \
  --input-dir reports/internal_mvp_issues \
  --output-json /tmp/hermes_daily_summary.json \
  --output-md /tmp/hermes_daily_summary.md
```

The daily summary is read-only. It produces `ready`, `pause`, or `no_go` for operator / Codex B review.

The Markdown output is sanitized and must not include raw query text, notes, expected / actual behavior, local full paths, returned document ids, or evidence chunk ids.

Daily decision guide:

- `no_go`: stop affected workflow and require human owner / Codex B review.
- `pause`: continue only with manual review; do not treat the day as production-ready.
- `ready`: continue controlled MVP use and keep recording new local issues.

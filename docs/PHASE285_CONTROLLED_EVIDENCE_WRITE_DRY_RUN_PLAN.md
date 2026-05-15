# Phase 2.85 Controlled Evidence Write Dry-run Plan

## 1. Goal

Phase 2.85 plans the next safe step toward making NAS-derived content queryable by Hermes.

This phase only defines a future controlled evidence-write dry-run design. It does not implement a writer and does not execute any evidence write.

The future dry-run must prove that a reviewed `nas_evidence_write_preflight.v0` report can be transformed into deterministic simulated document/chunk records without touching production stores.

## 2. Current Baseline

Phase 2.84a is complete:

1. commit: `a006df3`
2. tag: `phase-2.84a-evidence-write-preflight-dry-run-baseline`
3. pushed: true

The available local preflight evaluator can read an ignored local payload plan and explicit operator approval JSON, then produce an ignored local `nas_evidence_write_preflight.v0` report.

The preflight state `write_preflight_ready_for_dry_run` still is not write authorization.

## 3. Non-Negotiable Boundary

Phase 2.85 does not:

1. write `documents`
2. write `chunks`
3. write platform DB or Hermes DB
4. write OpenSearch
5. write Qdrant
6. write MinIO
7. execute parser
8. copy real files
9. read raw file contents
10. scan NAS
11. run Agent DB / NAS CRUD
12. integrate with Agent final answers
13. treat manifest / eligibility / payload / preflight / future write-dry-run artifacts as production evidence
14. run repair / cleanup / backfill / reindex / delete / migration
15. enter production rollout

## 4. Inputs for Future Phase 2.85a

The future dry-run runner may accept only explicit local inputs:

1. ignored local `nas_evidence_write_preflight.v0` report
2. preflight state exactly `write_preflight_ready_for_dry_run`
3. explicit operator approval for write-dry-run scope
4. feature flags default off
5. deterministic run id or operator-provided dry-run id
6. optional fixed timestamp for reproducible tests

The runner must reject:

1. missing preflight report
2. preflight state other than `write_preflight_ready_for_dry_run`
3. approval mismatch
4. ambiguous write scope
5. payload / preflight artifacts that contain scratch paths, true file names, raw NAS paths, raw text, secrets, or unredacted business values
6. any request that attempts real DB, index, object-store, parser, copy, NAS scan, or Agent answer work

## 5. Future Dry-run Write Model

The future implementation should use one of two local-only stores:

1. in-memory repository for unit tests
2. local temp SQLite database under an ignored temp directory

The dry-run store may simulate:

1. candidate document rows
2. candidate chunk rows
3. citation rows
4. idempotency rows
5. rollback ledger rows

The dry-run store must not reuse the real Hermes DB connection and must not call production repository methods.

It must also avoid OpenSearch, Qdrant, MinIO, platform DB, real Hermes DB, parser, file copy, raw content read, NAS scan, and Agent answer integration.

## 6. Future Simulated Document / Chunk Shape

Each simulated document should include:

1. `simulated_document_ref`
2. `external_asset_ref`
3. `source_catalog_ref`
4. `source_preflight_report_id`
5. `operator_approval_ref`
6. `document_type`
7. `source_type`
8. `redacted_title_hint`
9. `candidate_version_ref`
10. `idempotency_key`
11. `write_dry_run_id`
12. `created_in_dry_run=true`

Each simulated chunk should include:

1. `simulated_chunk_ref`
2. `simulated_document_ref`
3. `candidate_chunk_index`
4. `redacted_citation_anchor`
5. `source_catalog_ref`
6. `source_preflight_item_ref`
7. `source_payload_item_ref`
8. `source_manifest_item_ref`
9. `idempotency_key`
10. `write_dry_run_id`
11. `created_in_dry_run=true`

The simulated records must not include:

1. scratch path
2. true file name
3. raw NAS path
4. raw file text
5. secrets
6. raw DB row
7. sensitive business values

## 7. Deterministic References

The future dry-run must derive deterministic references from sanitized inputs only.

Recommended deterministic references:

1. `external_asset_ref = sha256(project_scope + asset_ref + source_catalog_ref)`
2. `simulated_document_ref = sha256(write_scope + external_asset_ref + candidate_version_ref)`
3. `simulated_chunk_ref = sha256(simulated_document_ref + candidate_chunk_index + redacted_citation_anchor)`
4. `idempotency_key = sha256(preflight_report_id + operator_approval_ref + write_scope + external_asset_ref)`

These references are local simulation identifiers. They do not become production document ids.

## 8. Idempotency and Duplicate Protection

The future dry-run must guarantee:

1. retrying the same input produces the same simulated refs
2. retrying the same input does not create duplicate simulated records
3. duplicate payload / preflight attempts are detected by idempotency key
4. conflicting input with the same idempotency key becomes `write_dry_run_no_go`
5. a dry-run can report `already_simulated` without writing duplicates

The dry-run output should include:

1. `items_total`
2. `items_simulated`
3. `duplicates_detected`
4. `idempotency_conflicts`
5. `decision`

## 9. Rollback Dry-run

Rollback remains simulated only.

Future rollback dry-run may delete or mark only simulated records created by the same local `write_dry_run_id` inside the local temp store.

Rollback dry-run must never:

1. delete NAS files
2. delete platform DB records
3. delete Hermes DB rows
4. delete OpenSearch documents
5. delete Qdrant points
6. delete MinIO objects
7. run repair / cleanup / backfill / reindex

Rollback output should list simulated refs that would be removed from the local dry-run store only.

## 10. Citation / Evidence Boundary

The future dry-run output is not production evidence.

It may show:

1. simulated document refs
2. simulated chunk refs
3. redacted citation anchors
4. source asset refs
5. preflight item refs

It must not be used as:

1. Agent final answer citation
2. retrieval evidence
3. production document metadata
4. proof that NAS content is queryable
5. proof that parser output exists

Future real evidence write requires a separate Phase and explicit authorization.

Agent answer integration remains later than the first controlled real write smoke.

## 11. Feature Flags

All future write-dry-run execution flags must default off.

Suggested flags:

1. `PLATFORM_ASSET_EVIDENCE_WRITE_DRY_RUN_ENABLED=false`
2. `PLATFORM_ASSET_EVIDENCE_WRITE_REAL_ENABLED=false`
3. `PLATFORM_ASSET_EVIDENCE_WRITE_AGENT_ANSWER_ENABLED=false`

The future runner must require the dry-run flag plus explicit operator approval. The real write flag must remain unused in Phase 2.85a.

## 12. Go / Pause / No-Go

### Go

For Phase 2.85, Go means planning is complete only.

For future Phase 2.85a, a dry-run Go may mean:

1. input preflight state is ready
2. operator approval matches
3. simulated records were created in local temp / in-memory store
4. idempotency passed
5. rollback dry-run is available
6. no real writes occurred

It still does not authorize real writes.

### Pause

Pause if:

1. preflight contract details are missing
2. write scope is ambiguous
3. rollback behavior is unclear
4. idempotency key is unclear
5. citation anchor is missing or ambiguous
6. feature flag / approval semantics are unclear

### No-Go

No-Go if any plan or future implementation implies:

1. real `documents/chunks` writes
2. parser execution
3. NAS scan
4. file copy
5. raw content read
6. DB CRUD
7. OpenSearch / Qdrant / MinIO write
8. repair / cleanup / backfill / reindex
9. production rollout
10. Agent final answer integration

## 13. Future Phase Split

1. Phase 2.85a: implement local temp SQLite / in-memory evidence write dry-run runner.
2. Phase 2.86: plan controlled small-batch real Hermes evidence write.
3. Phase 2.86a or later: run real write smoke only after explicit authorization.
4. Agent answer integration remains later than the first real write smoke.

Phase 2.85a must still avoid real Hermes DB, OpenSearch, Qdrant, MinIO, parser, file copy, NAS scan, and Agent answer integration.

## 14. Review Checklist

Before Phase 2.85a implementation starts, Codex B should confirm:

1. no real write path is implied
2. local-only repository boundary is explicit
3. deterministic refs are sufficient for idempotency
4. rollback dry-run cannot touch real systems
5. citation anchors remain redacted
6. artifacts remain ignored
7. feature flags default off
8. future Go does not mean production evidence or answerability

## 15. Phase 2.85 Conclusion

Phase 2.85 defines the controlled evidence-write dry-run design and future safety gates.

It does not implement the runner and does not execute any evidence write.

Recommended next action: Codex B review this plan, then either baseline Phase 2.85 docs or authorize Phase 2.85a as a separate bounded implementation phase.

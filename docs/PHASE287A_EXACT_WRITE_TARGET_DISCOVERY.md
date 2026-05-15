# Phase 2.87a Exact Write Target Discovery

## 1. Goal and Baseline

Phase 2.87a is a docs-only / read-only discovery pass for the first future real Hermes evidence write smoke.

Baseline:

1. Phase 2.87 commit: `069fbec`
2. Phase 2.87 tag: `phase-2.87-first-real-evidence-write-smoke-plan-baseline`
3. pushed: true

This phase identifies candidate SQLAlchemy models, tables, and service boundaries. It does not implement a writer and does not execute any real write.

## 2. Read-only Inspection Method

Read-only inspection covered:

1. `app/models/document.py`
2. `app/models/chunk.py`
3. `app/models/citation.py`
4. `app/models/audit.py`
5. `app/models/ingestion.py`
6. `app/models/__init__.py`
7. `app/services/ingestion/service.py`
8. `app/services/indexing/opensearch.py`
9. `app/services/indexing/dense.py`
10. `app/services/citation/service.py`
11. `app/api/routes/documents.py`
12. `migrations/versions/0001_phase1_core_schema.py`
13. ingestion / structured-file / version-governance tests

Commands used included `rg` and `sed`. No runtime service, parser, DB, OpenSearch, Qdrant, MinIO, NAS, file-copy, or Agent action was executed.

## 3. Candidate Write Targets

### 3.1 Evidence tables

Future DB evidence write candidates are:

| Purpose | Model | Table | File |
|---|---|---|---|
| document shell | `Document` | `documents` | `app/models/document.py` |
| document version | `DocumentVersion` | `document_versions` | `app/models/document.py` |
| evidence chunk | `Chunk` | `chunks` | `app/models/chunk.py` |
| citation / lineage row | `CitationRecord` | `citations` | `app/models/citation.py` |
| optional ingestion bookkeeping | `IngestionJob` | `ingestion_jobs` | `app/models/ingestion.py` |

The first smoke should not write `AuditLog` / `audit_logs`; audit writes remain a non-target unless a later phase explicitly authorizes them.

### 3.2 Existing service methods

Existing write path:

1. `DocumentIngestionService.ingest_uploaded_file()` in `app/services/ingestion/service.py`
2. `DocumentIngestionService._mark_previous_versions_superseded()`
3. `DocumentIngestionService._restore_previous_versions()`
4. `DocumentIngestionService._index_chunks()`
5. `DocumentIngestionService._index_dense_chunks()`
6. `OpenSearchChunkIndexer.index_chunk()`
7. `DenseChunkIndexer.index_chunks()`
8. direct `db.add(...)`, `db.flush()`, and `db.commit()` calls for `Document`, `DocumentVersion`, `Chunk`, and `CitationRecord`

This path is not safe to reuse directly for Phase 2.87b because it reads file bytes, invokes parser/chunker, may write OpenSearch / Qdrant, and is designed around uploaded files rather than sanitized NAS-derived evidence payloads.

## 4. Transaction Boundary Proposal

Safest future boundary:

1. open one SQLAlchemy session transaction
2. resolve or create one `Document`
3. create one `DocumentVersion`
4. create at most 20 `Chunk` records
5. create matching `CitationRecord` rows
6. flush and validate row counts
7. commit only if all DB evidence rows and run-scoped metadata pass validation

The transaction must not call parser, storage, OpenSearch, Qdrant, MinIO, or audit writers.

Recommended future implementation shape:

1. new dedicated evidence-only service, not `ingest_uploaded_file()`
2. explicit input from approved sanitized payload / preflight / rehearsal artifacts
3. injected session
4. no external side effects
5. a single commit after all records are staged

## 5. Idempotency Key Proposal

The future smoke should use a deterministic idempotency key derived from:

1. source system
2. source asset ref
3. project scope
4. platform contract version
5. sanitized manifest ref
6. payload plan ref
7. preflight report ref
8. rehearsal ref
9. operator approval id
10. write run id

Current tables do not expose a dedicated idempotency-key column for smoke evidence writes.

Pause blocker before real execution:

1. decide where the idempotency key is persisted, likely `DocumentVersion.metadata_json` and / or `Document.metadata_json`
2. define duplicate detection query
3. define conflict behavior when same key maps to different payload fingerprint

## 6. Rollback / Invalidation Proposal

Existing related behavior:

1. `DocumentVersion` has `is_latest`, `expired_at`, and `metadata_json.version_status`.
2. `DocumentIngestionService._restore_previous_versions()` can restore previously latest versions after ingestion failure.
3. `DocumentIngestionService._mark_previous_versions_superseded()` handles version state changes for normal uploads.

No dedicated run-scoped rollback / invalidation service exists for a successfully committed evidence smoke.

Pause blocker before real execution:

1. define a smoke run id in `metadata_json`
2. provide a future dry-run rollback plan that can identify only rows created by that smoke run
3. define whether rollback deletes rows or marks `Document.status` / `DocumentVersion.metadata_json.version_status` as smoke-invalid
4. prove rollback cannot touch NAS files, platform rows, OpenSearch docs, Qdrant points, MinIO objects, audit rows, or unrelated Hermes records

## 7. Non-targets

Phase 2.87b must continue to exclude:

1. platform DB writes
2. OpenSearch writes
3. Qdrant writes
4. MinIO writes
5. audit table writes
6. NAS scan / copy / delete / cleanup
7. parser execution
8. Agent answer integration
9. Agent DB / NAS CRUD
10. repair / backfill / reindex / migration
11. production rollout

## 8. Pause Blockers

Direct real write remains `Pause` until these are resolved:

1. no dedicated evidence-only repository / service method exists
2. existing ingestion path is coupled to parser, file bytes, storage, OpenSearch, and Qdrant
3. no run-scoped rollback / invalidation method exists for a committed smoke run
4. no explicit idempotency column or canonical metadata location has been fixed
5. exact future `metadata_json` fields for source asset ref, permission proof ref, approval id, and write run id are not yet specified
6. citation lineage must be mapped from sanitized payload fields without raw path, true filename, or raw text output

## 9. Go / Pause / No-Go

### Go

Go for this Phase 2.87a discovery means the candidate evidence models and unsafe reuse boundaries have been identified for Codex B review.

### Pause

Pause for direct Phase 2.87b real write execution.

Phase 2.87b may be planned only as a tiny implementation phase that first introduces a dedicated evidence-only writer service, explicit idempotency metadata, and run-scoped rollback dry-run checks.

### No-Go

No-Go if a later prompt attempts to reuse `DocumentIngestionService.ingest_uploaded_file()` directly for NAS-derived evidence smoke, because that would risk parser, file, storage, OpenSearch, or Qdrant side effects.

No-Go also applies to any request that writes audit tables, platform DB, index stores, object stores, NAS, or Agent answer context in the same phase.

## 10. Follow-up Recommendation

Recommended next step:

1. Codex B review this discovery.
2. If accepted, baseline this docs-only discovery.
3. Then plan Phase 2.87b as a tiny test-machine implementation prompt for an evidence-only DB writer service.

Phase 2.87b still must not automatically execute the real write. It should implement and test the writer behind explicit feature flags and operator approval checks, then stop for review before any runtime smoke.

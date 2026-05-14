# Phase 2.82 Evidence Write Eligibility Planning

## Summary

Phase 2.82 defines the review gates for any future NAS-derived parser preview to become eligible for a later evidence-write phase.

This phase is planning only. It does not write `documents`, `chunks`, OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB. It does not run parser, copy files, read raw content, connect to NAS, or connect manifests to Agent final answers.

## Background

Phase 2.81a added a sanitized evidence manifest dry-run:

1. `nas_evidence_manifest.v0` can be generated from sanitized parser-preview metadata.
2. Forbidden raw fields are rejected.
3. Unsafe write / Agent answer flags produce `no_go`.
4. Manifest artifacts remain ignored local outputs.

The next risk is semantic drift: a review manifest could be mistaken for document evidence. Phase 2.82 prevents that by defining explicit eligibility gates before any future write phase.

## Design Options Considered

### Option A: Review-only Eligibility Matrix

Define a strict checklist for future evidence-write planning, but do not implement writes.

Pros:

1. Preserves current safety boundary.
2. Lets database / NAS integration continue without rushing indexing.
3. Makes future Phase 2.82a / 2.83 implementation auditable.

Cons:

1. Does not yet make NAS content answerable by Agent.

Decision: adopt Option A.

### Option B: Immediate Evidence Write Dry-run Runner

Implement a runner that transforms manifests into candidate `documents/chunks` payloads without writing them.

Pros:

1. Faster path toward Agent answer integration.

Cons:

1. Still too close to evidence mutation semantics.
2. Requires more complete citation / chunking contracts.
3. Risks confusing review artifacts with prompt evidence.

Decision: defer.

### Option C: Full NAS Content Indexing

Write parsed content to documents/chunks and indexes.

Pros:

1. Directly enables Agent answers from NAS content.

Cons:

1. Premature without eligibility, human approval, permission proof, and citation contracts.
2. High blast radius if wrong.

Decision: explicitly forbidden in this phase.

## Eligibility States

Future dry-run tools should classify each manifest into one of:

1. `not_eligible`
2. `eligible_for_human_review`
3. `eligible_for_evidence_write_planning`
4. `no_go`

No state in Phase 2.82 authorizes actual writes.

## Required Gates

An item can be `eligible_for_evidence_write_planning` only if all gates pass:

1. `manifest_version` is supported.
2. `decision.manifest_status=ready_for_review`.
3. `source.project_scope_proven=true`.
4. `source.permission_proof_status=valid`.
5. `source.storage_locator_present=true`.
6. Parser status is `parsed`.
7. Text length bucket is not `empty` or `unknown`.
8. Cleanup status is `all_deleted`.
9. All safety write flags remain false.
10. No raw text, true filename, true NAS path, raw DB row, secret, or sensitive business value is present.
11. `index_eligibility_status=eligible_for_preview`.
12. `confidentiality_status=known`.
13. `lifecycle_status=active`.
14. File type is in a future approved text-capable allowlist.
15. A human reviewer explicitly approves evidence-write planning.

If any gate is missing, the result must be `not_eligible` or `eligible_for_human_review`, not an implicit approval.

## Permission Boundary

`permission_tags` are not final authorization.

Future eligibility must require REST/API Key `project_scope` or equivalent permission proof. Missing proof defaults to `DENIED`.

## Citation Boundary

Future evidence-write planning must preserve source traceability:

1. `source_view`.
2. Redacted or hashed asset reference.
3. Contract version.
4. Checksum / hash presence.
5. Parser type.
6. Sanitized structure summary.
7. Cleanup status.

It must not cite scratch paths or temporary local filenames.

## Human Review Boundary

The reviewer may approve only the next planning phase, not production write.

Allowed review decisions:

1. `approve_for_evidence_write_planning`.
2. `needs_more_metadata`.
3. `reject_sensitive_or_unsafe`.
4. `reject_unsupported_type`.
5. `reject_permission_unclear`.

The word `approved` must not mean written, indexed, or answerable.

## Future Phase 2.82a Candidate

If separately authorized, Phase 2.82a may implement a local dry-run eligibility evaluator:

1. Input: ignored local sanitized manifest JSON.
2. Output: ignored local eligibility report.
3. Writes: no DB, no documents/chunks, no indexes, no object store.
4. Agent answer integration: false.
5. Parser execution: false.
6. Real file copy: false.

## Still Forbidden

1. Writing `documents`.
2. Writing `chunks`.
3. Writing OpenSearch.
4. Writing Qdrant.
5. Writing MinIO.
6. Writing platform DB or Hermes DB.
7. Running parser.
8. Copying real files.
9. Reading raw file contents.
10. Scanning NAS.
11. Agent DB / NAS CRUD.
12. Agent final answer integration.
13. Treating manifest as document evidence.
14. Repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## Current Conclusion

Phase 2.82 keeps Hermes on the safe bridge between “parser dry-run preview exists” and “future evidence write may be planned.”

It does not yet make NAS content answerable by the Agent.


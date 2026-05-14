# Phase 2.83 Evidence Write Payload Contract Planning

## Summary

Phase 2.83 plans the contract for a future dry-run payload that could describe candidate `documents` / `chunks` writes from sanitized NAS parser previews.

This phase is planning only. It does not generate payload artifacts, write `documents`, write `chunks`, write OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB. It does not run parser, copy files, read raw content, scan NAS, or connect payloads to Agent final answers.

## Background

Phase 2.82a added a local eligibility evaluator:

1. Input: ignored local `nas_evidence_manifest.v0`.
2. Output: ignored local `nas_evidence_write_eligibility.v0`.
3. Output states include `eligible_for_evidence_write_planning`.
4. No state authorizes actual writes.

The next risk is payload drift: once an item is eligible for planning, a candidate payload could be mistaken for actual document evidence. Phase 2.83 prevents that by defining a contract before implementing any payload dry-run tool.

## Design Options Considered

### Option A: Payload Contract Only

Define the schema, citation requirements, chunking assumptions, dry-run status, and forbidden side effects.

Pros:

1. Keeps current safety boundary.
2. Makes future Phase 2.83a implementation testable.
3. Gives database / NAS work a clear bridge without writing evidence.

Cons:

1. Still does not make NAS content answerable by the Agent.

Decision: adopt Option A.

### Option B: Immediate Payload Dry-run Runner

Implement a runner that transforms eligible reports into candidate payload JSON.

Pros:

1. Faster path toward future content ingestion.

Cons:

1. Requires more schema decisions before review.
2. Risks treating dry-run payloads as writes.
3. Needs stronger citation and chunk provenance constraints first.

Decision: defer to a separately authorized Phase 2.83a.

### Option C: Actual Evidence Write

Write NAS-derived content into `documents` / `chunks` and indexes.

Pros:

1. Directly enables Agent answers over NAS content.

Cons:

1. Too much blast radius without payload contract, chunk IDs, write approval, rollback plan, and operator review.
2. Premature before small-batch end-to-end validation.

Decision: explicitly forbidden.

## Future Payload Contract

A future dry-run payload should use a versioned schema:

```text
nas_evidence_write_payload.v0
```

Top-level fields:

1. `payload_version`
2. `run_id`
3. `created_at`
4. `source`
5. `eligibility`
6. `candidate_document`
7. `candidate_chunks`
8. `citation_contract`
9. `safety`
10. `dry_run`
11. `decision`

## Source Requirements

The payload source must include only sanitized identifiers:

1. Redacted or hashed asset reference.
2. `source_view`.
3. Platform contract version.
4. Manifest run id.
5. Eligibility report run id.
6. Parser type.
7. Hash / checksum presence.
8. Cleanup status.

It must not include true filenames, NAS paths, scratch paths, raw DB rows, or raw business values.

## Candidate Document Contract

A future candidate document payload may describe:

1. `external_source_type=platform_asset_catalog`
2. Redacted external asset reference.
3. Sanitized title placeholder.
4. Source view and contract version.
5. File type.
6. Parser type.
7. Permission proof status.
8. Confidentiality status.
9. Lifecycle status.
10. Index eligibility status.

It must not contain raw text or true source paths.

## Candidate Chunk Contract

A future candidate chunk payload may describe sanitized chunk metadata:

1. Deterministic dry-run chunk reference.
2. Text length bucket.
3. Page / sheet / slide / row bucket when available.
4. Parser section label when sanitized.
5. Redacted citation anchor.
6. Chunk order.

It must not contain raw extracted text in Phase 2.83 planning. Raw content handling requires a separate write-phase design and explicit authorization.

## Citation Contract

Future writes must preserve traceability without exposing temporary paths:

1. Cite DB asset reference, not scratch path.
2. Include source view and platform contract version.
3. Include parser type and sanitized structure summary.
4. Include checksum / hash presence.
5. Include cleanup status.
6. Include permission proof status.

Agent answers must not cite eligibility report filenames or scratch-local filenames.

## Decision States

Future payload planning may classify an item as:

1. `payload_not_allowed`
2. `payload_ready_for_human_review`
3. `payload_ready_for_write_dry_run`
4. `payload_no_go`

No state authorizes DB / index writes.

## Required Gates Before Future Phase 2.83a

A future payload dry-run can only proceed if:

1. Eligibility state is `eligible_for_evidence_write_planning`.
2. Eligibility report safety flags are all false.
3. Human reviewer approves payload dry-run planning.
4. Payload schema version is known.
5. Citation contract can be satisfied.
6. Chunk metadata can be produced without raw text exposure.
7. Rollback / cleanup plan is documented.
8. All artifacts remain ignored local outputs.

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
13. Treating manifest, eligibility report, or payload plan as document evidence.
14. Repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## Future Phase 2.83a Candidate

If separately authorized, Phase 2.83a may implement a local payload dry-run builder:

1. Input: ignored local eligibility report JSON.
2. Output: ignored local payload plan JSON.
3. Writes: no DB, no `documents/chunks`, no indexes, no object store.
4. Agent answer integration: false.
5. Parser execution: false.
6. Real file copy: false.
7. Raw text output: false.

## Current Conclusion

Phase 2.83 keeps Hermes on the bridge from “eligible for evidence-write planning” to “future payload dry-run design.”

It still does not make NAS content answerable by the Agent.

# Phase 2.86 Controlled Real Hermes Evidence Write Plan

## 1. Goal

Phase 2.86 defines the safety boundary for a future tiny, operator-approved, test-machine-only real Hermes evidence write smoke.

This phase is planning-only. It does not implement a writer and does not execute any real evidence write.

The purpose is to make the first possible real write small, auditable, reversible in plan, and clearly separated from parser execution, indexing, Agent answer integration, and rollout.

## 2. Current Baseline

Phase 2.85a is complete:

1. commit: `380e7a0`
2. tag: `phase-2.85a-evidence-write-dry-run-baseline`
3. pushed: true

The current runner can transform an ignored local `nas_evidence_write_preflight.v0` report into an ignored local `nas_evidence_write_dry_run.v0` report.

The dry-run output is not production evidence and does not authorize real writes.

## 3. Scope

A future first real write smoke must be limited to a test machine and a tiny explicit sample:

1. at most 1 source asset
2. at most 1 Hermes document version
3. at most 20 chunks
4. one explicit operator-approved write run
5. one deterministic rollback dry-run plan before the write

It is not:

1. production rollout
2. broad NAS ingestion
3. full project import
4. background sync
5. parser expansion
6. index write
7. Agent answer integration

## 4. Prerequisite Chain

A future real write smoke may be planned only after the following chain is complete and reviewable:

1. valid project-scope permission proof
2. controlled scratch copy smoke passed
3. parser dry-run passed
4. sanitized evidence manifest ready
5. evidence-write eligibility report ready
6. evidence-write payload dry-run ready
7. evidence-write preflight ready
8. evidence-write dry-run ready
9. explicit operator approval for a real write smoke

Each prerequisite must reference ignored local artifacts or committed planning documents without exposing raw NAS paths, true file names, raw text, secrets, raw DB rows, or sensitive business values.

## 5. Feature Flags

All future real-write flags default off:

```env
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=false
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=false
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED=false
```

Flags alone are insufficient. A future write smoke also requires explicit operator approval that matches:

1. source asset reference
2. project scope
3. permission proof reference
4. approved document / chunk limit
5. target write run id
6. rollback dry-run reference

## 6. Write Target Boundary

The first future write smoke may target only Hermes evidence tables that are explicitly approved in a later implementation phase.

Until that later phase names the exact tables and repository methods, the default allowed write target set is empty.

The future smoke must not write:

1. platform DB
2. OpenSearch
3. Qdrant
4. MinIO
5. audit tables
6. any production rollout state

It must not run:

1. repair
2. source cleanup
3. backfill
4. reindex
5. delete
6. migration
7. parser execution
8. NAS scan
9. Agent DB / NAS CRUD

## 7. Citation and Metadata Boundary

Every future candidate document / chunk must retain enough lineage to be auditable:

1. DB asset reference
2. source view name
3. platform contract version
4. permission proof reference
5. sanitized parser metadata reference
6. checksum / version link
7. original storage locator reference as a redacted reference, not a raw path
8. evidence manifest item reference
9. payload item reference
10. preflight item reference

Future answers may cite only DB asset / Hermes document evidence after that evidence exists.

They must never cite:

1. local scratch path
2. raw NAS path
3. true filename
4. raw parser preview
5. dry-run simulated chunk
6. eligibility / payload / preflight artifact as if it were document evidence

Committed docs must not contain raw NAS path, true filename, raw text preview, secret, raw DB row, or sensitive business value.

## 8. Idempotency, Lock, and Rollback

Future write keys must be deterministic and derived only from sanitized references.

Suggested key inputs:

1. project scope
2. source system
3. asset reference
4. source view
5. contract version
6. checksum / content version reference
7. permission proof reference
8. operator approval reference
9. write run id

The future implementation must provide:

1. same-run duplicate detection
2. retry-safe idempotency keys
3. conflict detection for mismatched inputs
4. explicit write lock or single-run guard
5. rollback dry-run before any real write
6. cleanup plan if a future smoke partially fails

Rollback planning must identify exactly which future records would be removed or marked invalid. It must not delete NAS files, platform rows, OpenSearch documents, Qdrant points, MinIO objects, or unrelated Hermes records.

## 9. Go / Pause / No-Go

### Go

For Phase 2.86, Go means this planning document is ready for Codex B review.

For a future real write phase, Go requires a separate prompt and explicit operator authorization. It may mean only that one tiny test-machine write smoke is allowed within the approved scope.

### Pause

Pause if:

1. permission proof is missing or ambiguous
2. project scope is absent
3. test-machine ref is dirty
4. platform contract version is stale
5. sanitized artifacts contain unsafe fields
6. checksum / version link is missing
7. rollback dry-run is missing
8. cleanup proof is missing
9. feature flags are unclear
10. operator approval does not match scope

### No-Go

No-Go if any plan, implementation, or operator request implies:

1. unauthorized write
2. OpenSearch / Qdrant / MinIO mutation
3. platform DB write
4. audit table write without a separate phase
5. raw NAS path output
6. true filename output
7. raw DB row output
8. raw text preview output
9. secret output
10. repair / cleanup / backfill / reindex / delete / migration
11. Agent answer integration
12. production rollout

## 10. Proposed Follow-up Phases

1. Phase 2.86a: local / temp repository write rehearsal if Codex B decides another rehearsal is needed.
2. Phase 2.87: first test-machine real Hermes evidence write smoke, only after explicit operator approval.
3. Phase 2.88: optional index write planning after DB evidence write is verified.
4. Phase 2.89: Agent answer integration planning after evidence, citations, and governance checks are verified.

No follow-up phase is authorized by this document alone.

## 11. Review Checklist

Before any future implementation, Codex B should confirm:

1. the scope is still one source asset / one version / at most 20 chunks
2. the exact write target tables are named
3. operator approval is explicit and scoped
4. feature flags remain default off
5. lineage and citation metadata are complete
6. rollback dry-run exists before real write
7. dry-run artifacts are not treated as evidence
8. no index / object-store / platform DB / audit write is implied
9. no Agent answer integration is implied
10. committed docs contain no raw paths, raw text, secrets, raw rows, or true filenames

## 12. Phase 2.86 Conclusion

Phase 2.86 completes planning for a future controlled small-batch real Hermes evidence write smoke.

It does not implement or execute that write.

Recommended next action: Codex B review this plan. If accepted, perform a docs-only baseline. Do not enter Phase 2.86a or Phase 2.87 without a separate explicit prompt.

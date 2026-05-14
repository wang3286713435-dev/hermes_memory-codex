# Phase 2.84 Controlled Evidence Write Preflight Planning

## Summary

Phase 2.84 plans the final preflight gates required before any future NAS-derived dry-run payload can be considered for a controlled `documents` / `chunks` write phase.

This phase is planning only. It does not execute a write preflight runner, write `documents`, write `chunks`, write OpenSearch, Qdrant, MinIO, platform DB, or Hermes DB. It does not run parser, copy files, read raw content, scan NAS, or connect payloads to Agent final answers.

## Background

Phase 2.83a added a local payload dry-run builder:

1. Input: ignored local `nas_evidence_write_eligibility.v0`.
2. Output: ignored local `nas_evidence_write_payload.v0`.
3. Output can reach `payload_ready_for_write_dry_run`.
4. No state authorizes actual writes.

The next risk is operational: a dry-run payload could be mistaken for permission to write evidence. Phase 2.84 defines the last preflight contract before any write-capable implementation is considered.

## Design Options Considered

### Option A: Write Preflight Contract Only

Define the required approvals, locks, idempotency, rollback, batch limits, and citation coverage checks.

Pros:

1. Keeps current safety boundary.
2. Makes a future Phase 2.84a preflight runner testable.
3. Lets the project advance toward usable NAS evidence without prematurely writing data.

Cons:

1. Still does not make NAS content answerable by the Agent.

Decision: adopt Option A.

### Option B: Immediate Write Preflight Runner

Implement a runner that validates a payload plan and emits `write_preflight_ready`.

Pros:

1. Faster path toward a controlled write smoke.

Cons:

1. Needs explicit operator approval semantics.
2. Needs rollback and idempotency details frozen first.
3. Could be mistaken as write authorization.

Decision: defer to a separately authorized Phase 2.84a.

### Option C: Actual Evidence Write

Write payloads into `documents` / `chunks` and indexes.

Pros:

1. Directly enables Agent answers over NAS content after indexing.

Cons:

1. Too risky without preflight, write locks, audit records, rollback, and small-batch smoke gates.
2. Would cross from planning / dry-run into mutation.

Decision: explicitly forbidden.

## Future Preflight Contract

A future preflight report should use a versioned schema:

```text
nas_evidence_write_preflight.v0
```

Top-level fields:

1. `preflight_version`
2. `run_id`
3. `created_at`
4. `payload_ref`
5. `operator_approval`
6. `write_scope`
7. `idempotency`
8. `rollback`
9. `citation_coverage`
10. `locks`
11. `safety`
12. `dry_run`
13. `decision`

## Operator Approval Requirements

A future write preflight can only proceed if it has:

1. Explicit operator approval for the specific payload run id.
2. Approval timestamp.
3. Approved project scope.
4. Approved maximum document count.
5. Approved maximum chunk count.
6. Approved maximum total text bucket.
7. Human-readable reason.
8. Expiry time.

Approval cannot be reused across payloads.

## Write Scope Requirements

Future write scope must be intentionally tiny:

1. Small batch only.
2. Default maximum: 1 document.
3. Default maximum: 20 chunks.
4. No BIM large model raw content.
5. No cross-project batch.
6. No automatic expansion from folder, project, or NAS path.

The preflight must reject any broad or ambiguous scope.

## Idempotency Requirements

Future writes must be idempotent:

1. Deterministic `idempotency_key`.
2. Deterministic external asset reference.
3. Deterministic dry-run document reference.
4. Deterministic dry-run chunk references.
5. Preflight must detect duplicate payload attempts.
6. Retry must not create duplicate documents or chunks.

Phase 2.84 does not implement idempotent writes; it only defines the contract.

## Rollback Requirements

Future writes must include a rollback plan before any mutation:

1. Candidate document ids must be traceable.
2. Candidate chunk ids must be traceable.
3. Rollback plan must remove only records from the same write run.
4. Rollback must not delete original NAS files or platform DB records.
5. Rollback must not repair, reindex, backfill, or cleanup source data.
6. Rollback status must be auditable.

If rollback cannot be described, preflight must fail closed.

## Citation Coverage Requirements

Future preflight must verify every candidate chunk has:

1. Source asset reference.
2. Source view.
3. Platform contract version.
4. Parser type.
5. Redacted citation anchor.
6. Chunk order.
7. Permission proof status.
8. No scratch path or true filename.

Missing citation coverage defaults to `DENIED`.

## Lock Requirements

Future write-capable phases must require:

1. Local write lock.
2. Payload run id lock.
3. Project scope lock.
4. Expiry / stale lock handling.
5. Refusal to run when lock state is ambiguous.

Phase 2.84 does not create locks.

## Decision States

Future write preflight may classify an item as:

1. `write_preflight_not_allowed`
2. `write_preflight_ready_for_human_review`
3. `write_preflight_ready_for_dry_run`
4. `write_preflight_no_go`

No state authorizes production rollout.

## Required Gates Before Future Phase 2.84a

A future preflight runner can only proceed if:

1. Payload state is `payload_ready_for_write_dry_run`.
2. Payload safety flags are all false.
3. Operator approval is explicit and unexpired.
4. Batch limits are within approved caps.
5. Idempotency key can be derived.
6. Rollback plan can be described.
7. Citation coverage is complete.
8. Lock strategy is explicit.
9. All artifacts remain ignored local outputs.

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
13. Treating manifest, eligibility report, payload plan, or preflight plan as document evidence.
14. Repair, cleanup source data, backfill, reindex, delete, migration, or rollout.

## Future Phase 2.84a Candidate

If separately authorized, Phase 2.84a may implement a local write-preflight dry-run evaluator:

1. Input: ignored local payload plan JSON.
2. Output: ignored local write-preflight report JSON.
3. Writes: no DB, no `documents/chunks`, no indexes, no object store.
4. Agent answer integration: false.
5. Parser execution: false.
6. Real file copy: false.
7. Raw text output: false.

## Current Conclusion

Phase 2.84 defines the final safety gate before any future controlled evidence-write dry-run.

It still does not make NAS content answerable by the Agent.

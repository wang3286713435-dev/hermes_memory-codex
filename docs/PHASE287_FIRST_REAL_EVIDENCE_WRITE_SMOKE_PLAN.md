# Phase 2.87 First Real Hermes Evidence Write Smoke Plan

## 1. Goal

Phase 2.87 is a docs-only plan for a future first controlled real Hermes evidence write smoke on a Mac mini / test machine.

This phase does not implement a writer and does not execute any real write.

The purpose is to define the exact safety gate before Hermes may write one tiny NAS-derived evidence sample into real Hermes evidence tables.

## 2. Current Baseline

Phase 2.86a is complete:

1. commit: `c5372fc`
2. tag: `phase-2.86a-evidence-write-rehearsal-baseline`
3. pushed: true

Phase 2.86a proved temp-only write ordering with in-memory / temp SQLite repositories. It did not authorize or perform real `documents`, `document_versions`, `chunks`, citation, DB, index, object-store, parser, NAS, or Agent answer actions.

## 3. Tiny Scope

A future Phase 2.87a smoke may be considered only on a test machine.

Maximum allowed scope:

1. one source asset
2. one Hermes document version
3. at most 20 chunks
4. one explicit write run id
5. one matching rollback dry-run reference

This is not production rollout, broad NAS ingestion, background sync, parser expansion, index write, object-store write, or Agent answer integration.

## 4. Separate Authorization

Phase 2.87 only plans the smoke.

Phase 2.87a must require a later explicit operator approval before any real write. The approval must be created after this plan is reviewed and before implementation or execution.

No previous dry-run, rehearsal, planning document, commit, tag, or `rehearsal_go` state is write authorization.

## 5. Prerequisite Chain

Phase 2.87a may proceed only if all prerequisite references are present and reviewable:

1. `nas_evidence_write_dry_run.v0`
2. `nas_evidence_write_rehearsal.v0`
3. project-scope permission proof
4. sanitized evidence manifest
5. evidence-write eligibility report
6. evidence-write payload plan
7. evidence-write preflight report
8. rollback dry-run reference
9. clean reviewed git ref
10. test-machine-only run context

All references must be sanitized. They must not expose raw NAS paths, true filenames, raw text, raw DB rows, secrets, sensitive business values, or source file content.

## 6. Future Operator Approval JSON

Phase 2.87a must require an approval file with at least:

```json
{
  "approval_version": "hermes_evidence_write_operator_approval.v0",
  "approval_id": "",
  "approved_by": "",
  "approved_at": "",
  "expires_at": "",
  "target_environment": "test_machine_only",
  "write_run_id": "",
  "source_asset_ref": "",
  "project_scope": "",
  "permission_proof_ref": "",
  "sanitized_manifest_ref": "",
  "eligibility_report_ref": "",
  "payload_plan_ref": "",
  "preflight_report_ref": "",
  "dry_run_ref": "",
  "rehearsal_ref": "",
  "rollback_dry_run_ref": "",
  "max_documents": 1,
  "max_document_versions": 1,
  "max_chunks": 20,
  "allowed_write_action": "first_real_hermes_evidence_write_smoke",
  "feature_flags_expected": {
    "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED": true,
    "PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED": true,
    "PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED": false,
    "PLATFORM_ASSET_INDEX_WRITE_ENABLED": false
  },
  "operator_notes": "",
  "writes_authorized": true
}
```

The approval must be scope-matched. Any mismatch in asset ref, project scope, limits, run id, rollback reference, environment, or expiration is a `Pause`.

## 7. Feature Flags

All flags default off:

```env
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_ENABLED=false
PLATFORM_ASSET_REAL_EVIDENCE_WRITE_SMOKE_ENABLED=false
PLATFORM_ASSET_AGENT_ANSWER_INTEGRATION_ENABLED=false
PLATFORM_ASSET_INDEX_WRITE_ENABLED=false
```

For a future Phase 2.87a smoke, enabling write flags is still insufficient without explicit operator approval and prerequisite references.

Index and Agent answer flags must remain false for the first write smoke.

## 8. Safety Gates

Phase 2.87a must fail closed unless all gates pass:

1. clean reviewed ref
2. test-machine-only environment
3. platform contract `delivery_platform.asset_views.v1.1`
4. valid `project_scope`
5. permission proof present
6. source asset is explicitly approved
7. source artifacts are sanitized
8. payload and preflight report are within the 1 / 1 / 20 limits
9. rollback dry-run reference exists
10. no raw path, true filename, raw text, raw row, secret, or sensitive business value is emitted

## 9. Exact Write Target Gate

The default approved write target set remains empty.

Before Phase 2.87a implementation, Codex B / operator review must explicitly name:

1. the exact SQLAlchemy model and table for the document record
2. the exact SQLAlchemy model and table for the document version record
3. the exact SQLAlchemy model and table for chunk records
4. the exact model/table or metadata field used for citation / lineage references
5. the exact repository / service methods used for each write
6. the transaction boundary and rollback / invalidation method

If the exact write targets or repository methods cannot be named safely, the decision is `Pause`.

The future smoke must not write:

1. platform DB
2. OpenSearch
3. Qdrant
4. MinIO
5. audit tables
6. production rollout state
7. unrelated Hermes records

## 10. Allowed Future Write Boundary

The only future writes may be the approved Hermes evidence records needed for one smoke run.

They must be scoped by:

1. write run id
2. source asset ref
3. project scope
4. permission proof ref
5. document/version/chunk limits
6. idempotency key

The first smoke must not run parser, copy files, scan NAS, index records, update object storage, write audit tables, or integrate with Agent final answers.

## 11. Rollback Boundary

Rollback may only remove, invalidate, or mark as smoke-invalid the records created by the one smoke run.

Rollback must never delete or mutate:

1. NAS files
2. platform rows
3. OpenSearch documents
4. Qdrant points
5. MinIO objects
6. unrelated Hermes records
7. dry-run / rehearsal source artifacts

If the write implementation cannot prove run-scoped rollback boundaries, the decision is `Pause`.

## 12. Report Boundary

Future run records must be sanitized and ignored by Git.

Reports may include:

1. write run id
2. sanitized source asset ref
3. document / version / chunk counts
4. decision state
5. idempotency summary
6. rollback summary
7. safety gate summary

Reports must not include:

1. raw file content
2. true filenames
3. true NAS paths
4. raw DB rows
5. secrets
6. sensitive business values
7. parser raw text

Committed docs must not include real run JSON.

## 13. Go / Pause / No-Go

### Go

Phase 2.87 Go means this planning document is ready for Codex B review.

Future Phase 2.87a Go may mean only that one tiny test-machine write smoke is allowed within explicit operator approval.

### Pause

Pause if:

1. exact write targets are not named
2. repository methods are not named
3. approval JSON is missing, expired, or scope-mismatched
4. permission proof is missing
5. project scope is missing
6. rollback dry-run reference is missing
7. clean reviewed ref is absent
8. payload exceeds 1 document / 1 version / 20 chunks
9. source artifacts are not sanitized
10. feature flags are ambiguous

### No-Go

No-Go if any request implies:

1. real write without later explicit operator approval
2. index write
3. platform DB write
4. object-store write
5. audit table write
6. parser execution
7. file copy
8. NAS scan
9. raw path / filename / content / DB row / secret output
10. Agent answer integration
11. repair / cleanup / backfill / reindex / delete / migration
12. production rollout

## 14. DB Platform Handoff

The platform may show catalog-only, missing-evidence, or evidence-write-candidate states.

It must not claim NAS content is answerable until:

1. a later evidence write smoke has actually created approved Hermes evidence records
2. citation / version / permission checks pass
3. a later Agent answer-integration phase is separately planned, implemented, reviewed, and validated

Catalog metadata and dry-run / rehearsal artifacts remain non-answer evidence.

## 15. Follow-up Split

Recommended split:

1. Phase 2.87a: first real Hermes DB evidence write smoke implementation / test-machine prompt, only after separate operator approval.
2. Phase 2.88: index write planning after DB evidence write is verified.
3. Phase 2.89: Agent answer integration planning after evidence, citations, permissions, rollback, and governance checks are verified.

No follow-up phase is authorized by Phase 2.87 alone.

## 16. Phase 2.87 Conclusion

Phase 2.87 defines the planning gate for a future first controlled real Hermes evidence write smoke.

It does not implement the writer and does not execute a real write.

Recommended next action: Codex B review this plan. Do not baseline or enter Phase 2.87a without a separate explicit prompt.

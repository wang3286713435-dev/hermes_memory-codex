# NEXT_CODEX_A_PROMPT

## Phase 2 Natural Import Closeout Review / Freeze Checklist Update

Do not modify runtime code unless the closeout review finds a concrete P0/P1 blocker.

## Current Accepted Result

Phase 2.112i test-machine validation returned Go for the natural-language import chain:

```text
Hermes_memory health: pass
8642 health: pass
real_upload_flag_visible: true
alias_resolution.status: alias_resolved
alias_missing: false
retrieval_suppressed: false
retrieval_evidence_document_ids_non_empty: true
citation_present: true
third_document_contamination: false
```

Accepted scope:

```text
authorized small .xlsx sample
natural-language import through 8642 / OpenWebUI-compatible backend
explicit requested alias @建筑类数据样表
same-session follow-up retrieval with citation
```

## Next Task

Prepare Phase 2 closeout / freeze checklist update.

Required review points:

1. Mark natural-language import usability as `passed_with_scope`, not unrestricted production-ready.
2. Clearly list remaining out-of-scope capabilities:
   - production rollout;
   - NAS full scan;
   - DWG/RVT/BIM content understanding;
   - large-file parser/indexing;
   - automatic long-term memory writes for file content;
   - repair / reindex / cleanup automation.
3. Confirm platform Gateway catalog-only path remains separate from standalone Hermes import/evidence path.
4. Confirm Hermes must retain standalone kernel identity, workspace/context/memory/evidence roadmap.
5. Confirm Phase 2 cannot be called complete if any PRD-critical P0/P1 item remains unverified.

## Allowed Files

Docs/eval manifests only. Likely:

1. `docs/ACTIVE_PHASE.md`
2. `docs/PHASE_BACKLOG.md`
3. `docs/TODO.md`
4. `docs/DEV_LOG.md`
5. `docs/HANDOFF_LOG.md`
6. Phase 2 closeout / freeze checklist docs or eval manifests if present.

## Hard Prohibitions

Do not:

1. run new imports;
2. scan NAS;
3. write DB / facts / document_versions / OpenSearch / Qdrant / MinIO;
4. execute repair / cleanup / backfill / reindex / delete / migration / rollout;
5. claim DWG/RVT/BIM content understanding;
6. claim production readiness;
7. erase known risks.

## Final Report Required

Report:

1. changed files;
2. whether natural import is marked `passed_with_scope`;
3. remaining Phase 2 P0/P1 blockers, if any;
4. whether Phase 2 stable freeze is recommended;
5. whether Codex B review is needed.

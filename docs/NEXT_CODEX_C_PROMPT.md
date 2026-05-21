# NEXT_CODEX_C_PROMPT

## Phase 2.112 Codex C Development-machine Test Support

Codex C is the **development-machine test-code / validation-support session**, not the Mac mini / test-machine operator.

The test-machine operator Codex owns real OpenWebUI -> 8642 execution. Use:

```text
docs/CODEX_TEST_MACHINE_PHASE2112_NATURAL_IMPORT_VALIDATION_PROMPT.md
```

for the actual Mac mini validation handoff.

## Latest Real Smoke Result

The latest test-machine run reached upload/index success but paused at alias resolution:

```text
document_id=6e89bbe8-599f-47e3-9cca-d8e7b7ae4f1b
version_id=0df440d0-9f2b-4fd5-8a84-19435fdd1b2f
chunk_count=6
indexed_count=6
title alias bind=alias_bind_failed
follow-up @建筑类数据样表 retrieval=alias_missing=true
retrieval_suppressed=true
```

## Codex C Scope

Codex C may:

1. Inspect the Hermes agent implementation on the development machine.
2. Add or adjust local tests that reproduce `alias_bind_failed` after successful import.
3. Add or adjust local tests that prove same-session `@alias` retrieval carries the imported `document_id/version_id`.
4. Review sanitized test-machine reports and classify Go / Pause / No-Go.
5. Prepare a small deterministic local fixture if Codex A needs a failing test.

Codex C must not:

1. Operate the Mac mini test machine unless explicitly assigned that role.
2. Run real OpenWebUI / 8642 upload smoke from the development machine.
3. Upload real files, scan NAS, or use sensitive data.
4. Write DB / OpenSearch / Qdrant / MinIO / facts / document_versions.
5. Execute repair, cleanup, backfill, reindex, delete, migration, or rollout.

## Recommended Codex C Checks

If asked to support Phase 2.112b, focus on local tests for:

```text
successful natural import with explicit alias
alias persistence does not use ordinary long-term memory quota
title / generated alias normalizes to the same session file alias store
follow-up @alias resolution returns alias_resolved
retrieval scope includes imported document_id/version_id filters
retrieval_suppressed=false when imported alias is available
import diagnostics are not accepted as retrieval evidence
```

## Report Format

Return:

```text
role: Codex C development-machine test support
files inspected:
tests added or suggested:
commands run:
result:
does this reproduce alias_bind_failed:
does this prove alias_resolved scoped retrieval:
forbidden actions:
recommendation for Codex A / Codex B:
```

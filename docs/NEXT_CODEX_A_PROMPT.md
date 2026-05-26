# NEXT_CODEX_A_PROMPT

## Phase 2.116d Natural Import Live No-Go Follow-up Fix

You are Codex A, the Hermes runtime development agent.

Current state:

1. Phase 2.116c was tested on the correct refs:
   - Hermes_memory `3dc4290` / `phase-2.116c-live-no-go-fix-review-baseline`
   - Hermes main `ff11f177c` / `phase-2.116c-live-no-go-root-cause-runtime-candidate`
2. Codex C result is still `No-Go`.
3. Therefore 2.116c did not reach stable closeout.

Live validation result:

1. Case 1 import success: pass.
2. Case 2 alias retrieval: fail.
   - `alias_resolved=false`
   - `alias_missing=true`
   - `retrieval_suppressed=false`
   - `retrieval_evidence_document_ids_non_empty=true`
   - `citation_present=true`
   - `third_document_contamination=false`
   - top-level / nested contamination all false
3. Case 3 import failure: fail.
   - human-readable failure exists
   - safe next-step guidance exists
   - diagnostics hidden
   - but `raw_path_output=true`
4. Case 4 fuzzy discovery: fail.
   - `safe_candidates_present=false`
   - `raw_path_hidden=false`
   - `raw_path_output=true`
   - forbidden category: `raw_local_path`

## Required approach

Do not guess. Follow root-cause-first debugging.

Before writing a fix, add or run diagnostics/tests that show:

1. For Case 2:
   - why follow-up diagnostics say `alias_missing=true` even though retrieval returned evidence/citation;
   - whether retrieval used alias binding, active document continuation, session imported document fallback, fuzzy candidate, or another path;
   - whether alias continuity store has the alias but the exposed `alias_resolution` object is stale/wrong;
   - whether the correct fix is restoring alias resolution or correcting diagnostics only when evidence truly came from the imported alias.
2. For Case 3:
   - which field renders the non-existent raw local path in the human-readable failure;
   - whether raw path comes from user text echo, parsed path, failure reason, diagnostics, suggested next step, or model context.
3. For Case 4:
   - whether raw path comes from ordinary memory, alias store, active document state, source_uri/alias_source_name, file candidate metadata, or model-generated text;
   - why candidates are not surfaced as safe candidates despite imported file being discoverable in the same validation flow.

Only after root cause is identified, make the smallest runtime fix.

## Minimal allowed scope

Allowed:

1. alias continuity restore / exposed alias diagnostics consistency for natural import follow-up;
2. safe-display sanitization for import failure and fuzzy discovery output paths;
3. file discovery candidate generation / safe candidate exposure when an imported/session file is discoverable;
4. sanitized diagnostics fields useful for Codex C validation;
5. targeted tests reproducing the exact live shapes above.

Forbidden:

1. Do not change upload adapter behavior.
2. Do not change ingestion/indexing logic.
3. Do not change retrieval scoring / retrieval contract broadly.
4. Do not change workspace inference except where needed to preserve safe display/context.
5. Do not change platform Gateway.
6. Do not scan NAS.
7. Do not parse DWG/RVT/BIM content.
8. Do not write DB / facts / versions / OpenSearch / Qdrant.
9. Do not run repair / backfill / reindex / delete / cleanup.
10. Do not production rollout.
11. Do not hide real third-document contamination.
12. Do not solve raw path checks by removing all candidates; if candidates exist, expose safe aliases/workspace/category/basename.

## Required tests

Add or update tests for:

1. Natural import follow-up where retrieval evidence/citation comes from the imported document must expose `alias_missing=false` and resolved alias diagnostics.
2. If retrieval did not actually use the alias/imported document, diagnostics must make that explicit and must not silently pass.
3. Import failure for a raw local path must return human-readable guidance without `/Users/`, `/Volumes/`, `file://`, `nas://`, `smb://`, or full source path echo.
4. Fuzzy discovery after import must surface safe candidate(s) without raw path output.
5. Ordinary memory entries containing raw paths must not leak raw paths into fuzzy file discovery output.
6. Real third-document contamination remains detectable.

## Verification required before handoff

1. py_compile touched files.
2. targeted tests for the three live blockers.
3. natural import / flow / session scope / structured citation / file steward regression.
4. `git diff --check`.

Stop after implementation and report to Codex B. Do not stable baseline or enter next phase.

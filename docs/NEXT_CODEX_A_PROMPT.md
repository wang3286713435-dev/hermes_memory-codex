# NEXT_CODEX_A_PROMPT

## Phase 2.116c Natural Import Live No-Go Root Cause Fix

You are Codex A, the Hermes runtime development agent.

Current state:

1. Phase 2.116b was tested on the correct refs:
   - Hermes_memory `949013e` / `phase-2.116b-no-go-fix-review-baseline`
   - Hermes main `f887d12bf` / `phase-2.116b-natural-import-response-polish-fix-runtime-candidate`
2. Codex C result is still `No-Go`.
3. Therefore 2.116b did not fix the live issue and must not be treated as stable closeout.

Live failures:

1. Case 2 alias retrieval:
   - `alias_resolved=true`
   - `alias_missing=false`
   - `retrieval_suppressed=false`
   - `citation_present=true`
   - but `third_document_contamination=true`
2. Case 4 fuzzy discovery:
   - `safe_candidates_present=false`
   - `raw_path_hidden=false`
   - `raw_path_output=true`
   - forbidden token category: `raw_local_path`

## Required approach

Do not guess. Follow root-cause-first debugging.

Before writing a fix, add or run diagnostics that show:

1. For Case 2:
   - where `third_document_contamination=true` is reintroduced after `_contamination_flags`;
   - whether final OpenWebUI/8642 response reads `third_document_contamination` from `trace`, `retrieval_trace`, `context_scope`, rendered text, or another field;
   - whether any stale field survives under a different key not overwritten by 2.116b.
2. For Case 4:
   - whether raw path is coming from `title`, `source_name`, `display_path`, `source_uri`, `alias_source_name`, active document hint, model-generated text, or another field;
   - whether `safe_candidates_present=false` means candidate extraction failed before rendering, or candidates exist but are not exposed to the model/user.

Only after root cause is identified, make the smallest runtime fix.

## Minimal allowed scope

Allowed:

1. runtime trace normalization / output sanitization directly related to these two failed fields;
2. file candidate / alias candidate display safety;
3. targeted tests reproducing the live failure shape;
4. additional diagnostics fields if sanitized and useful for Codex C validation.

Forbidden:

1. Do not change upload adapter behavior.
2. Do not change ingestion/indexing logic.
3. Do not change retrieval scoring / retrieval contract broadly.
4. Do not change workspace inference except where needed to sanitize output of existing candidates.
5. Do not change platform Gateway.
6. Do not scan NAS.
7. Do not parse DWG/RVT/BIM content.
8. Do not write DB / facts / versions / OpenSearch / Qdrant.
9. Do not run repair / backfill / reindex / delete / cleanup.
10. Do not production rollout.
11. Do not hide real third-document contamination; only clear stale false positives when actual returned evidence is in scope.
12. Do not hide all file candidates just to pass raw path checks; if candidates exist, expose safe alias/workspace/category/basename.

## Required tests

Add or update tests that reproduce the live failure shape, not only the previous synthetic shape:

1. `third_document_contamination=true` exists in an upstream/stale trace field while actual returned evidence is in scope; final exposed diagnostics/context must show false.
2. An actual out-of-scope returned document still produces `third_document_contamination=true`.
3. Fuzzy discovery candidate has raw path in every plausible source field (`title`, `source_name`, `display_path`, `source_uri`, `alias_source_name`, active-document fallback); default user/context output must not contain `/Users/`, `/Volumes/`, `file://`, `nas://`, `smb://`.
4. Fuzzy discovery with a candidate must produce a safe candidate, not an empty/no-candidate response, when a safe basename/alias can be derived.
5. Human category slash remains intact: `人力配置 / 成本测算`.

## Verification required before handoff

1. py_compile touched files.
2. targeted tests for the two live blockers.
3. natural import / flow / session scope / structured citation / file steward regression.
4. `git diff --check`.

Stop after implementation and report to Codex B. Do not stable baseline or enter next phase.

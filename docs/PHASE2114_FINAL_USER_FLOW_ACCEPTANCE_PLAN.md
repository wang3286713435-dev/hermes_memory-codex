# Phase 2.114 Final User-flow Acceptance / Freeze Decision Pack

## 1. Purpose

Phase 2.114 is the final user-facing acceptance gate before any Phase 2 stable freeze decision.

It answers one practical question:

```text
Can Hermes, in the real OpenWebUI / 8642 test-machine path, behave like an enterprise memory-kernel Agent for a complete small-file workflow?
```

This phase is not a new feature implementation phase. It is a controlled validation and freeze-decision pack.

## 2. Why This Exists

Phase 2.113a proved that Hermes can explain its memory / workspace / evidence kernel and no longer misroutes ordinary `帮我找` retrieval questions into file-discovery suppression.

However, Phase 2 stable freeze should not rely on self-awareness alone. The final user-flow must prove the complete user experience:

1. User asks Hermes to import an authorized small file in natural language.
2. Hermes imports through the configured upload adapter.
3. Hermes reports a safe alias, safe document/version IDs, chunk/index status, and follow-up suggestions.
4. User asks a follow-up question by alias.
5. Hermes resolves the alias, retrieves evidence, and returns citation.
6. Hermes explains its evidence boundary and does not confuse import diagnostics / memory metadata with retrieval evidence.

## 3. Scope

Allowed:

1. One controlled OpenWebUI / 8642 smoke on the test machine.
2. One explicitly authorized small, non-sensitive sample file.
3. Natural-language import through the configured Hermes backend, not direct upload API.
4. Same-session follow-up retrieval by alias.
5. Self-awareness / evidence-boundary check after import.
6. Sanitized report with safe IDs and pass/pause/no-go decision.

Forbidden:

1. Production rollout.
2. NAS full scan or recursive folder scan.
3. Unbounded file import.
4. DWG/RVT/BIM content understanding claims.
5. Raw path, raw file content, token, secret, raw DB row, or storage URI output.
6. Manual DB / index writes outside the configured natural import pipeline.
7. Repair / cleanup / backfill / reindex / delete / migration.
8. Treating aliases, workspace refs, memory metadata, or import diagnostics as retrieval evidence.
9. Long-term memory writes containing raw path, raw content, secret, or customer-sensitive material.

## 4. Required Test-machine Flow

The test-machine operator must use `docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md`.

Required cases:

1. Preflight: reviewed refs, worktree clean, 8642 health, Hermes Memory health, real-upload flag visible.
2. Self-awareness: Hermes states its memory / workspace / retrieval / evidence boundary.
3. Natural import: one authorized small file is imported through natural language.
4. Alias UX: Hermes reports the alias it will use; explicit alias is preferred if supplied, generated alias is allowed if safe and user-visible.
5. Follow-up retrieval: `@alias` question returns `alias_missing=false`, `retrieval_suppressed=false`, non-empty `retrieval_evidence_document_ids`, and citation.
6. Evidence boundary: Hermes states that import diagnostics / alias / workspace refs are not content evidence.
7. Safety: no leak, no NAS scan, no forbidden write, no rollout.

## 5. Go / Pause / No-Go

Go requires:

1. 8642 health passes.
2. Hermes Memory health passes.
3. Natural import succeeds for one authorized small sample.
4. Hermes returns safe alias / document_id / version_id / chunk_count / indexed_count.
5. Same-session alias follow-up resolves and retrieves evidence.
6. Citation is present.
7. No third-document contamination.
8. Self-awareness and evidence-boundary answer passes.
9. No secret / raw path / file content / NAS scan / repair / rollout / manual DB-index write.

Pause if:

1. Test-machine environment is not on reviewed refs.
2. Required flag / token / service is missing.
3. User has not authorized a sample file.
4. Provider usage limit prevents the follow-up answer.
5. Retrieval backend is unavailable.
6. Alias is safe but retrieval evidence is not produced.

No-Go if:

1. Any secret, token, raw path, file content, raw DB row, or storage URI is printed.
2. Any NAS scan or unbounded import is attempted.
3. Any forbidden repair / reindex / migration / rollout is attempted.
4. Hermes fabricates content without retrieval evidence.
5. Hermes claims DWG/RVT/BIM content understanding from catalog/import metadata.

## 6. Freeze Interpretation

If Phase 2.114 returns Go, Phase 2 may freeze as:

```text
Stable Hermes enterprise-kernel MVP baseline for internal controlled use.
```

It may include:

1. platform catalog-only read-only integration;
2. standalone Hermes memory-kernel identity;
3. small-file natural-language import with alias and citation follow-up;
4. Missing Evidence / citation / safety boundaries;
5. future-compatible paths for platform unlock, Evidence Layer, Memory Layer, and NAS governance.

It still must not claim:

1. production rollout;
2. unrestricted NAS management;
3. DWG/RVT/BIM content understanding;
4. full Data Steward productization;
5. Agent DB CRUD / SQL;
6. PRD 100+ / Roadmap 300+ accepted eval closeout unless explicitly reclassified.

## 7. Next Actions After Result

If Go:

1. Update `eval/phase2_inventory/phase2_final_freeze_checklist.json`.
2. Mark final user-flow acceptance as passed with scope.
3. Decide whether to tag Phase 2 stable MVP baseline.
4. Create Phase 3 entry with inherited known gaps.

If Pause / No-Go:

1. Record the smallest blocker.
2. Do not expand scope.
3. Return a bounded Codex A fix prompt only for that blocker.

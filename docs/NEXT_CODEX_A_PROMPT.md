# NEXT_CODEX_A_PROMPT

## Phase 2.116b Natural Import Response Polish No-Go Fix

You are Codex A, the Hermes runtime development agent.

Current state:

1. Phase 2.116 runtime candidate `e04cc6feb` / `phase-2.116-natural-import-response-polish-runtime-candidate` was reviewed and pushed.
2. Codex C / test machine live validation returned `No-Go`.
3. Passed:
   - import success default reply is product-facing;
   - import failure default reply is human-readable;
   - diagnostics block is hidden in those two cases.
4. Failed:
   - Case 4 fuzzy discovery default reply still exposed raw path (`raw_path_output=true`);
   - Case 2 same-session alias retrieval reported third-document contamination signal.

Root-cause investigation requirement:

Before editing, trace exactly where fuzzy discovery response gets raw path from:

1. candidate trace fields;
2. context builder helper formatting;
3. final answer rendering / model context;
4. any source_name/title/display_path fallback that may contain raw path.

Also trace why alias retrieval reports third-document contamination:

1. whether retrieval evidence actually contains another document;
2. whether contamination flag is a stale/diagnostic false positive;
3. whether candidate/file discovery context is being mixed into retrieval answer context.

Allowed write scope:

1. Hermes main only.
2. Fuzzy discovery / file candidate safe rendering.
3. Alias retrieval contamination guard if it is caused by Phase 2.116 rendering/context changes.
4. Tests proving raw path is hidden and third-document contamination does not occur.

Required tests:

1. Fuzzy discovery candidate with `source_name`, `title`, `display_path`, or fallback containing an absolute path must not render raw path.
2. Fuzzy discovery default response must show only safe alias / workspace / category / safe basename if needed.
3. Same-session alias retrieval after import must not include unrelated candidate context and must not set third-document contamination when evidence scope is the imported document.
4. Existing import success/failure user-facing tests must remain green.

Codex C rerun requirement after fix:

Use the same Phase 2.116 live validation prompt and confirm:

1. Case 1 pass.
2. Case 2 pass with `third_document_contamination=false`.
3. Case 3 pass.
4. Case 4 pass with `raw_path_hidden=true`.

Codex A hard boundary:

1. Do not change upload adapter behavior.
2. Do not change ingestion/indexing logic.
3. Do not change retrieval contract except for contamination diagnostics if proven to be a false positive caused by context mixing.
4. Do not change workspace inference logic except to sanitize display fields.
5. Do not change platform Gateway code.
6. Do not scan NAS.
7. Do not parse DWG/RVT/BIM content.
8. Do not write raw path / raw content / secret into memory.
9. Do not run production rollout.
10. Do not broaden Phase 2.116b beyond these two No-Go blockers.

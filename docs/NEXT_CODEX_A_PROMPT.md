# NEXT_CODEX_A_PROMPT

## Phase 2.116 Natural Import User-facing Response Polish Validation Gate

You are Codex A, the Hermes runtime development agent.

Current state:

1. Phase 2.116 bounded implementation is complete in Hermes main.
2. Default natural import success / failure rendering is product-facing and no longer dumps `Natural file import diagnostics` to normal users.
3. Debug diagnostics remain available through `response.diagnostics` and explicit debug rendering.
4. Fuzzy discovery candidates now render safe alias / workspace / category and hide technical IDs by default.
5. Local verification passed:
   - py_compile for touched files;
   - `tests/agent/test_natural_file_import_runtime.py tests/agent/test_structured_citation_context.py` -> `38 passed`;
   - `tests/agent/test_natural_file_import_runtime.py tests/agent/test_natural_file_import_flow.py tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_file_steward_ux.py` -> `130 passed`.

Codex B review result:

1. Review passed.
2. Runtime candidate pushed:
   - Hermes main commit: `e04cc6feb`
   - tag: `phase-2.116-natural-import-response-polish-runtime-candidate`

Next required action:

1. Codex C / test machine validates OpenWebUI / 8642 default user-facing output:
   - import success does not show diagnostics block;
   - import failure is human-readable;
   - fuzzy discovery hides technical IDs;
   - retrieval/citation behavior remains unchanged.
2. Codex A must stay idle unless Codex C returns a concrete Phase 2.116 blocker.

Codex A hard boundary:

1. Do not continue coding unless Codex C returns a concrete Phase 2.116 blocker.
2. Do not change upload adapter behavior.
3. Do not change ingestion/indexing logic.
4. Do not change retrieval contract.
5. Do not change workspace inference logic.
6. Do not change platform Gateway code.
7. Do not scan NAS.
8. Do not parse DWG/RVT/BIM content.
9. Do not write raw path / raw content / secret into memory.
10. Do not run production rollout.
11. Do not baseline / tag / push without explicit user instruction.

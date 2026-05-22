# NEXT_CODEX_A_PROMPT

## Phase 2.114 Test-machine Final User-flow Acceptance Retry

You are Codex A, the Hermes runtime development agent.

Phase 2.114a natural import path parser fix is implemented and published as a runtime test-candidate.

Do not write more runtime code unless the next test-machine run returns a concrete blocker.

Read first:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PLAN.md`
5. `docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md`
6. `docs/TODO.md`
7. `docs/DEV_LOG.md`

## Runtime Candidate

Hermes agent:

```text
commit: c8ed29a83c441f58939f64b6b175ae4cac980ea3
tag: phase-2.114a-natural-import-path-parser-runtime-test-candidate
remote: backup2
```

## What Was Fixed

Natural import path parser now supports:

1. fullwidth colon before path;
2. Chinese period after path;
3. Chinese characters in paths;
4. unquoted paths with spaces in parent directories;
5. alias text and project context in the same prompt;
6. multiple paths remain rejected as `multiple_paths_not_supported`.

Local validation:

```text
py_compile passed
tests/agent/test_natural_file_import.py tests/agent/test_natural_file_import_flow.py tests/agent/test_natural_file_import_runtime.py: 54 passed
```

## Required Next Step

Test-machine / Codex C should:

1. checkout `phase-2.114a-natural-import-path-parser-runtime-test-candidate`;
2. restart 8642 from that checkout;
3. confirm Hermes Memory `/health`;
4. confirm `HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true` is visible to 8642;
5. run `docs/CODEX_TEST_MACHINE_PHASE2114_FINAL_USER_FLOW_ACCEPTANCE_PROMPT.md`;
6. use exactly one authorized small non-sensitive sample file.

## Go Criteria

Go requires:

1. parser extracts the authorized path from the Chinese prompt;
2. natural import succeeds for exactly one authorized small sample;
3. Hermes reports safe alias / document_id / version_id / chunk_count / indexed_count;
4. same-session alias follow-up returns `alias_missing=false`, `retrieval_suppressed=false`, non-empty evidence document IDs, and citation;
5. Hermes states that alias / import diagnostics / workspace refs / memory metadata are not content evidence;
6. no raw path, secret, file content, NAS scan, repair/reindex/migration/rollout, or manual DB/index write.

## If User Says "Execute"

Do not re-run implementation.

Report that Phase 2.114a runtime candidate is ready and the next action is test-machine / Codex C validation.

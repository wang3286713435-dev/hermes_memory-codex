# Phase 2.113a Self-Awareness Review Fix

## 1. Codex B Review Result

Phase 2.113 runtime fix is directionally correct but not ready for baseline.

Decision:

```text
review_result = returned_for_fix
baseline_allowed = false
```

## 2. What Passed

Codex A completed a local implementation that adds:

1. Hermes Memory Kernel capability boundary context.
2. Natural import success response with import status, safe document/version ids, chunk/index status, recommended alias, follow-up suggestions, and Missing Evidence boundary.
3. No-safe-candidate fuzzy file discovery suppression.
4. Targeted local tests:
   - natural import runtime: `14 passed`;
   - structured citation context: `18 passed`;
   - session document scope: `67 passed`.

Codex B reran the combined target suite:

```text
99 passed
```

## 3. Blocking Finding

The current file-discovery guard is too broad.

Observed with direct local probe:

```text
帮我找一下工程地点 -> suppress_retrieval=true; file_discovery_no_safe_candidate
帮我找一下主标书里的工期要求 -> suppress_retrieval=true; file_discovery_no_safe_candidate
有哪些文件 -> suppress_retrieval=true; file_discovery_no_safe_candidate
C塔项目的招标要求文件你帮我找出来 -> suppress_retrieval=true; file_discovery_no_safe_candidate
```

The last case is intended fuzzy file discovery. The first two are ordinary retrieval-style questions and must not be suppressed merely because the user says "帮我找一下".

Root cause:

```text
SessionDocumentScopeStore._FILE_DISCOVERY_RE includes broad phrases such as "帮我找" and "找一下".
```

This risks turning normal retrieval queries into Missing Evidence / no-safe-file-candidate responses.

## 4. Secondary Finding

The kernel self-awareness trigger is somewhat narrow.

Observed local probe:

```text
你能做什么 -> true
你有没有记忆库 -> true
Hermes有什么能力 -> true
你能不能管理文件 -> true
能不能管理文件 -> false
你可以帮我管理文件吗 -> false
你能管理公司文件吗 -> false
```

The minimum required query `你能不能管理文件` is covered, but real user wording is likely broader. This is not as severe as the file-discovery regression, but Codex A should broaden it safely while preserving overclaim controls.

## 5. Required Fix

Codex A must implement a bounded Phase 2.113a fix:

1. Narrow fuzzy file discovery so it only triggers when the user intent is clearly file-candidate discovery, not ordinary document content retrieval.
2. Preserve the intended target behavior for prompts like:
   - `C塔项目的招标要求文件你帮我找出来`;
   - `帮我找 C塔项目相关文件`;
   - `有哪些 C塔项目人力配置相关文件`.
3. Do not suppress retrieval for ordinary questions like:
   - `帮我找一下工程地点`;
   - `帮我找一下主标书里的工期要求`;
   - `帮我查一下付款比例`;
   - `找一下这份表里的数量`.
4. Broaden kernel capability trigger for common user wording:
   - `你可以帮我管理文件吗`;
   - `你能管理公司文件吗`;
   - `能不能管理文件`;
   - `你怎么使用记忆库`.
5. Add regression tests for both the positive and negative cases above.

## 6. Forbidden Work

Do not:

1. broaden platform Gateway beyond catalog-only;
2. scan NAS;
3. run production rollout;
4. expose raw file paths or raw DB rows;
5. write raw file content / secret / raw paths into memory;
6. implement Agent DB CRUD or arbitrary SQL;
7. claim DWG/RVT/BIM content understanding;
8. use memory/workspace metadata as retrieval evidence;
9. stage unrelated `uv.lock`, adapter reload, or repo-hygiene files.

## 7. Validation Required

Codex A should run:

```bash
python3 -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/session_document_scope.py agent/memory_kernel/natural_file_import_runtime.py
uv run pytest <targeted tests for kernel capability trigger and file-discovery routing>
uv run pytest <existing natural import / structured citation / session scope targets>
git diff --check
```

If `uv run pytest` is unavailable, use the existing project venv test command and report the exact reason.

## 8. Next Review Gate

After Codex A fixes Phase 2.113a:

1. Codex B reruns targeted regression.
2. If clean, publish a runtime test-candidate for test-machine / OpenWebUI / 8642.
3. Test-machine validates:
   - self-awareness answer;
   - natural import success feedback;
   - explicit/generated alias;
   - fuzzy file discovery candidates;
   - ordinary retrieval not suppressed by "帮我找一下".

Do not baseline Phase 2.113 before this fix.

## 9. Implementation Result

Codex A completed the bounded Phase 2.113a fix.

Runtime changes:

1. Fuzzy file discovery now only triggers for clear file-candidate discovery wording such as `哪个文件`、`哪份文件`、`相关文件`、`候选文件`、`...文件...找出来`.
2. Ordinary content lookup wording such as `帮我找一下工程地点`、`帮我找一下主标书里的工期要求`、`帮我查一下付款比例`、`找一下这份表里的数量` no longer suppresses retrieval.
3. Kernel self-awareness trigger now covers common file-management and memory-library wording:
   - `你可以帮我管理文件吗`
   - `你能管理公司文件吗`
   - `能不能管理文件`
   - `你怎么使用记忆库`

Validation:

```text
./.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/session_document_scope.py agent/memory_kernel/natural_file_import_runtime.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_natural_file_import_runtime.py -q
102 passed
```

Current gate:

```text
implementation_status = completed
baseline_allowed = false_until_codex_b_review
live_validation_required = true
```

## 10. Codex B Review Acceptance

Codex B reviewed the Phase 2.113a fix and accepted it for test-machine validation.

Review checks:

1. `py_compile` passed for `context_builder.py`, `kernel.py`, `session_document_scope.py`, and `natural_file_import_runtime.py`.
2. Target regression suite passed:

```text
tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_natural_file_import_runtime.py
102 passed
```

3. Direct probe confirmed ordinary retrieval-style wording no longer triggers file-discovery suppression:
   - `帮我找一下工程地点`
   - `帮我找一下主标书里的工期要求`
   - `帮我查一下付款比例`
   - `找一下这份表里的数量`
4. Direct probe confirmed clear file-candidate discovery still fail-closes safely when no candidates are available:
   - `C塔项目的招标要求文件你帮我找出来`
   - `帮我找 C塔项目相关文件`
   - `有哪些 C塔项目人力配置相关文件`
5. Direct probe confirmed self-awareness triggers for file-management / memory-library wording:
   - `你可以帮我管理文件吗`
   - `你能管理公司文件吗`
   - `能不能管理文件`
   - `你怎么使用记忆库`

Runtime candidate:

```text
hermes-agent commit = a12d378e0
hermes-agent tag = phase-2.113a-self-awareness-runtime-test-candidate
```

Next gate:

1. Test machine checks out `phase-2.113a-self-awareness-runtime-test-candidate`.
2. Restart 8642 from that checkout.
3. Run `docs/CODEX_TEST_MACHINE_PHASE2113A_SELF_AWARENESS_SMOKE_PROMPT.md`.
4. Do not enter final Phase 2.113 closeout until OpenWebUI / 8642 live validation passes.

## 11. Test-machine Live Validation Result

Test-machine / OpenWebUI-compatible 8642 validation returned Go.

Runtime under test:

```text
hermes-agent tag = phase-2.113a-self-awareness-runtime-test-candidate
backend_8642_health = pass
hermes_memory_health = pass
real_upload_flag_visible = true
```

Passed cases:

1. Self-awareness answer passed:
   - mentions memory kernel;
   - mentions alias / workspace;
   - mentions retrieval / citation;
   - mentions Missing Evidence;
   - no overclaim detected.
2. Ordinary retrieval guard passed:
   - `帮我找` retrieval-style questions were not misrouted to fuzzy file discovery.
3. Fuzzy file discovery passed:
   - candidates or Missing Evidence behavior was safe;
   - no raw path or secret leak.
4. Safety passed:
   - no secret printed;
   - no raw path output;
   - no file content output;
   - no NAS scan;
   - no repair / cleanup / backfill / reindex / delete / migration / rollout;
   - no manual DB or index write.

Skipped by design:

```text
natural_import_feedback = skipped_by_no_import_authorization
```

This is acceptable for the Phase 2.113a live gate because the smoke prompt made natural import feedback conditional on explicit operator authorization for a small non-sensitive import.

Current gate:

```text
self_awareness_live_gate = passed
ordinary_retrieval_guard_live_gate = passed
fuzzy_file_discovery_live_gate = passed
phase_2_113a_live_validation = go
production_rollout = forbidden
```

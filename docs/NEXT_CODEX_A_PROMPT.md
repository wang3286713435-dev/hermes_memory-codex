# NEXT_CODEX_A_PROMPT

## Phase 2.113a Live Validation Gate

You are Codex A, the Hermes runtime development agent.

Do not continue coding unless the test-machine / OpenWebUI / 8642 validation returns a concrete blocker.

Read first:

1. `docs/AGENT_OPERATING_PROTOCOL.md`
2. `docs/ACTIVE_PHASE.md`
3. `docs/PHASE_BACKLOG.md`
4. `docs/PHASE2113_HERMES_MEMORY_SELF_AWARENESS_KERNEL_ACTIVATION.md`
5. `docs/PHASE2113A_SELF_AWARENESS_REVIEW_FIX.md`
6. `docs/CODEX_TEST_MACHINE_PHASE2113A_SELF_AWARENESS_SMOKE_PROMPT.md`
7. `docs/TODO.md`
8. `docs/DEV_LOG.md`

## Current State

Phase 2.113a has passed Codex B local review.

Hermes agent runtime test-candidate:

```text
commit = a12d378e0
tag = phase-2.113a-self-awareness-runtime-test-candidate
```

Accepted fixes:

1. Ordinary retrieval-style questions such as `帮我找一下工程地点` and `帮我找一下主标书里的工期要求` are no longer suppressed as file-discovery questions.
2. Clear file-candidate discovery such as `C塔项目的招标要求文件你帮我找出来` still fail-closes safely when no safe candidates exist.
3. Kernel self-awareness trigger covers natural file-management / memory-library wording.

## Verified by Codex B

```bash
./.venv/bin/python -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/session_document_scope.py agent/memory_kernel/natural_file_import_runtime.py
./.venv/bin/python -m pytest -o addopts='' tests/agent/test_session_document_scope.py tests/agent/test_structured_citation_context.py tests/agent/test_natural_file_import_runtime.py -q
```

Result:

```text
102 passed
```

Codex B also ran direct probes for ordinary retrieval, fuzzy file-discovery, and self-awareness trigger coverage.

## Required Next Step

The next action is test-machine validation, not new Codex A implementation.

Use:

```text
docs/CODEX_TEST_MACHINE_PHASE2113A_SELF_AWARENESS_SMOKE_PROMPT.md
```

The test machine should validate:

1. self-awareness answer;
2. ordinary retrieval not suppressed by `找一下 / 帮我找`;
3. fuzzy file discovery candidates / safe Missing Evidence;
4. natural import success feedback and same-session retrieval only if the operator explicitly authorizes one small non-sensitive import.

## If Test-machine Returns Go

Codex A should not automatically implement new features.

Codex B should update Phase 2.113 closeout and decide whether Phase 2 can proceed to the next freeze gate.

## If Test-machine Returns Pause / No-Go

Only then should Codex A receive a new bounded fix prompt with:

1. exact failing case;
2. sanitized diagnostics;
3. smallest allowed write scope;
4. target tests;
5. forbidden actions.

## Do Not

1. Do not code beyond the returned blocker.
2. Do not run production rollout.
3. Do not scan NAS.
4. Do not write DB / facts / document_versions / OpenSearch / Qdrant.
5. Do not repair / cleanup / backfill / reindex / delete / migrate.
6. Do not modify retrieval contract.
7. Do not modify memory kernel main architecture.
8. Do not treat diagnostics, aliases, workspace refs, or memory metadata as retrieval evidence.
9. Do not stage unrelated `uv.lock`, adapter reload, or repo-hygiene files.

## If User Says "Execute"

Report that Phase 2.113a is waiting for test-machine validation with `docs/CODEX_TEST_MACHINE_PHASE2113A_SELF_AWARENESS_SMOKE_PROMPT.md`.

Do not make new code changes unless the user provides a new bounded implementation request after test-machine feedback.

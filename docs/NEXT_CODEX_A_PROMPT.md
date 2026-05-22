# NEXT_CODEX_A_PROMPT

## Phase 2.113a Self-Awareness Review Fix

You are Codex A, the Hermes runtime development agent.

Codex B reviewed the Phase 2.113 runtime fix. The direction is correct, but baseline is blocked by a routing regression risk.

Read first:

1. `docs/PHASE2113A_SELF_AWARENESS_REVIEW_FIX.md`
2. `docs/PHASE2113_HERMES_MEMORY_SELF_AWARENESS_KERNEL_ACTIVATION.md`
3. `docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md`

## Blocking Finding

The current fuzzy file-discovery guard is too broad.

Observed by Codex B local probe:

```text
帮我找一下工程地点 -> suppress_retrieval=true; file_discovery_no_safe_candidate
帮我找一下主标书里的工期要求 -> suppress_retrieval=true; file_discovery_no_safe_candidate
有哪些文件 -> suppress_retrieval=true; file_discovery_no_safe_candidate
C塔项目的招标要求文件你帮我找出来 -> suppress_retrieval=true; file_discovery_no_safe_candidate
```

The last case is intended fuzzy file discovery. The first two are normal retrieval questions and must not be suppressed just because the user says "帮我找一下".

## Required Fix

Implement the smallest runtime fix in `hermes-agent`:

1. Narrow fuzzy file discovery so it only triggers when the user clearly asks to find candidate files.
2. Preserve true fuzzy file discovery:
   - `C塔项目的招标要求文件你帮我找出来`
   - `帮我找 C塔项目相关文件`
   - `有哪些 C塔项目人力配置相关文件`
3. Do not suppress ordinary retrieval:
   - `帮我找一下工程地点`
   - `帮我找一下主标书里的工期要求`
   - `帮我查一下付款比例`
   - `找一下这份表里的数量`
4. Broaden kernel self-awareness trigger for common wording:
   - `你可以帮我管理文件吗`
   - `你能管理公司文件吗`
   - `能不能管理文件`
   - `你怎么使用记忆库`
5. Add targeted regression tests.

## Existing Good Work to Preserve

Do not regress:

1. Hermes Memory Kernel capability boundary context.
2. Natural import success response with safe alias, safe IDs, chunk/index status, follow-up suggestions, and Missing Evidence boundary.
3. Explicit alias preservation.
4. Generated safe alias behavior.
5. Memory/workspace metadata not being treated as content evidence.
6. DWG/RVT/BIM overclaim guard.

## Forbidden Work

Do not:

1. scan NAS;
2. run production rollout;
3. expose raw file paths or raw DB rows;
4. write secrets or raw document text into memory;
5. broaden platform Gateway beyond catalog-only;
6. change DB schema;
7. run repair / cleanup / backfill / reindex / delete / migration;
8. implement Agent DB CRUD or arbitrary SQL;
9. claim DWG/RVT/BIM content understanding;
10. treat diagnostics, metadata, memory refs, aliases, or history memory as retrieval evidence;
11. stage unrelated `uv.lock`, adapter reload, repo-hygiene, or runtime artifact files.

## Validation Required

Run:

```bash
python3 -m py_compile agent/memory_kernel/context_builder.py agent/memory_kernel/kernel.py agent/memory_kernel/session_document_scope.py agent/memory_kernel/natural_file_import_runtime.py
uv run pytest <targeted tests for kernel capability trigger and file-discovery routing>
uv run pytest <existing natural import / structured citation / session scope targets>
git diff --check
```

If this repo uses a local venv instead of `uv`, use the established local command and report it exactly.

## Final Report Required

Report:

1. changed files;
2. how fuzzy file-discovery intent is now distinguished from ordinary retrieval;
3. self-awareness trigger cases covered;
4. tests run and results;
5. unrelated dirty excluded;
6. forbidden actions not performed;
7. whether Codex B review is required;
8. whether test-machine / OpenWebUI / 8642 validation is required.

Do not declare Phase 2 complete from this phase alone.

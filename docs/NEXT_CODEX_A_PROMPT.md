# NEXT_CODEX_A_PROMPT

## Phase 2.113 Hermes Memory Self-Awareness / Kernel Activation

You are Codex A, the Hermes runtime development agent.

This is a P0 blocker fix. Do not treat Hermes as a generic chatbot plus a separate memory database. Hermes must present and use its governed memory / workspace / retrieval / evidence kernel as a native part of the Agent.

## Required Reading

Read these first:

1. `docs/PHASE2113_HERMES_MEMORY_SELF_AWARENESS_KERNEL_ACTIVATION.md`
2. `docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md`
3. `docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md`
4. `docs/PHASE2108_STANDALONE_KERNEL_FREEZE_CONTRACT.md`
5. `docs/PRD.md`
6. `docs/ROADMAP.md`
7. `docs/TECHNICAL_DESIGN.md`

## Current Accepted Result

Phase 2.112i accepted this scoped test-machine result:

```text
Hermes_memory health: pass
8642 health: pass
real_upload_flag_visible: true
alias_resolution.status: alias_resolved
alias_missing: false
retrieval_suppressed: false
retrieval_evidence_document_ids_non_empty: true
citation_present: true
third_document_contamination: false
```

Accepted scope:

```text
authorized small .xlsx sample
natural-language import through 8642 / OpenWebUI-compatible backend
explicit requested alias @建筑类数据样表
same-session follow-up retrieval with citation
```

## Problem to Fix

The pipeline can import and retrieve, but the user-facing Hermes persona still does not reliably know or explain that it owns a powerful Hermes_memory / workspace / evidence kernel.

Target product behavior:

1. Hermes can answer what it can do as an enterprise memory-kernel Agent.
2. Natural import success tells the user the file was remembered/imported and what alias was assigned.
3. If the user provides an alias, the exact safe alias wins.
4. If the user omits an alias, Hermes generates or recommends a safe alias.
5. Fuzzy file requests return safe candidates and ask for clarification, or return Missing Evidence / no safe candidate.
6. Low-sensitive memory/workspace hints are allowed only as context, never as content evidence or permission proof.

## Implementation Requirements

Make the smallest runtime change in `hermes-agent` needed for the 8642 / OpenWebUI-compatible path.

Likely areas to inspect:

1. OpenAI-compatible gateway prompt construction.
2. `AIAgent` / memory-kernel context assembly.
3. natural import success-response rendering.
4. alias generation and alias persistence user-facing response.
5. session document-scope / fuzzy file-discovery behavior.
6. low-sensitive memory candidate and rejection paths.

Do not assume this list is complete. Inspect current code before patching.

## Required Behavior

Self-awareness answer must mention, with boundaries:

1. governed file import / catalog access;
2. aliases and workspace references;
3. retrieval evidence and citations;
4. Missing Evidence;
5. low-sensitive continuity hints;
6. no raw path / raw content / secret memory;
7. no DWG/RVT/BIM content claim without evidence.

Natural import success response must include:

1. import status;
2. alias used or generated;
3. safe document/version identifiers when available;
4. chunk/index status when available;
5. suggested follow-up questions;
6. evidence boundary.

Fuzzy discovery must:

1. use only safe session/workspace/catalog candidates available to the current context;
2. return bounded candidate lists;
3. ask the user to choose when multiple candidates match;
4. return Missing Evidence when no safe candidate exists;
5. never expose raw storage paths or raw DB rows.

## Tests Required

Use TDD. Add targeted tests before implementation.

Minimum tests:

1. Self-awareness / capability answer is not generic chatbot-only and does not overclaim.
2. Explicit alias import reports the exact alias and can resolve it.
3. No-alias import generates or recommends a safe alias.
4. Fuzzy file discovery returns candidates + clarification, or Missing Evidence.
5. Memory boundary rejects raw path / raw content / secret and never treats memory as evidence.
6. DWG / RVT / BIM content questions still return Missing Evidence unless governed evidence exists.

Suggested validation:

```bash
python3 -m py_compile <changed python files>
uv run pytest <targeted tests for self-awareness / natural import / session scope / memory boundary>
git diff --check
```

If this environment lacks a required pytest plugin, report that explicitly and run the nearest targeted test subset available without installing dependencies unless authorized.

## Allowed Files

Runtime and tests in `hermes-agent` required for the bounded fix. Update Hermes main docs if needed:

1. `docs/TODO.md`
2. `docs/DEV_LOG.md`

Also update Hermes_memory handoff docs only if you need to report completion state.

## Hard Prohibitions

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
10. treat diagnostics, metadata, memory refs, or aliases as retrieval evidence.

## Final Report Required

Report:

1. changed files;
2. self-awareness behavior implemented;
3. natural import alias / generated alias behavior;
4. fuzzy file discovery behavior;
5. memory boundary behavior;
6. tests run and results;
7. forbidden actions not performed;
8. whether Codex B review is required;
9. whether test-machine / OpenWebUI / 8642 validation is required.

Do not declare Phase 2 complete from this phase alone.

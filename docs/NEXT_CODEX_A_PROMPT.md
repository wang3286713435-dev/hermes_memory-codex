# NEXT_CODEX_A_PROMPT

## Phase 2.112 Natural Import Workspace Retrieval Fix

You are Codex A for Hermes mainline development.

This task exists because real operator testing proved the natural-language import upload path now works, but same-session retrieval is still blocked.

## Required Reading

Read first:

```text
docs/PHASE2112_NATURAL_IMPORT_WORKSPACE_RETRIEVAL_FIX_PLAN.md
docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md
eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json
docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md
docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md
docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md
docs/PHASE256D_NATURAL_IMPORT_RUNTIME_WIRING_PLAN.md
```

If working in the Hermes main repo, also read the corresponding main-repo natural import runtime / alias / session files before editing.

## Live Evidence From User Testing

The user tested through OpenWebUI connected to the 8642 Hermes OpenAI-compatible backend.

After the 8642 process was restarted with:

```text
HERMES_NATURAL_IMPORT_REAL_UPLOAD_ENABLED=true
```

real import succeeded:

```text
natural_import_detected=true
real_upload_enabled=true
upload_adapter_status=executed
ingestion_status=upload_succeeded
document_id=2baf5527-42c9-4467-8856-573e54c97121
version_id=b2efc465-cde8-4aef-a113-5c8615929719
chunk_count=6
indexed_count=6
```

But follow-up retrieval failed:

```text
alias_resolution.status=bound_to_document
retrieval_evidence_document_ids=[]
citation=Missing Evidence
```

A manual memory write attempt also failed because ordinary memory was full. That is not the desired storage path: file alias / active document state must not depend on ordinary long-term memory text.

## User Experience Requirement

Natural import must feel like a company-kernel Agent, not an operator ceremony.

The user should be able to say:

```text
帮我导入这个文件。
```

Hermes should:

1. Detect the authorized file path or ask for the file if missing.
2. Import through the real upload adapter when enabled.
3. Generate a safe alias automatically if the user does not provide one.
4. Bind the imported file to session alias / active document state.
5. Reply clearly, for example:

```text
文件我已经记下了。
别名我设定为：@建筑类数据样表
后续你可以用这个别名继续问我。
```

Later, if the user asks:

```text
C塔项目的招标要求文件你帮我找出来。
```

Hermes should use safe fuzzy file discovery over known session/workspace aliases and governed file metadata, then list candidate aliases / safe file refs and ask which one the user means if ambiguous.

## Implementation Scope

Fix only the natural import workspace / alias / retrieval path.

Allowed:

1. Main Hermes runtime code for natural import result handling.
2. Session alias / active document state seeding after successful import.
3. Scoped retrieval from newly imported `document_id` / `version_id`.
4. Deterministic safe alias generation when alias is omitted.
5. Bounded fuzzy alias / file discovery over safe known aliases / metadata.
6. Targeted tests for upload success -> alias -> scoped retrieval.
7. Handoff docs / test prompts sync.

Do not implement broad workspace productization beyond what is required for this fix.

## Hard Boundaries

Do not:

1. Store file alias bindings as ordinary long-term memory text.
2. Treat import diagnostics or upload metadata as retrieval evidence.
3. Answer file content without retrieval citation.
4. Use direct API upload as substitute evidence.
5. Scan NAS, folders, or multiple files.
6. Enable production rollout.
7. Execute repair, cleanup, backfill, reindex, delete, migration, or destructive operations.
8. Modify platform Gateway / DB / NAS Data Steward contracts.
9. Expose raw path, file content, secrets, raw DB rows, or raw answers.
10. Claim DWG/RVT/BIM content understanding.

## Required Tests

Add or update focused tests covering:

1. Import success with explicit alias seeds session alias / active document state.
2. Same-session `@alias` query becomes scoped retrieval for imported `document_id` / `version_id`.
3. Retrieval evidence document ids contain only the imported document.
4. Citation is required; if no retrieval evidence, return Missing Evidence.
5. Import success without alias generates a deterministic safe alias and reports it.
6. Generated alias works for same-session retrieval.
7. Fuzzy file discovery returns safe candidate aliases / file refs and asks for clarification when ambiguous.
8. Alias binding does not require ordinary long-term memory write.
9. Import diagnostics are never treated as retrieval evidence.
10. Safety flags remain false: `metadata_as_answer`, `facts_as_answer`, `snapshot_as_answer`, `transcript_as_fact`.

If the Hermes main repo test environment cannot run full tests, run the narrowest available unit tests plus py_compile / static checks and explain any skipped tests.

## Optional Live Smoke

Do not run real upload smoke unless the user explicitly authorizes the exact file path and confirms the 8642 backend has real upload enabled.

If authorized, use one small non-sensitive file only and verify:

```text
natural_import_detected=true
real_upload_enabled=true
upload_adapter_status=executed/succeeded
ingestion_status=upload_succeeded/completed
document_id present
version_id present
chunk_count > 0
indexed_count > 0
alias_resolution.status=alias_bound or alias_resolved
retrieval_evidence_document_ids=[imported document_id]
citation present
third_document_contamination=false
```

## Expected Output

At the end, report:

1. Files changed.
2. Tests run and results.
3. Whether explicit alias import passes.
4. Whether auto alias generation passes.
5. Whether same-session retrieval returns citation from the imported document.
6. Whether fuzzy file discovery is implemented or deferred with reason.
7. Whether ordinary memory was avoided for alias persistence.
8. Whether Phase 2 closeout remains blocked or can proceed to Codex B / Codex C validation.

Stop after one bounded implementation round. Do not baseline automatically unless Codex B has reviewed and the user policy allows baseline.

# NEXT_CODEX_A_PROMPT

## Phase 2.111 Baseline Complete / Await Natural Import Decision

Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack has passed Codex B review.

Do not implement a new runtime phase automatically.

## Current Decisions

```text
natural_import_technical_path = partially proven
natural_import_live_usability_closeout = not ready
full_phase2_closeout = still blocked
platform_stable_baseline = still valid
```

## What Exists

The reviewed pack contains:

```text
docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md
eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json
docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md
```

The pack confirms:

1. Intent detection, runtime hook, real upload client path, explicit authorization gates, operator checklist, and evidence template are proven or technically supported.
2. Full natural-language import closeout still needs a future accepted Hermes CLI natural-language import smoke, or explicit user exception.
3. Direct API upload cannot substitute for natural-language import usability evidence.
4. Planning / mocked / dry-run evidence cannot substitute for live usability evidence.

## Awaiting User Decision

The next action requires the user to choose one path:

### Path A: Authorize Codex C Natural Import Acceptance Smoke

The user must provide:

```text
<AUTHORIZED_FILE_PATH>
<ALIAS>
<PROJECT_CONTEXT>
```

Then Codex C may execute:

```text
docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md
```

### Path B: Record User Exception

The user may explicitly decide:

```text
Natural-language import usability moves out of Phase 2 closeout and remains post-Phase-2 backlog.
```

If so, create a docs-only exception record before any full Phase 2 closeout claim.

## Hard Boundaries

Do not:

1. Run a real natural-language import smoke without concrete user authorization.
2. Upload files.
3. Use direct API upload as substitute evidence.
4. Connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
5. Execute SQL.
6. Run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
7. Write Hermes memory, facts, documents, chunks, OpenSearch, Qdrant, MinIO, DB, or NAS.
8. Print secrets, raw paths, raw DB rows, raw answers, file contents, or customer data.
9. Declare full Phase 2 completion.
10. Stage unrelated shared mirror files or `docs/digital-delivery-standards/`.

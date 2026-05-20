# NEXT_CODEX_A_PROMPT

## Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack

You are Codex A in the Hermes_memory mainline. This task is docs / matrix / handoff only. Do not implement runtime features.

## Goal

Create a Phase 2.111 closeout pack that turns the natural-language import gap into a concrete acceptance matrix.

The pack must answer:

```text
Which natural-language import capabilities are proven?
Which are only partial / planning / mocked evidence?
Which require a real user-authorized smoke before full Phase 2 closeout?
Which can only move out of Phase 2 by explicit user exception?
```

This phase does not run a real smoke. It prepares the exact evidence matrix and optional Codex C smoke prompt for a future authorized run.

## Required Reading

Read:

```text
docs/PHASE2110_PHASE2_FULL_CLOSEOUT_RETURN_PLAN.md
eval/phase2_inventory/phase2_full_closeout_return_checklist.json
docs/PHASE2102_METRIC_EVALUATION_EVIDENCE_PACK.md
eval/phase2_inventory/phase2_eval_inventory_manifest.json
docs/PHASE2101_PRD_ACCEPTANCE_GAP_CLOSURE_PLAN.md
docs/PHASE253_NATURAL_LANGUAGE_FILE_IMPORT_PLAN.md
docs/PHASE253B_NATURAL_IMPORT_INTEGRATION_PLAN.md
docs/PHASE256_NATURAL_IMPORT_REAL_ADAPTER_PLAN.md
docs/PHASE256B_NATURAL_IMPORT_REAL_SMOKE_PLAN.md
docs/PHASE256D_NATURAL_IMPORT_RUNTIME_WIRING_PLAN.md
docs/PHASE257_NATURAL_IMPORT_MVP_USABILITY_PLAN.md
docs/PHASE259_NATURAL_IMPORT_SECOND_SMOKE_PLAN.md
docs/MAC_MINI_NATURAL_IMPORT_OPERATOR_CHECKLIST.md
scripts/phase257a_natural_import_evidence_template.py
tests/test_phase257a_natural_import_evidence_template.py
docs/PRD.md
docs/ROADMAP.md
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/TODO.md
docs/DEV_LOG.md
```

## Required Outputs

Create:

```text
docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md
eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json
```

Optional, only if useful and still not executed:

```text
docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md
```

Update:

```text
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/HANDOFF_LOG.md
docs/TODO.md
docs/DEV_LOG.md
docs/NEXT_CODEX_A_PROMPT.md
reports/agent_runs/latest.json
```

## Required Matrix Semantics

The JSON matrix must include at least these sections:

```json
{
  "phase": "Phase 2.111 Natural-language Import / MVP Closeout Gap Closure Pack",
  "closeout_decision": "not_ready_until_evidence_or_user_exception",
  "evidence_categories": [
    "proven",
    "partial_evidence",
    "missing_live_evidence",
    "requires_user_authorization",
    "candidate_user_exception"
  ],
  "acceptance_items": []
}
```

Each `acceptance_items` entry must include:

```json
{
  "item_id": "stable_id",
  "name": "human readable name",
  "phase2_requirement": "prd_or_roadmap_requirement",
  "current_status": "proven|partial_evidence|missing_live_evidence|requires_user_authorization|candidate_user_exception",
  "evidence_refs": ["docs/..."],
  "missing_evidence": ["specific missing proof"],
  "closeout_effect": "blocks_full_phase2_closeout|can_close_with_user_exception|informational",
  "required_next_action": "specific next action",
  "forbidden_substitutes": ["direct_api_upload_as_natural_import_success"]
}
```

## Required Acceptance Items

At minimum cover:

1. Natural-language import intent detection.
2. Runtime hook before normal retrieval / answer.
3. Real upload client path.
4. Feature-flag / explicit authorization gate.
5. Hermes CLI natural-language import path, not direct API upload.
6. Document ID / version ID / chunk count / index count returned after real import.
7. Same-session alias persistence.
8. Follow-up retrieval from imported document with citation.
9. Third-document contamination check.
10. Missing Evidence when parser / permission / evidence is absent.
11. No raw path / secret / raw row / customer data output.
12. Mac mini operator checklist readiness.
13. Evidence template / ignored sanitized run record readiness.
14. Employee usability / non-developer operator evidence.
15. Whether this can close Phase 2 full closeout or requires user exception.

## Required Written Conclusions

The Markdown pack must clearly say:

1. Current natural-language import is not yet enough to announce full Phase 2 closeout.
2. Historical real upload smoke is valuable evidence but must be mapped carefully; do not overcount planning / mock / direct API evidence.
3. A future accepted smoke must use Hermes CLI natural-language import path.
4. Direct API upload cannot substitute for natural-language import usability.
5. Full closeout requires either a new accepted natural-language import smoke or explicit user exception moving this gap out of Phase 2.
6. Platform stable baseline remains valid and separate.
7. This phase does not authorize production rollout, full NAS scan, DB write, parser/index write, or arbitrary file ingestion.

## Optional Codex C Smoke Prompt Requirements

If you create `docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md`, it must:

1. Contain placeholders for `<AUTHORIZED_FILE_PATH>`, `<ALIAS>`, and `<PROJECT_CONTEXT>`.
2. State that it cannot be executed until the user explicitly authorizes a specific small non-sensitive file.
3. Require Hermes CLI natural-language import path.
4. Forbid direct API upload as substitute evidence.
5. Require sanitized report fields only.
6. Forbid raw path / raw text / secret / raw DB row output.
7. Stop on parser unavailable, permission missing, upload disabled, alias not persisted, retrieval not citation-backed, third-document contamination, or any forbidden output.

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m py_compile scripts/phase257a_natural_import_evidence_template.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run pytest tests/test_phase257a_natural_import_evidence_template.py
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short
```

If pytest is unavailable in the local environment, do not install dependencies automatically. Report it as blocked / skipped with exact reason.

## Hard Boundaries

Do not:

1. Modify runtime code.
2. Modify existing tests except only if needed to keep docs-only validation references accurate; prefer no test changes.
3. Run a real natural-language import smoke.
4. Upload files.
5. Connect to DB, NAS, Gateway, API, OpenSearch, Qdrant, MinIO, or platform services.
6. Execute SQL.
7. Run parser, writer, scratch copy, repair, backfill, reindex, delete, migration, or rollout.
8. Write Hermes memory, facts, documents, chunks, OpenSearch, Qdrant, MinIO, DB, or NAS.
9. Print secrets, raw paths, raw DB rows, raw answers, file contents, or customer data.
10. Declare full Phase 2 completion.
11. Stage unrelated shared mirror files or `docs/digital-delivery-standards/`.

## Baseline Scope

Allowed files for selective staging:

```text
docs/PHASE2111_NATURAL_IMPORT_MVP_CLOSEOUT_GAP_CLOSURE_PACK.md
eval/phase2_inventory/natural_import_mvp_closeout_gap_matrix.json
docs/CODEX_C_NATURAL_IMPORT_ACCEPTANCE_SMOKE_PROMPT.md
docs/ACTIVE_PHASE.md
docs/PHASE_BACKLOG.md
docs/HANDOFF_LOG.md
docs/TODO.md
docs/DEV_LOG.md
docs/NEXT_CODEX_A_PROMPT.md
```

Optional if changed in the same reviewed work:

```text
reports/agent_runs/latest.json
```

Stop after completing Phase 2.111 and updating handoff. Do not enter Phase 2.112 or Phase 3 without explicit user instruction.

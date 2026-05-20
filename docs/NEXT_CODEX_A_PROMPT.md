# NEXT_CODEX_A_PROMPT

## Phase 2.104d Codex B Review / Docs + Fixture Baseline Gate

You are Codex A. Do not implement Phase 2.104e automatically.

## Current State

Phase 2.104d docs / fixture planning has been completed locally:

1. `docs/PHASE2104D_FEEDBACK_SCORING_LINKAGE_CONTRACT.md`
2. `eval/phase2_inventory/feedback_scoring_linkage_examples.json`
3. updated `docs/ACTIVE_PHASE.md`
4. updated `docs/PHASE_BACKLOG.md`
5. updated `docs/HANDOFF_LOG.md`
6. updated `docs/TODO.md`
7. updated `docs/DEV_LOG.md`
8. updated ignored `reports/agent_runs/latest.json`

No runtime code, tests, scoring scripts, feedback ingestion, issue creation, memory writes, facts writes, DB, NAS, Gateway, OpenSearch, Qdrant, MinIO, or repair implementation was changed.

## Review Checklist

Codex B should verify:

1. Feedback is consistently described as evaluation / triage signal, not evidence.
2. Feedback never becomes permission proof, content evidence, facts, repair, or automatic metric pass.
3. Allowed labels include:
   - `helpful`
   - `wrong_document`
   - `missing_evidence`
   - `wrong_boundary`
   - `citation_problem`
   - `permission_problem`
   - `overclaim`
   - `needs_human_review`
   - `irrelevant_result`
4. Sanitized input shape excludes:
   - raw user note text
   - raw answer text
   - raw path / storage path / NAS path
   - raw DB row
   - raw catalog row
   - secret / token / credential / `.env`
   - customer-sensitive material
5. Scoring linkage requires reviewed sanitized result rows before official metric effect.
6. `helpful` cannot auto-pass a metric.
7. `wrong_document`, `citation_problem`, `missing_evidence`, `wrong_boundary`, `overclaim`, `permission_problem`, and `irrelevant_result` are review candidates only.
8. Memory linkage is limited to low-sensitive hints after review.
9. Fixtures cover:
   - `feedback_helpful_positive_signal_no_auto_pass`
   - `feedback_wrong_document_topk_candidate`
   - `feedback_citation_problem_candidate`
   - `feedback_missing_evidence_candidate`
   - `feedback_wrong_boundary_forbidden_behavior_candidate`
   - `feedback_permission_problem_fail_closed_candidate`
   - `feedback_overclaim_requires_review`
   - `feedback_sensitive_note_rejected`
   - `feedback_low_sensitive_memory_hint_after_review`
10. Fixtures use sanitized fake IDs only and contain no raw text/path/row/secret/customer-sensitive content.

## Validation Commands

Run:

```bash
git diff --check
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool reports/agent_runs/latest.json >/dev/null
UV_CACHE_DIR=/private/tmp/uv-cache uv run python -m json.tool eval/phase2_inventory/feedback_scoring_linkage_examples.json >/dev/null
git check-ignore reports/agent_runs/latest.json
git status --short --untracked-files=all
```

Do not run pytest for this phase. This is docs / fixture planning only.

## Optional Baseline Command

Only if the user explicitly authorizes baseline after review:

1. Stage only Phase 2.104d docs / fixture / handoff files.
2. Do not stage unrelated `docs/digital-delivery-standards/` files.
3. Commit message:

```text
docs: add phase 2.104d feedback scoring linkage contract
```

4. Tag:

```text
phase-2.104d-feedback-scoring-linkage-contract-baseline
```

5. Push `origin/main` and tag.

## Hard Boundaries

1. Do not modify runtime code.
2. Do not modify tests.
3. Do not modify scoring scripts.
4. Do not implement feedback ingestion.
5. Do not write Hermes memory.
6. Do not write facts.
7. Do not create issues automatically.
8. Do not implement repair / DB writes / NAS scan / parser / indexing / Gateway integration.
9. Do not run API / CLI / Gateway / DB / NAS smoke.
10. Do not connect to DB / NAS / Gateway.
11. Do not execute SQL.
12. Do not read or output raw rows, NAS paths, storage paths, raw answer text, secrets, tokens, or `.env` values.
13. Do not enter Phase 3 or production rollout.
14. Do not stage unrelated `docs/digital-delivery-standards/`.

## Stop Condition

After review or baseline, stop and report:

1. changed files;
2. validation result;
3. whether shared docs were readable;
4. key feedback / scoring linkage boundary conclusion;
5. risks / blockers;
6. whether Codex B review is complete;
7. whether baseline was authorized and completed.

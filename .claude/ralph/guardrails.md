# Ralph Guardrails

### Sign: DB-2 Boundary Drift

- **Trigger:** Any change proposes real MySQL, NAS, REST, migrations, ORM models, `documents` / `chunks`, OpenSearch, Qdrant, retrieval adapters, or memory-kernel architecture for DB-2.
- **Instruction:** Stop and record an OPEN finding unless the user has explicitly authorized implementation after Codex review.
- **Added after:** DB-1a baseline established a fake View adapter contract and DB-2 was limited to planning only.

### Sign: Validation Without Evidence

- **Trigger:** The agent is ready to report completion.
- **Instruction:** Run `npm test` and `npm run lint` first, then verify `.claude/ralph/findings.md` has no OPEN findings before emitting `RALPH_AUDIT_COMPLETE_NO_FINDINGS`.
- **Added after:** Ralph loop setup requires verification-first exit.

# Internal MVP Issue Records

This directory is for local internal MVP operator issue records.

Real issue JSON, Markdown notes, screenshots, logs, spreadsheets, documents, and copied terminal evidence are ignored by default and must not be committed.

Recommended local write path:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py \
  --new-template \
  --output-json reports/internal_mvp_issues/<local-file>.json
```

Issue records may contain query text, operator judgement, document IDs, citation IDs, local paths, customer context, project context, and internal business assessment. Treat them as local sensitive artifacts.

If a record needs to become tracked documentation, Codex B must first produce a sanitized summary. Do not commit the raw record.

This directory is not an external issue tracker. It does not create Linear issues, GitHub issues, or any other external task.

This directory does not authorize repair, cleanup, delete, backfill, reindex, migration, database writes, index writes, or rollout.

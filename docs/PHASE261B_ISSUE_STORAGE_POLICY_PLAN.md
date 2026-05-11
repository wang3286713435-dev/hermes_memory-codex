# Phase 2.61b Local Issue Storage Policy Plan

## 1. Goal

Phase 2.61b plans the local storage policy for internal MVP operator issue records.

Phase 2.61a added a dry-run issue intake helper. Real operator issue records may include sensitive query text, business judgement, document IDs, citations, paths, customer context, project context, and internal assessment notes. They must be local-first and ignored by Git by default.

This phase is docs-only planning. It does not write code, upload files, run API or CLI smoke, write DB or index state, create external issues, execute repair, or enter production rollout.

## 2. Recommended Directory

Recommended local issue record directory:

```text
reports/internal_mvp_issues/
```

Suggested future layout:

```text
reports/internal_mvp_issues/
  README.md
  .gitignore
  YYYYMMDD_<session_id>_<severity>_<short_issue_id>.json
  YYYYMMDD_<session_id>_summary.md
```

Only `README.md` and `.gitignore` should be candidates for Git tracking in a future phase.

Real issue JSON / Markdown records must remain untracked and ignored by default.

## 3. Git Policy

Default policy:

1. Do not commit real issue JSON.
2. Do not commit real operator Markdown notes.
3. Do not commit raw query logs.
4. Do not commit customer / project / file path details from live use.
5. Do not commit reports generated from real internal MVP sessions.
6. Commit only directory policy files such as `README.md`, `.gitignore`, or sanitized templates.

Recommended ignore policy for a future Phase 2.61c:

```gitignore
*.json
*.md
!README.md
!.gitignore
```

If a sanitized summary is needed for documentation, Codex B must review it first and strip sensitive details before it enters tracked docs.

## 4. Writing Records

The Phase 2.61a helper must remain explicit-path only:

```bash
uv run python scripts/phase261a_mvp_issue_intake.py \
  --new-template \
  --output-json reports/internal_mvp_issues/<local-file>.json
```

The helper should not automatically choose a persistent directory.

Operators are responsible for selecting a local ignored path and checking the record before sharing any summary.

## 5. Record Sensitivity

Issue records may contain:

1. query text.
2. expected / actual behavior.
3. operator judgement.
4. document IDs and version IDs.
5. evidence chunk IDs.
6. citations.
7. customer or project context.
8. local source paths.
9. business risk notes.
10. screenshots or copied terminal snippets if the operator adds them manually.

Because of this, true records must be treated as local sensitive artifacts.

## 6. Review Flow

1. Operator creates or validates a local issue JSON with the Phase 2.61a helper.
2. Operator keeps the record under an ignored path.
3. Codex B reviews the issue status and decides whether the problem becomes:
   - implementation fix prompt.
   - retrieval quality tail.
   - display / trace tail.
   - operator guidance update.
   - out-of-scope backlog item.
4. Codex A only receives bounded prompts derived from reviewed issue summaries.
5. Codex C only receives explicit validation prompts.

## 7. Phase 2.61c Candidate

Recommended next implementation candidate:

Phase 2.61c: local issue records directory policy.

Minimum boundary:

1. add `reports/internal_mvp_issues/.gitignore`.
2. add `reports/internal_mvp_issues/README.md`.
3. optionally add a sanitized example template that contains no real query, document ID, path, customer, or project data.
4. update operator checklist.

Non-goals:

1. no issue DB.
2. no external issue creation.
3. no Linear or GitHub issue automation.
4. no report upload.
5. no repair executor.
6. no production rollout.

## 8. Non-Goals

Phase 2.61b does not:

1. implement storage files.
2. write any real issue record.
3. write DB / facts / document_versions / audit_logs.
4. write OpenSearch / Qdrant / MinIO.
5. create external issues.
6. execute cleanup, delete, repair, backfill, reindex, or migration.
7. run API / CLI smoke.
8. upload files.
9. enter Data Steward / DB / NAS / BIM / TB file pool.
10. enter production rollout.

## 9. Current Recommendation

Phase 2.61b should not block Mac mini internal MVP use.

It should guide where real issue records live and how they stay out of Git. If Codex B accepts this plan, Phase 2.61c can add the ignored directory policy files only.

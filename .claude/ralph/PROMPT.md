# Ralph Loop: DB-2 Boundary Guard

## Mission

Keep DB-2 aligned with the documented Data Steward asset-catalog boundary while making only the minimal fixes needed for validation to pass.

## Before Doing Anything

1. Read `.claude/context/memory/learnings.md`.
2. Read `.claude/ralph/guardrails.md`.
3. Read previous findings in `.claude/ralph/findings.md` if it exists.
4. Read `docs/DATA_STEWARD_BRANCH_ROADMAP.md`, `docs/DB_BRANCH_ACCEPTANCE_AND_MERGE_CHECKLIST.md`, `docs/DB2_ASSET_CATALOG_MIRROR_PLAN.md`, and `docs/ACTIVE_PHASE.md`.

## Scope

### 1. Validation Failures Only

- Run `npm test` and `npm run lint`.
- If either command fails, fix only failures directly related to `tests/` or the existing DB-1 asset-catalog source surface.
- Allowed source surfaces are `tests/`, `app/services/asset_catalog/`, and `app/core/config.py`.

### 2. DB-2 Boundary Audit

- Confirm no implementation crosses the DB-2 planning boundary.
- Do not add migrations, ORM models, real platform clients, retrieval adapters, indexing code, or document ingestion code.
- Do not connect real MySQL, NAS, REST, OpenSearch, or Qdrant.
- Do not write to `documents`, `chunks`, OpenSearch, Qdrant, or any real DB/index.
- Do not scan `/Volumes/zyzn/卓羽智能项目`.
- Treat missing `permission_tags` as default deny.
- Keep asset-catalog-only records separate from document evidence and Missing Evidence.

### 3. Git / Baseline Boundary

- Do not create commits, tags, branches, or baselines.
- Do not switch branches.
- Report findings and validation output only.

## Validation Commands

```bash
npm test
npm run lint
```

## Findings Log

Write findings to `.claude/ralph/findings.md`.

Use this format:

```markdown
### FINDING-001: Boundary short title
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW
- **File:** path/to/file
- **Problem:** What is wrong
- **Status:** OPEN | FIXED_THIS_ITERATION
```

If there are no findings, keep the file present with:

```markdown
# Ralph Findings

No OPEN findings.
```

## Completion Condition

If findings remain open:

```text
RALPH_ITERATION_COMPLETE: N findings remain open.
```

If all findings are fixed and both validation commands pass:

```text
RALPH_AUDIT_COMPLETE_NO_FINDINGS
```

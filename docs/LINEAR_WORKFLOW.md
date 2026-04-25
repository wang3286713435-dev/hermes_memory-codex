# Hermes Memory Linear Lightweight Workflow

## Purpose

Use Linear as the lightweight execution board across Codex A, Codex B, and the user.

Goals:
- Track work across both repos without deep integration.
- Make Codex A -> Codex B -> user coordination short and reliable.
- Keep code details in git and task state in Linear.

## Current Linear Baseline

- Workspace: `Hermes_memory`
- Team: `HER`
- Project created: `MVP Retrieval Closure`
- Project state: `started`
- Project created: `Phase 2.10 Enterprise Agent Scope`
- Project state: `started`
- Non-dev onboarding seeds: `HER-1` to `HER-4` are canceled and labeled `non-dev:onboarding`
- Completed framework anchor: `HER-5 Linear framework: Codex A/B handoff protocol`
- Anchor URL: `https://linear.app/hermes-memory/issue/HER-5/linear-framework-codex-ab-handoff-protocol`
- Project PRD source: `docs/LINEAR_PROJECT_PRD.md`
- Active execution issue: `HER-6 Phase 2.9c: 总工期/关键节点召回与高可信灰度补证`
- Real execution issue map:
  - `HER-6` active schedule/key-node retrieval and high-confidence validation
  - `HER-7` next contract commercial parameter retrieval
  - `HER-8` dense ingestion for uploaded chunks
  - `HER-9` real tender retrieval evaluation set
  - `HER-10` Linear project PRD/progress maintenance and cross-project guardrail
  - `HER-11` active Phase 2.10 PRD/Roadmap enterprise Agent scope alignment
  - `HER-12` staged multimodal ingestion plan
  - `HER-13` meeting memory pilot and governance boundary
  - `HER-14` Codex B review of Phase 2.10 scope boundary
- Default workflow statuses:
  - `Backlog`
  - `Todo`
  - `In Progress`
  - `In Review`
  - `Done`
  - `Canceled`
  - `Duplicate`

## API Access

Use the local Linear API key for routine project maintenance.

- Load credentials with `source ~/.hermes/linear.env`.
- Do not print or commit `LINEAR_API_KEY`.
- Prefer GraphQL API calls over browser automation for reading issues, labels, statuses, and writing comments or issue updates.
- Use browser automation only when the API lacks the needed capability or the user explicitly asks for visual confirmation.

## Project Rule

Use delivery-oriented projects by capability:

- `MVP Retrieval Closure`
- `Phase 2.10 Enterprise Agent Scope`

Do not split projects by repo yet.
Use labels to distinguish repo and execution environment.

For onboarding a new Codex implementation session, start from the assigned concrete issue. If no issue is provided, start from the current active issue:

- `HER-6` for Phase 2.9c retrieval closure.
- `HER-11` for Phase 2.10 PRD/Roadmap scope alignment.

For Codex B project hygiene or prompt-writing sessions, start from `HER-10`.

Use `HER-5` only as historical framework context; it is not an active development issue.

For project-level context, read `docs/LINEAR_PROJECT_PRD.md` before creating or reshaping issues.

## Recommended Labels

Use the following label set as the long-term standard:

- `repo:memory-codex`
- `repo:hermes-repo`
- `repo:cross-repo`
- `env:mac`
- `env:windows`
- `role:codex-a`
- `role:codex-b`
- `handoff:ready`
- `handoff:needs-sync`
- `track:mvp-retrieval-closure`
- `track:enterprise-agent-scope`
- `phase:2.9c`
- `phase:2.10`

Optional labels if issue volume grows:

- `area:retrieval`
- `area:integration`
- `area:evaluation`
- `area:runbook`
- `area:indexing`
- `area:linear-ops`
- `area:product-scope`
- `area:multimodal-ingestion`
- `area:meeting-memory`
- `non-dev:onboarding`
- `framework:linear`

## Linear Intervention Rule

Linear must be part of the work loop, not an after-the-fact note.

- Start rule: before substantial Codex A/B work, read the active Linear issue and its refs.
- Missing issue rule: if work has no matching issue, create one or ask for one before continuing substantial implementation or planning.
- End rule: after each work session, add one short Linear comment with current state, evidence, blocker if any, next action, and refs.
- Drift rule: if local docs/code indicate a new phase or workstream, update Linear during the same session.
- Noise rule: do not mirror every commit or paste large logs; use Linear for milestones, blockers, handoffs, reviews, and completion.

## Issue Structure

Every cross-device or cross-repo issue should use this structure:

```md
Context:
- What goal this issue serves.

Current state:
- What is already done.

Why handoff:
- Why this needs another machine, repo, or owner now.

Next action:
- The first concrete thing the next Codex should do.

Done when:
- Clear completion criteria.

Refs:
- Repo
- Branch
- Commit
- Key files
- Commands or scripts if needed
```

## Update Frequency

Do not update Linear for every code change.

Update Linear only when one of these happens:

1. A new task starts.
2. The task becomes blocked.
3. Work is handed between Codex A, Codex B, the user, or another execution environment.
4. A milestone is completed.
5. The issue is closed.

## Status Rules

- `Backlog`: valid work, not in the current batch.
- `Todo`: ready to start with clear scope.
- `In Progress`: someone is actively working on it.
- `In Review`: waiting for validation, review, or test confirmation.
- `Done`: code and required validation are complete.
- `Canceled`: intentionally dropped.
- `Duplicate`: superseded by another issue.

## Handoff Rule

Before handoff from Codex A to Codex B, the user, or another execution context:

- Push or save work to a branch when possible.
- Update the issue body or a comment using the standard structure.
- Add the relevant role or environment label for the next owner.
- Add `handoff:ready` when the next Codex can start immediately.

After receiving handoff:

- Read the full issue first.
- Confirm repo, branch, and machine intent from `Refs`.
- Move the issue to `In Progress`.
- Remove `handoff:ready` when active work begins.
- Add a short completion or blocker comment before handing back.

## Codex B Co-Pilot Rule

Codex B is not the Windows-side executor by default.

Codex B should primarily:

- Monitor Codex A's work and Linear issue freshness.
- Write concise next-step prompts for the user or Codex A.
- Review changed files, tests, blockers, and risks.
- Keep issue context actionable without mirroring every code change.
- Fix only small bounded bugs when the issue context is clear or the user asks.

Codex B should avoid taking over Codex A's main implementation thread unless explicitly asked.

## First Use Path

1. Open the assigned concrete issue. If none is provided, open `HER-6` for Phase 2.9c, `HER-11` for Phase 2.10, or `HER-10` for Codex B project hygiene.
2. Confirm the active project is either `MVP Retrieval Closure` or `Phase 2.10 Enterprise Agent Scope`.
3. Confirm `HER-1` to `HER-4` are ignored as canceled onboarding seeds and `HER-5` is historical framework context only.
4. Add repo and environment labels only when they describe the next action.
5. Keep Git as the code source of truth and Linear as the task/handoff source of truth.

## Scope Boundary

Linear is the execution board, not the source of truth for code.

- Code lives in git.
- Technical detail lives in code, tests, and docs.
- Linear stores task intent, status, blockers, and handoff context.

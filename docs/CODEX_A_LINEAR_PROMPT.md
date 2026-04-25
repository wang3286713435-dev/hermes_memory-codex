# Codex A Linear Prompt

You are Codex A working mainly from the current machine.

Use Linear as the lightweight execution board for Hermes Memory.

Default entry:
- Start from the assigned Linear issue. If no more specific issue is provided, start from `HER-6` for Phase 2.9c retrieval closure or `HER-11` for Phase 2.10 PRD/Roadmap scope alignment.
- Use project `MVP Retrieval Closure` for Phase 2.9c retrieval work.
- Use project `Phase 2.10 Enterprise Agent Scope` for Phase 2.10 product-scope, multimodal ingestion, meeting memory, and governance-boundary work.
- Read `/Users/Weishengsu/Hermes_memory/docs/LINEAR_PROJECT_PRD.md` for current project PRD, progress, and first-batch issue structure.
- Treat `HER-1` to `HER-4` as canceled Linear onboarding seeds.
- Treat `HER-5` as completed framework context, not active implementation work.

Rules:
- Read the relevant Linear issue before starting work.
- If your work has no matching Linear issue, create or request one before continuing substantial work.
- Treat Linear as the task source of truth, not the code source of truth.
- Keep code changes in git and task state in Linear.
- When you need Codex B review, user guidance, or machine-specific validation, update the issue instead of writing a long handoff prompt.
- At the end of each work session, add one concise Linear comment with current state, evidence, blocker if any, next action, and refs.

Workflow:
1. Read the issue title, body, labels, status, and project.
2. Identify repo scope from `repo:*` labels.
3. Work locally until you hit a machine-specific blocker or finish your milestone.
4. If handing off, update the issue with:
   - `Context`
   - `Current state`
   - `Why handoff`
   - `Next action`
   - `Done when`
   - `Refs`
5. Add `role:codex-b` if Codex B should review, monitor, or write the next prompt.
6. Add `env:windows` only if a Windows-specific validation or execution step is actually needed.
7. Add `handoff:ready` only when the next Codex can act immediately.
8. Move the issue status to match reality.

Do not:
- Mirror every commit into Linear.
- Paste large logs unless they are necessary.
- Leave the next Codex guessing which repo, branch, or file matters.

Use short, operational updates.

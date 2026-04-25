# Hermes Memory Linear Project PRD

## Linear Target

- Workspace: `Hermes_memory`
- Team: `HER`
- Project: `MVP Retrieval Closure`
- Project state: `started`
- Project: `Phase 2.10 Enterprise Agent Scope`
- Project state: `started`
- Non-dev onboarding seeds: `HER-1` to `HER-4` are canceled and labeled `non-dev:onboarding`
- Completed framework anchor: `HER-5 Linear framework: Codex A/B handoff protocol`
- Anchor URL: `https://linear.app/hermes-memory/issue/HER-5/linear-framework-codex-ab-handoff-protocol`

## Product Intent

Hermes Memory upgrades the existing Hermes agent into an enterprise long-term memory kernel.

The MVP is not a larger chat window and not a vector database demo. The MVP must prove a reliable enterprise knowledge QA loop:

- Ingest representative enterprise documents.
- Parse and chunk documents with structure preserved.
- Index chunks into dense and sparse retrieval backends.
- Retrieve with hybrid search, metadata filters, rerank, version awareness, and permission boundaries.
- Answer with traceable citations.
- Evaluate retrieval quality and rollout readiness with repeatable scripts.

## Current Phase

Current active phases:

- `Phase 2.9c`: retrieval closure and rollout-readiness evidence.
- `Phase 2.10`: PRD/Roadmap expansion toward enterprise Agent scope, multimodal ingestion, meeting memory, and governance boundaries.

Phase 2.9c goal:

- Close the retrieval quality gap for large real tender documents.
- Keep the existing local rerank default-enable baseline stable.
- Collect higher-confidence validation evidence before any broader rollout.

Phase 2.9c is not:

- Production rollout.
- Global rerank enablement.
- Full AI tender-review automation.
- Full enterprise long-term memory completion.

Phase 2.10 goal:

- Align PRD and ROADMAP with Hermes as an enterprise Agent kernel, not just a document retriever.
- Define staged multimodal ingestion and meeting memory direction without prematurely committing implementation.
- Preserve governance boundaries: citations, permissions, auditability, evaluation, and human confirmation.

Phase 2.10 is not:

- Immediate implementation of Excel, PowerPoint, audio, image, and meeting-memory pipelines.
- A replacement for Phase 2.9c retrieval closure.
- A license to bypass permission, audit, citation, or human-confirmation boundaries.

## Current Progress

Completed or stable enough:

- Dense/hybrid retrieval contract and trace shape are established.
- Qdrant dense retriever path exists and query-vector / embedding paths have been exercised in earlier gates.
- OpenSearch sparse indexing and retrieval are wired into the retrieval service.
- Rerank hook, candidate pool, fail-open behavior, and Aliyun Text Rerank adapter are implemented.
- Local default rerank enablement is limited to high-value tender queries.
- Phase 2.8 local baseline and runbook evidence exist.
- Real-file testing has proven single-file retrieval, multi-file isolation, Hermes integration, and large tender ingestion/search can work.
- `db=None` compatibility regression in `RetrievalService.search()` has been fixed for validation scripts.

Still open or not stable enough:

- `总工期 / 关键节点` retrieval remains the highest-priority quality gap.
- Contract/commercial parameters are improving but not yet stable enough: payment nodes, settlement, defect liability, retention, delay penalty.
- High-confidence long-window validation is not complete.
- Dense ingestion for uploaded chunks is not connected end-to-end.
- Full PRD capabilities remain incomplete: structured facts, conversation memory, permission governance, incremental update loop, audit loop, full evaluation system, version governance, knowledge admin workflow, and human verification.

## Linear Operating Model

Use `MVP Retrieval Closure` as the delivery project.

Do not split projects by repository yet. Use labels for ownership, repo scope, phase, and capability area.

`HER-5` is completed framework context. It should not be treated as a concrete implementation task.

Concrete implementation work starts at `HER-6` and should happen in separate issues under the same project.

Routine Linear reads and updates should use the local GraphQL API key from `~/.hermes/linear.env`. Browser automation is a fallback, not the default path.

Linear intervention rule:

- Before substantial Codex A/B work, read the active Linear issue.
- If work has no matching issue, create or request one before continuing.
- After each session, leave one concise Linear comment with current state, evidence, blocker if any, next action, and refs.
- If local docs/code move to a new phase, update Linear in the same session.

## Recommended Labels

Repo labels:

- `repo:memory-codex`
- `repo:hermes-repo`
- `repo:cross-repo`

Role labels:

- `role:codex-a`
- `role:codex-b`

Phase / track labels:

- `track:mvp-retrieval-closure`
- `track:enterprise-agent-scope`
- `phase:2.9c`
- `phase:2.10`
- `phase:rollout-readiness`

Area labels:

- `area:retrieval`
- `area:indexing`
- `area:evaluation`
- `area:runbook`
- `area:governance`
- `area:linear-ops`
- `area:product-scope`
- `area:multimodal-ingestion`
- `area:meeting-memory`

Handoff labels:

- `handoff:ready`
- `handoff:needs-sync`

Environment labels:

- `env:mac`
- `env:windows`

Use `env:windows` only when Windows-specific validation or execution is actually required.

## Recommended Status Rules

- `Backlog`: valid but not in the immediate execution batch.
- `Todo`: ready to start with clear scope.
- `In Progress`: active work is happening now.
- `In Review`: waiting for validation, review, or user confirmation.
- `Done`: implementation and required validation are complete.
- `Canceled`: intentionally dropped.
- `Duplicate`: superseded by another issue.

## First Issue Batch

Current Linear issue map:

- `HER-6`: `Phase 2.9c: 总工期/关键节点召回与高可信灰度补证` (`In Progress`)
- `HER-7`: `Phase 2.9c: stabilize contract commercial parameter retrieval` (`Todo`)
- `HER-8`: `Connect dense ingestion for uploaded chunks` (`Backlog`)
- `HER-9`: `Expand retrieval evaluation set for real tender queries` (`Backlog`)
- `HER-10`: `Keep Linear project PRD, progress, and next actions current` (`Todo`)
- `HER-11`: `Phase 2.10: align PRD/Roadmap with enterprise Agent scope` (`In Progress`)
- `HER-12`: `Phase 2.10: define staged multimodal ingestion plan` (`Todo`)
- `HER-13`: `Phase 2.10: define meeting memory pilot and governance boundary` (`Todo`)
- `HER-14`: `Codex B: review Phase 2.10 scope boundary and keep Linear in sync` (`Todo`)
- `HER-5`: `Linear framework: Codex A/B handoff protocol` (`Done`, framework context)
- `HER-1` to `HER-4`: Linear onboarding seed issues (`Canceled`, non-development)

### P0: Stabilize schedule / critical milestone retrieval

Title:

`Phase 2.9c: stabilize 总工期 / 关键节点 retrieval`

Created issue:

- `HER-6`: `Phase 2.9c: 总工期/关键节点召回与高可信灰度补证`

Labels:

- `repo:memory-codex`
- `phase:2.9c`
- `track:mvp-retrieval-closure`
- `area:retrieval`
- `role:codex-a`

Context:

- Current schedule queries can enter `schedule_scope`, but top results still drift into technical requirements, bid forms, or quantity-list context.
- This blocks Phase 2.9c closeout because schedule and critical milestone fields are core tender-review parameters.

Next action:

- Inspect `RetrievalService._infer_section_scope()` and OpenSearch sparse scoring around `schedule_scope`.
- Add or adjust structure-aware retrieval signals that favor front matter, schedule clauses, and contract duration chunks without breaking existing qualification/commercial/pricing scopes.
- Add targeted regression coverage for schedule queries.

Done when:

- Schedule queries move from "obviously not stable" to at least "improved but still under observation".
- Existing qualification and pricing query behavior does not regress.
- Trace clearly shows schedule-specific scope, aliases, and target-section influence.

Refs:

- `/Users/Weishengsu/Hermes_memory/app/services/retrieval/service.py`
- `/Users/Weishengsu/Hermes_memory/tests/test_retrieval_contract.py`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE29_ROLLOUT_READINESS.md`

### P0: Stabilize contract commercial parameter retrieval

Title:

`Phase 2.9c: stabilize contract commercial parameter retrieval`

Created issue:

- `HER-7`

Labels:

- `repo:memory-codex`
- `phase:2.9c`
- `track:mvp-retrieval-closure`
- `area:retrieval`
- `role:codex-a`

Context:

- Payment, settlement, defect liability, retention, and delay penalty queries now approach contract supplement sections but still often hit neighboring clauses.

Next action:

- Refine `commercial_scope` target sections and aliases.
- Improve ranking separation between exact target clauses and neighboring final-settlement / general liability clauses.
- Add regression cases that protect contract parameter retrieval.

Done when:

- Commercial parameter queries consistently hit the intended contract-related section family.
- Top results become cleaner and less dominated by adjacent but non-answer chunks.

Refs:

- `/Users/Weishengsu/Hermes_memory/app/services/retrieval/service.py`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE29_ROLLOUT_READINESS.md`

### P0: Run high-confidence validation window

Title:

`Phase 2.9c: execute high-confidence long-window validation`

Current Linear placement:

- Included in `HER-6` as the validation half of the active Phase 2.9c closeout issue.
- Split into a separate issue only if a dedicated high-performance validation owner or machine is available.

Labels:

- `repo:memory-codex`
- `phase:2.9c`
- `phase:rollout-readiness`
- `track:mvp-retrieval-closure`
- `area:evaluation`
- `area:runbook`
- `env:windows`

Context:

- Air 8GB can run short and medium windows, but it should not be treated as the final high-confidence validation machine.
- Phase 2.9c still lacks high-confidence long-window and continuous real-workflow evidence.

Next action:

- Run `scripts/phase26_rerank_gray_validation.py` on a higher-confidence machine.
- Capture `rerank_hit_rate`, `fail_open_rate`, `dense_failed_count`, `sparse_failed_count`, `p95`, `p99`, target hit set, false positives, and drift.
- Record results back into Phase 2.9 readiness docs and the Linear issue.

Done when:

- A repeatable high-confidence validation result is recorded.
- Result either supports continued Phase 2.9c closeout work or clearly identifies remaining runtime blockers.

Refs:

- `/Users/Weishengsu/Hermes_memory/scripts/phase26_rerank_gray_validation.py`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE29_ROLLOUT_READINESS.md`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE28_RERANK_LONGRUN.md`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE27_RERANK_RUNBOOK.md`

### P1: Connect dense ingestion for uploaded chunks

Title:

`Connect dense ingestion for uploaded chunks`

Created issue:

- `HER-8`

Labels:

- `repo:memory-codex`
- `track:mvp-retrieval-closure`
- `area:indexing`
- `area:retrieval`

Context:

- Real-file testing currently relies primarily on sparse / OpenSearch.
- Dense ingestion into Qdrant is still not connected end-to-end for uploaded chunks.

Next action:

- Trace the ingestion pipeline from parsed chunks to `OpenSearchChunkIndexer` and Qdrant upsert.
- Define the minimum safe dense-ingestion path without mixing it into Phase 2.9c retrieval-quality closeout.

Done when:

- Uploaded chunks can be embedded and upserted to Qdrant in a repeatable path.
- Dense/hybrid retrieval can be validated against uploaded real-file chunks.

Refs:

- `/Users/Weishengsu/Hermes_memory/app/services/indexing/opensearch.py`
- `/Users/Weishengsu/Hermes_memory/app/services/retrieval/dense.py`
- `/Users/Weishengsu/Hermes_memory/docs/TODO.md`

### P1: Expand retrieval evaluation set for real tender queries

Title:

`Expand retrieval evaluation set for real tender queries`

Created issue:

- `HER-9`

Labels:

- `repo:memory-codex`
- `phase:2.9c`
- `track:mvp-retrieval-closure`
- `area:evaluation`

Context:

- Current golden queries are useful but still not enough to represent large real tender review coverage.
- Phase 2.9c needs targeted samples for schedule, commercial, qualification, pricing, citation, and multi-file switching.

Next action:

- Add or draft a small targeted eval set for unresolved real-tender retrieval gaps.
- Keep samples low-sensitive or desensitized.

Done when:

- Evaluation can separately report schedule, commercial, qualification, pricing, and multi-file-switch behavior.
- The eval set supports regression protection before broader rollout discussion.

Refs:

- `/Users/Weishengsu/Hermes_memory/eval/golden_queries/rerank_phase23.yaml`
- `/Users/Weishengsu/Hermes_memory/docs/PHASE29_ROLLOUT_READINESS.md`

### P1: Keep Linear project state current

Title:

`Keep Linear project PRD, progress, and next actions current`

Created issue:

- `HER-10`

Labels:

- `repo:cross-repo`
- `track:mvp-retrieval-closure`
- `area:linear-ops`
- `role:codex-b`

Context:

- Linear should serve as the lightweight execution panel across Codex A, Codex B, and the user.
- Codex B is a project co-pilot, not a Windows executor.

Next action:

- Keep `HER-5` as the framework anchor.
- Keep concrete work in separate issues.
- After each milestone, blocker, or handoff, summarize state in Linear without mirroring every commit.

Done when:

- User can ask Codex B for project state and get a reliable answer from Linear plus local docs.
- Codex A can start from a specific issue without needing a long prompt.

Refs:

- `/Users/Weishengsu/Hermes_memory/docs/LINEAR_WORKFLOW.md`
- `/Users/Weishengsu/Hermes_memory/docs/CODEX_A_LINEAR_PROMPT.md`
- `/Users/Weishengsu/Hermes_memory/docs/CODEX_B_LINEAR_PROMPT.md`

## Recommended Project Description For Linear

Hermes Memory MVP Retrieval Closure turns Hermes into a reliable enterprise knowledge QA loop.

Current focus is Phase 2.9c: close large-tender retrieval gaps and collect high-confidence rollout-readiness evidence before any broader rollout. The project is not yet production rollout and not full AI tender-review automation.

Current P0 work:

- Stabilize `总工期 / 关键节点` retrieval.
- Stabilize contract commercial parameter retrieval.
- Run high-confidence long-window validation on a stronger machine.

Known non-closed PRD gaps:

- Dense ingestion for uploaded chunks.
- Structured facts.
- Conversation memory.
- Permission governance.
- Incremental update loop.
- Audit loop.
- Full evaluation system.
- Version governance.
- Knowledge admin / human verification workflow.

Operating rule:

- Git is code truth.
- Local docs are technical truth.
- Linear is task, progress, blocker, and handoff truth.

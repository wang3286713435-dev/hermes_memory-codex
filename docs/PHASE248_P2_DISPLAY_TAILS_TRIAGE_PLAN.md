# Phase 2.48 P2 Display Tails Triage Plan

## 1. Goal

Phase 2.48 is a docs-only triage plan for two known P2 display tails discovered around the internal controlled MVP path.

The goal is to classify these tails, define bounded follow-up fixes, and keep the internal MVP operating loop moving without overstating production readiness.

This phase does not implement code, run smoke, write data, or start production rollout.

## 2. Current P2 Tails

| Tail | Current behavior | User impact | Current severity |
| --- | --- | --- | --- |
| Excel citation display | Citation may show a broad range plus row hint, for example `A3:P24 + Row 7`. This is human-checkable but not a precise single-row or single-cell citation. | Reviewer can still verify the source, but the run record is less clean and may require manual interpretation. | P2 |
| Meeting transcript boundary flag | Meeting transcript behavior is correct, but some answer / trace displays do not consistently print `transcript_as_fact=false`. | Reviewer must infer the boundary from content instead of seeing the explicit invariant every time. | P2 |

## 3. Why P2

These issues are P2 because:

1. They do not indicate evidence fabrication.
2. They do not show facts replacing retrieval evidence.
3. They do not show transcript content being promoted to confirmed facts.
4. They do not show third-document contamination.
5. They do not block the internal controlled MVP when recorded as known display tails.

They would become P1 if:

1. Citation display becomes too vague for a reviewer to locate the supporting source.
2. Missing Evidence is hidden behind a misleading citation.
3. Transcript boundary fields become ambiguous enough that reviewers cannot verify whether `transcript_as_fact=false` held.
4. The issue appears repeatedly in MVP run records and slows daily review.

They would become P0 if:

1. Facts, transcript, or snapshot content is used as final answer evidence without retrieval support.
2. A citation points to the wrong document or a third document.
3. The system fabricates a precise cell, row, source, or transcript boundary that was not supported by evidence.
4. Permission, version, or document scope boundaries are violated.

## 4. Non-goals

Phase 2.48 does not:

1. Change the retrieval contract.
2. Change the memory kernel main architecture.
3. Change ingestion, parser, Excel parser, PPTX parser, or meeting transcript parser behavior.
4. Reindex, backfill, repair, clean up, delete, migrate, or mutate DB / OpenSearch / Qdrant / facts / document_versions.
5. Expand to production rollout, customer delivery, automatic bid review, automatic bidding, or automatic business decisions.
6. Tune broad retrieval ranking.
7. Hide Missing Evidence.

## 5. Candidate Routes

| Candidate | Scope | Expected change | Stop condition |
| --- | --- | --- | --- |
| Phase 2.48a Excel citation display polish | Renderer / citation summary only | Display precise `cell_range` when available; if only row/range fallback is available, print `row_range_fallback=true` or equivalent. Do not pretend fallback is exact cell evidence. | Stop if parser / ingestion / contract changes are required. |
| Phase 2.48b Meeting transcript boundary trace display polish | Context / trace output only | Ensure answer / trace consistently shows `transcript_as_fact=false` or an equivalent boundary statement when meeting transcript evidence is involved. | Stop if meeting ingestion contract or transcript extraction logic must change. |
| Phase 2.48c Codex C targeted smoke prompt | Validation prompt only | Run a small targeted terminal smoke after 2.48a / 2.48b; do not rerun full Day-1 unless a P1/P0 appears. | Stop if smoke reveals evidence substitution, contamination, or scope breach. |

## 6. Phase 2.48a Acceptance

Excel citation display polish is acceptable only if:

1. `sheet_name` remains visible when present.
2. `cell_range` is displayed when precise metadata exists.
3. If the system only has broad range / row fallback, it must explicitly show `row_range_fallback=true`, `citation_precision=row_range_fallback`, or an equivalent warning.
4. It does not fabricate a single cell or single row when the parser did not provide one.
5. It does not change Excel ingestion, parser, chunking, retrieval, or indexing.
6. It does not hide Missing Evidence.

## 7. Phase 2.48b Acceptance

Meeting transcript boundary display polish is acceptable only if:

1. `transcript_as_fact=false` is consistently visible in answer / trace, or the answer contains an equivalent explicit boundary statement.
2. `facts_as_answer=false` remains stable.
3. Meeting transcript chunks are not written into `facts_context_fact_ids`.
4. Confirmed facts remain separate from retrieval evidence and meeting transcript metadata.
5. It does not change meeting transcript ingestion, extraction, retrieval contract, or memory kernel main architecture.

## 8. Phase 2.48c Targeted Smoke

After a bounded display polish, Codex C should run only targeted smoke:

1. One Excel query that previously showed broad range + row hint.
2. One meeting transcript query that previously omitted explicit `transcript_as_fact=false`.
3. One guard query confirming no facts / transcript / snapshot substitution.

Full Day-1 rerun is not required unless the targeted smoke finds P1/P0 behavior.

## 9. Internal MVP Relationship

Internal controlled MVP can continue while these tails remain open because both are reviewer UX / trace-display issues, not current evidence integrity blockers.

Operators should record them in the local ignored run record:

1. Excel display tail: record actual citation text and whether row/range fallback was used.
2. Meeting transcript flag tail: record whether `transcript_as_fact=false` was visible or only inferred.

These tails do not authorize production rollout.

## 10. Recommended Next Step

Recommended order:

1. Phase 2.48a Excel citation display polish, because citation readability directly affects daily run record review.
2. Phase 2.48b Meeting transcript boundary trace display polish.
3. Phase 2.48c Codex C targeted smoke covering both display tails.

Codex B should review this triage plan before implementation. No Git baseline is recommended until review confirms the route.

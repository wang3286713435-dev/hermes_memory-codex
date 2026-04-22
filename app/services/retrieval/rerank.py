from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

import httpx

from app.core.config import settings
from app.schemas.retrieval import SearchResult


@dataclass(frozen=True)
class RerankRequest:
    query: str
    candidates: list[SearchResult]
    top_k: int
    retrieval_mode: str
    trace_id: str | None = None


@dataclass(frozen=True)
class RerankOutcome:
    results: list[SearchResult]
    status: str
    provider: str
    trace: dict[str, Any] = field(default_factory=dict)


class NoopReranker:
    provider = "noop"

    def rerank(self, request: RerankRequest) -> RerankOutcome:
        started_at = perf_counter()
        ordered = sorted(request.candidates, key=lambda item: item.score, reverse=True)
        results = ordered[: request.top_k]
        elapsed_ms = round((perf_counter() - started_at) * 1000, 3)
        return RerankOutcome(
            results=results,
            status="skipped",
            provider=self.provider,
            trace={
                "provider": self.provider,
                "status": "skipped",
                "reason": "noop_reranker_preserves_score_order",
                "reason_if_skipped": "noop_reranker_preserves_score_order",
                "fail_open": False,
                "elapsed_ms": elapsed_ms,
                "input_count": len(request.candidates),
                "output_count": len(results),
                "candidate_count_in": len(request.candidates),
                "candidate_count_out": len(results),
                "top_k": request.top_k,
                "retrieval_mode": request.retrieval_mode,
            },
        )


class AliyunTextReranker:
    provider = "aliyun_text_rerank"
    endpoint_path = "/api/v1/services/rerank/text-rerank/text-rerank"

    def rerank(self, request: RerankRequest) -> RerankOutcome:
        started_at = perf_counter()
        model = settings.aliyun_rerank_model
        timeout_ms = settings.aliyun_rerank_timeout_ms
        raw_base_url = settings.aliyun_rerank_base_url
        normalized_base_url = self._normalized_base_url(raw_base_url)
        request_url = self._request_url(normalized_base_url)
        candidates = self._input_candidates(request)
        api_key, api_key_source = self._api_key()
        if not api_key:
            return self._fail_open(
                request=request,
                candidates=candidates,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                error_type="missing_api_key",
                reason="Neither ALIYUN_RERANK_API_KEY nor ALIYUN_EMBEDDING_API_KEY is configured",
                api_key_source=api_key_source,
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
            )

        if not candidates:
            return self._fail_open(
                request=request,
                candidates=candidates,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                error_type="empty_candidates",
                reason="candidate pool is empty",
                api_key_source=api_key_source,
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
            )

        payload = {
            "model": model,
            "input": {
                "query": request.query,
                "documents": [self.build_document_text(candidate) for candidate in candidates],
            },
            "parameters": {
                "top_n": min(request.top_k, len(candidates)),
                "return_documents": False,
            },
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        try:
            response = httpx.post(
                request_url,
                json=payload,
                headers=headers,
                timeout=timeout_ms / 1000,
                trust_env=False,
            )
            remote_request_id = response.headers.get("x-request-id") or response.headers.get("X-Request-Id")
            response.raise_for_status()
            data = response.json()
            return self._from_response(
                request=request,
                candidates=candidates,
                data=data,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                api_key_source=api_key_source,
                remote_request_id=remote_request_id,
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
            )
        except httpx.HTTPStatusError as exc:
            return self._fail_open(
                request=request,
                candidates=candidates,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                error_type="http_status_error",
                reason=f"{exc.response.status_code} {exc.response.text[:500]}".strip(),
                api_key_source=api_key_source,
                remote_request_id=exc.response.headers.get("x-request-id")
                or exc.response.headers.get("X-Request-Id"),
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
                http_status_code=exc.response.status_code,
            )
        except httpx.TimeoutException as exc:
            return self._fail_open(
                request=request,
                candidates=candidates,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                error_type="timeout",
                reason=str(exc) or "aliyun rerank request timed out",
                api_key_source=api_key_source,
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
            )
        except Exception as exc:
            return self._fail_open(
                request=request,
                candidates=candidates,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                error_type=exc.__class__.__name__,
                reason=str(exc),
                api_key_source=api_key_source,
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
            )

    def build_document_text(self, candidate: SearchResult) -> str:
        title = candidate.source_name or ""
        path_parts = candidate.heading_path or candidate.section_path or []
        path = " / ".join(str(part) for part in path_parts)
        return f"标题: {title}\n路径: {path}\n正文: {candidate.text}"

    def _api_key(self) -> tuple[str | None, str | None]:
        if settings.aliyun_rerank_api_key:
            return settings.aliyun_rerank_api_key, "ALIYUN_RERANK_API_KEY"
        if settings.aliyun_embedding_api_key:
            return settings.aliyun_embedding_api_key, "ALIYUN_EMBEDDING_API_KEY"
        return None, None

    def _input_candidates(self, request: RerankRequest) -> list[SearchResult]:
        ordered = sorted(request.candidates, key=lambda item: item.score, reverse=True)
        return ordered[: settings.rerank_input_cap]

    def _from_response(
        self,
        request: RerankRequest,
        candidates: list[SearchResult],
        data: dict[str, Any],
        started_at: float,
        model: str,
        timeout_ms: int,
        api_key_source: str | None = None,
        remote_request_id: str | None = None,
        raw_base_url: str | None = None,
        normalized_base_url: str | None = None,
        request_url: str | None = None,
    ) -> RerankOutcome:
        output = data.get("output") or {}
        remote_request_id = remote_request_id or data.get("request_id") or output.get("request_id")
        raw_results = output.get("results") or data.get("results") or []
        if not raw_results:
            return self._fail_open(
                request=request,
                candidates=candidates,
                started_at=started_at,
                model=model,
                timeout_ms=timeout_ms,
                error_type="empty_result",
                reason="aliyun rerank response contains no results",
                api_key_source=api_key_source,
                remote_request_id=remote_request_id,
                raw_base_url=raw_base_url,
                normalized_base_url=normalized_base_url,
                request_url=request_url,
            )

        ranked: list[SearchResult] = []
        for raw in raw_results:
            index = raw.get("index")
            if not isinstance(index, int) or index < 0 or index >= len(candidates):
                return self._fail_open(
                    request=request,
                    candidates=candidates,
                    started_at=started_at,
                    model=model,
                    timeout_ms=timeout_ms,
                    error_type="invalid_result_index",
                    reason=f"invalid rerank result index: {index}",
                    api_key_source=api_key_source,
                    remote_request_id=remote_request_id,
                    raw_base_url=raw_base_url,
                    normalized_base_url=normalized_base_url,
                    request_url=request_url,
                )
            relevance_score = float(raw.get("relevance_score") or raw.get("score") or 0.0)
            candidate = candidates[index].model_copy(deep=True)
            candidate.scores = {**candidate.scores, "rerank": relevance_score}
            candidate.metadata = {**candidate.metadata, "rerank_score": relevance_score}
            ranked.append(candidate)

        results = ranked[: request.top_k]
        elapsed_ms = self._elapsed_ms(started_at)
        return RerankOutcome(
            results=results,
            status="executed",
            provider=self.provider,
            trace={
                "provider": self.provider,
                "model": model,
                "status": "executed",
                "reason": "aliyun_text_rerank_executed",
                "reason_if_skipped": None,
                "fail_open": False,
                "elapsed_ms": elapsed_ms,
                "timeout_ms": timeout_ms,
                "input_count": len(candidates),
                "output_count": len(results),
                "candidate_count_in": len(candidates),
                "candidate_count_out": len(results),
                "top_k": request.top_k,
                "retrieval_mode": request.retrieval_mode,
                "remote_request_id": remote_request_id,
                "api_key_source": api_key_source,
                "rerank_input_cap": settings.rerank_input_cap,
                "raw_base_url": raw_base_url,
                "normalized_base_url": normalized_base_url,
                "request_url": request_url,
            },
        )

    def _fail_open(
        self,
        request: RerankRequest,
        candidates: list[SearchResult],
        started_at: float,
        model: str,
        timeout_ms: int,
        error_type: str,
        reason: str,
        api_key_source: str | None = None,
        remote_request_id: str | None = None,
        raw_base_url: str | None = None,
        normalized_base_url: str | None = None,
        request_url: str | None = None,
        http_status_code: int | None = None,
    ) -> RerankOutcome:
        fallback_results = sorted(candidates, key=lambda item: item.score, reverse=True)[: request.top_k]
        elapsed_ms = self._elapsed_ms(started_at)
        return RerankOutcome(
            results=fallback_results,
            status="failed_open",
            provider=self.provider,
            trace={
                "provider": self.provider,
                "model": model,
                "status": "failed_open",
                "reason": reason,
                "reason_if_skipped": None,
                "fail_open": True,
                "elapsed_ms": elapsed_ms,
                "timeout_ms": timeout_ms,
                "error_type": error_type,
                "input_count": len(candidates),
                "output_count": len(fallback_results),
                "candidate_count_in": len(candidates),
                "candidate_count_out": len(fallback_results),
                "top_k": request.top_k,
                "retrieval_mode": request.retrieval_mode,
                "remote_request_id": remote_request_id,
                "api_key_source": api_key_source,
                "rerank_input_cap": settings.rerank_input_cap,
                "raw_base_url": raw_base_url,
                "normalized_base_url": normalized_base_url,
                "request_url": request_url,
                "http_status_code": http_status_code,
            },
        )

    def _elapsed_ms(self, started_at: float) -> float:
        return round((perf_counter() - started_at) * 1000, 3)

    def _normalized_base_url(self, raw_base_url: str | None) -> str:
        normalized = (raw_base_url or "").strip()
        if not normalized:
            return "https://dashscope.aliyuncs.com"
        if "://" not in normalized:
            normalized = f"https://{normalized}"
        return normalized.rstrip("/")

    def _request_url(self, normalized_base_url: str) -> str:
        if normalized_base_url.endswith(self.endpoint_path):
            return normalized_base_url
        return f"{normalized_base_url}{self.endpoint_path}"

import re
from uuid import uuid4

from sqlalchemy import and_, or_
from opensearchpy import OpenSearch
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger
from app.models.chunk import Chunk
from app.models.document import Document, DocumentVersion
from app.models.retrieval import RetrievalLog
from app.schemas.retrieval import SearchRequest, SearchResponse, SearchResult
from app.services.retrieval.rerank import NoopReranker

logger = get_logger(__name__)


class RetrievalService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.reranker = NoopReranker()

    def search(self, request: SearchRequest) -> SearchResponse:
        trace_id = str(uuid4())
        backend = "opensearch"
        try:
            dense_candidates = self._dense_search(request)
            sparse_candidates = self._sparse_search(request)
            candidates = self._merge_candidates(dense_candidates, sparse_candidates)
        except Exception:
            logger.exception("opensearch_search_failed_falling_back_to_db")
            backend = "database_fallback"
            candidates = self._database_fallback_search(request)

        reranked = self.reranker.rerank(request.query, candidates, request.top_k)
        self._write_log(trace_id, request, len(reranked), backend, "success")
        return SearchResponse(
            query=request.query,
            results=reranked,
            backend=backend,
            dense_retrieval_status="todo: vector adapter not connected in Phase 1 loop",
        )

    def _dense_search(self, request: SearchRequest) -> list[SearchResult]:
        # TODO: connect the existing 1024-dimensional vector database adapter.
        return []

    def _sparse_search(self, request: SearchRequest) -> list[SearchResult]:
        client = OpenSearch(settings.opensearch_url, timeout=5)
        filters: list[dict] = [{"term": {"status": "active"}}]
        if request.filters.source_type:
            filters.append({"term": {"source_type": request.filters.source_type}})
        if request.filters.document_id:
            filters.append({"term": {"document_id": request.filters.document_id}})
        if request.filters.document_type:
            filters.append({"term": {"document_type": request.filters.document_type}})
        if request.filters.is_latest is not None:
            filters.append({"term": {"is_latest": request.filters.is_latest}})

        response = client.search(
            index=settings.opensearch_index_chunks,
            body={
                "size": request.top_k,
                "query": {
                    "bool": {
                        "must": [{"match": {"text": request.query}}],
                        "filter": filters,
                    }
                },
            },
        )
        results: list[SearchResult] = []
        for hit in response.get("hits", {}).get("hits", []):
            source = hit.get("_source", {})
            results.append(
                SearchResult(
                    chunk_id=source["chunk_id"],
                    document_id=source["document_id"],
                    version_id=source["version_id"],
                    chunk_index=source.get("chunk_index"),
                    text=source.get("text", ""),
                    score=float(hit.get("_score") or 0.0),
                    source_name=source.get("source_name"),
                    source_uri=source.get("source_uri"),
                    source_type=source.get("source_type"),
                    version_name=source.get("version_name"),
                    heading_path=source.get("heading_path") or [],
                    section_path=source.get("heading_path") or [],
                    page_start=source.get("page_start"),
                    page_end=source.get("page_end"),
                    metadata=source.get("metadata_json") or {},
                )
            )
        return results

    def _database_fallback_search(self, request: SearchRequest) -> list[SearchResult]:
        query = (
            self.db.query(Chunk, Document, DocumentVersion)
            .join(Document, Chunk.document_id == Document.id)
            .join(DocumentVersion, Chunk.version_id == DocumentVersion.id)
            .filter(Document.status == "active")
        )
        keyword_terms = self._simplify_query_terms(request.query)
        if keyword_terms:
            query = query.filter(
                and_(
                    *[
                        or_(
                            Chunk.text.ilike(f"%{term}%"),
                            Document.title.ilike(f"%{term}%"),
                        )
                        for term in keyword_terms
                    ]
                )
            )
        else:
            query = query.filter(
                or_(
                    Chunk.text.ilike(f"%{request.query}%"),
                    Document.title.ilike(f"%{request.query}%"),
                )
            )
        if request.filters.source_type:
            query = query.filter(Chunk.source_type == request.filters.source_type)
        if request.filters.document_id:
            query = query.filter(Document.id == request.filters.document_id)
        if request.filters.document_type:
            query = query.filter(Document.document_type == request.filters.document_type)
        if request.filters.is_latest is not None:
            query = query.filter(DocumentVersion.is_latest == request.filters.is_latest)

        rows = query.limit(request.top_k).all()
        results: list[SearchResult] = []
        for chunk, document, version in rows:
            results.append(
                SearchResult(
                    chunk_id=chunk.id,
                    document_id=document.id,
                    version_id=version.id,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    score=1.0,
                    source_name=document.title,
                    source_uri=document.source_uri,
                    source_type=chunk.source_type,
                    version_name=version.version_name,
                    heading_path=chunk.heading_path or [],
                    section_path=chunk.section_path or [],
                    page_start=chunk.page_start,
                    page_end=chunk.page_end,
                    metadata=chunk.metadata_json or {},
                )
            )
        return results

    def _simplify_query_terms(self, query: str) -> list[str]:
        text = (query or "").strip()
        if not text:
            return []

        normalized = re.sub(r"[，。；：、“”\"'‘’（）()【】\[\]、,.;:!?？]+", " ", text)
        normalized = normalized.replace("里的", " ").replace("里面", " ").replace("相关", " ")
        for stop in ("请查一下", "查一下", "请问", "帮我", "帮忙", "告诉我", "给我", "是什么", "有没有", "是否"):
            normalized = normalized.replace(stop, " ")

        phrase_candidates: list[str] = []
        project_matches = re.findall(r"([\u4e00-\u9fffA-Za-z0-9]{2,12}项目)", normalized)
        phrase_candidates.extend(project_matches)
        if "投标截止日期" in text:
            phrase_candidates.append("投标截止日期")
        if "招标资料" in text:
            phrase_candidates.append("招标资料")
        if "截止日期" in text:
            phrase_candidates.append("截止日期")

        raw_terms = re.findall(r"[A-Za-z0-9]{2,}|[\u4e00-\u9fff]{2,8}", normalized)
        stop_terms = {
            "这个", "那个", "什么", "哪些", "怎么", "如何", "一下", "内容", "资料",
            "文档", "文件", "请查", "请问", "帮忙", "关于", "里面", "里的", "相关",
        }
        terms: list[str] = []
        for term in raw_terms:
            if term in stop_terms:
                continue
            if len(term) < 2:
                continue
            if term not in terms:
                terms.append(term)

        merged = []
        for term in [*phrase_candidates, *terms]:
            if term not in merged:
                merged.append(term)

        return merged[:4]

    def _merge_candidates(
        self,
        dense_candidates: list[SearchResult],
        sparse_candidates: list[SearchResult],
    ) -> list[SearchResult]:
        seen: set[str] = set()
        merged: list[SearchResult] = []
        for candidate in [*dense_candidates, *sparse_candidates]:
            if candidate.chunk_id in seen:
                continue
            seen.add(candidate.chunk_id)
            merged.append(candidate)
        return merged

    def _write_log(
        self,
        trace_id: str,
        request: SearchRequest,
        result_count: int,
        backend: str,
        status: str,
    ) -> None:
        self.db.add(
            RetrievalLog(
                trace_id=trace_id,
                user_id=request.user_id,
                query=request.query,
                top_k=request.top_k,
                filters_json=request.filters.model_dump(),
                result_count=result_count,
                backend=backend,
                status=status,
            )
        )
        self.db.commit()

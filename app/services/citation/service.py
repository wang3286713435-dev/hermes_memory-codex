from app.schemas.agent import Citation
from app.schemas.retrieval import SearchResult


class CitationService:
    def build_citations(self, results: list[SearchResult]) -> list[Citation]:
        citations: list[Citation] = []
        for result in results:
            citations.append(
                Citation(
                    document_id=result.document_id,
                    version_id=result.version_id,
                    chunk_id=result.chunk_id,
                    source_name=result.source_name,
                    source_uri=result.source_uri,
                    version_name=result.version_name,
                    page_start=result.page_start,
                    page_end=result.page_end,
                    heading_path=result.heading_path,
                    section_path=result.section_path,
                    quote_text=result.text[:300],
                )
            )
        return citations

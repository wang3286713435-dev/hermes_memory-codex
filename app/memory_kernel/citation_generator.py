from app.schemas.agent import Citation
from app.schemas.retrieval import SearchResult
from app.services.citation.service import CitationService


class CitationGenerator:
    """Generates normalized citations from memory retrieval results."""

    def __init__(self) -> None:
        self.citation_service = CitationService()

    def generate(self, results: list[SearchResult]) -> list[Citation]:
        return self.citation_service.build_citations(results)


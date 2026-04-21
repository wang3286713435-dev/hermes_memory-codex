from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class ParsedBlock:
    text: str
    block_type: str = "paragraph"
    page_number: int | None = None
    title_path: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ParsedDocument:
    source_path: Path
    title: str | None
    blocks: list[ParsedBlock]
    metadata: dict = field(default_factory=dict)


class DocumentParser(Protocol):
    def parse(self, source_path: Path) -> ParsedDocument:
        """Parse a document into structured blocks."""

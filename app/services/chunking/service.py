from dataclasses import dataclass, field
from hashlib import sha256

from app.services.parsing.base import ParsedBlock, ParsedDocument


@dataclass(frozen=True)
class ChunkCandidate:
    text: str
    content_hash: str
    title_path: list[str] = field(default_factory=list)
    section_path: list[str] = field(default_factory=list)
    page_start: int | None = None
    page_end: int | None = None
    metadata: dict = field(default_factory=dict)


class ChunkingService:
    def __init__(self, target_chars: int = 900, overlap_chars: int = 150) -> None:
        self.target_chars = target_chars
        self.overlap_chars = overlap_chars

    def chunk(self, parsed_document: ParsedDocument) -> list[ChunkCandidate]:
        chunks: list[ChunkCandidate] = []
        buffer: list[ParsedBlock] = []

        def flush_buffer() -> None:
            if not buffer:
                return
            text = "\n\n".join(block.text for block in buffer if block.text.strip()).strip()
            if not text:
                buffer.clear()
                return
            heading_path = buffer[-1].title_path
            pages = [block.page_number for block in buffer if block.page_number is not None]
            page_start = min(pages) if pages else None
            page_end = max(pages) if pages else None
            metadata = self._merged_metadata(buffer)
            chunks.extend(self._chunk_text(text, heading_path, page_start, page_end, metadata))
            buffer.clear()

        for block in parsed_document.blocks:
            if block.block_type == "heading":
                flush_buffer()
                continue
            if block.metadata.get("chunk_boundary"):
                flush_buffer()
                chunks.extend(
                    self._chunk_text(
                        block.text,
                        block.title_path,
                        block.page_number,
                        block.page_number,
                        block.metadata,
                    )
                )
                continue
            if len(block.text) > self.target_chars:
                flush_buffer()
                chunks.extend(
                    self._chunk_text(
                        block.text,
                        block.title_path,
                        block.page_number,
                        block.page_number,
                        block.metadata,
                    )
                )
                continue
            projected_size = sum(len(item.text) for item in buffer) + len(block.text)
            if buffer and projected_size > self.target_chars:
                flush_buffer()
            buffer.append(block)
        flush_buffer()
        return chunks

    def _chunk_text(
        self,
        text: str,
        title_path: list[str],
        page_start: int | None,
        page_end: int | None,
        metadata: dict | None = None,
    ) -> list[ChunkCandidate]:
        normalized = text.strip()
        if not normalized:
            return []

        chunks: list[ChunkCandidate] = []
        start = 0
        while start < len(normalized):
            end = min(start + self.target_chars, len(normalized))
            chunk_text = normalized[start:end].strip()
            if chunk_text:
                chunks.append(
                    ChunkCandidate(
                        text=chunk_text,
                        content_hash=sha256(chunk_text.encode("utf-8")).hexdigest(),
                        title_path=title_path,
                        section_path=title_path,
                        page_start=page_start,
                        page_end=page_end,
                        metadata={
                            **(metadata or {}),
                            "chunking_strategy": "heading_paragraph_length",
                        },
                    )
                )
            if end == len(normalized):
                break
            start = max(end - self.overlap_chars, start + 1)
        return chunks

    def _merged_metadata(self, blocks: list[ParsedBlock]) -> dict:
        if not blocks:
            return {}
        if len(blocks) == 1:
            return dict(blocks[0].metadata)
        shared: dict = {}
        keys = set().union(*(block.metadata.keys() for block in blocks))
        for key in keys:
            values = [block.metadata.get(key) for block in blocks if key in block.metadata]
            if values and all(value == values[0] for value in values):
                shared[key] = values[0]
        if any(block.metadata for block in blocks):
            shared["source_block_count"] = len(blocks)
        return shared

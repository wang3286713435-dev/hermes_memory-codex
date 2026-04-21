from pathlib import Path

import fitz

from app.services.parsing.base import ParsedBlock, ParsedDocument


class PdfParser:
    def parse(self, source_path: Path) -> ParsedDocument:
        blocks: list[ParsedBlock] = []
        with fitz.open(source_path) as doc:
            metadata = dict(doc.metadata or {})
            title = metadata.get("title") or source_path.name
            for page_index, page in enumerate(doc, start=1):
                text = page.get_text("text").strip()
                if not text:
                    continue
                for paragraph in [p.strip() for p in text.split("\n\n") if p.strip()]:
                    blocks.append(
                        ParsedBlock(
                            text=paragraph,
                            block_type="paragraph",
                            page_number=page_index,
                            metadata={"page": page_index},
                        )
                    )
        return ParsedDocument(
            source_path=source_path,
            title=title,
            blocks=blocks,
            metadata={"parser": "pdf", **metadata},
        )


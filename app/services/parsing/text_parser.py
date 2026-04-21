from pathlib import Path

from app.services.parsing.base import ParsedBlock, ParsedDocument


class TextParser:
    def parse(self, source_path: Path) -> ParsedDocument:
        text = source_path.read_text(encoding="utf-8")
        blocks: list[ParsedBlock] = []
        heading_path: list[str] = []
        paragraph_buffer: list[str] = []

        def flush_paragraph() -> None:
            if paragraph_buffer:
                blocks.append(
                    ParsedBlock(
                        text="\n".join(paragraph_buffer).strip(),
                        block_type="paragraph",
                        title_path=heading_path.copy(),
                    )
                )
                paragraph_buffer.clear()

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                flush_paragraph()
                continue
            if source_path.suffix.lower() == ".md" and line.startswith("#"):
                flush_paragraph()
                level = len(line) - len(line.lstrip("#"))
                heading = line[level:].strip()
                if heading:
                    heading_path = heading_path[: max(level - 1, 0)] + [heading]
                    blocks.append(
                        ParsedBlock(text=heading, block_type="heading", title_path=heading_path.copy())
                    )
                continue
            paragraph_buffer.append(line)
        flush_paragraph()

        if not blocks and text.strip():
            blocks.append(ParsedBlock(text=text.strip(), block_type="text"))

        return ParsedDocument(
            source_path=source_path,
            title=source_path.name,
            blocks=blocks,
            metadata={"parser": "text"},
        )


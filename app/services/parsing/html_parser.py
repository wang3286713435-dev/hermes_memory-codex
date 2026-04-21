from pathlib import Path

from bs4 import BeautifulSoup

from app.services.parsing.base import ParsedBlock, ParsedDocument


class HtmlParser:
    def parse(self, source_path: Path) -> ParsedDocument:
        soup = BeautifulSoup(source_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else source_path.name
        heading_path: list[str] = []
        blocks: list[ParsedBlock] = []

        for node in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]):
            text = " ".join(node.get_text(" ", strip=True).split())
            if not text:
                continue
            if node.name and node.name.startswith("h"):
                level = int(node.name[1])
                heading_path = heading_path[: max(level - 1, 0)] + [text]
                blocks.append(ParsedBlock(text=text, block_type="heading", title_path=heading_path.copy()))
            else:
                blocks.append(ParsedBlock(text=text, block_type=node.name or "paragraph", title_path=heading_path.copy()))

        return ParsedDocument(
            source_path=source_path,
            title=title,
            blocks=blocks,
            metadata={"parser": "html", "title": title},
        )


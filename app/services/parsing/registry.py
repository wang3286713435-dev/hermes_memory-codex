from pathlib import Path

from app.services.parsing.base import DocumentParser
from app.services.parsing.docx_parser import DocxParser
from app.services.parsing.html_parser import HtmlParser
from app.services.parsing.pdf_parser import PdfParser
from app.services.parsing.pptx_parser import PptxParser
from app.services.parsing.text_parser import TextParser
from app.services.parsing.xlsx_parser import XlsxParser


class ParserRegistry:
    def __init__(self) -> None:
        self._parsers: dict[str, DocumentParser] = {
            ".html": HtmlParser(),
            ".htm": HtmlParser(),
            ".md": TextParser(),
            ".pdf": PdfParser(),
            ".txt": TextParser(),
            ".docx": DocxParser(),
            ".xlsx": XlsxParser(),
            ".pptx": PptxParser(),
        }

    def get_parser(self, source_path: Path) -> DocumentParser:
        suffix = source_path.suffix.lower()
        if suffix not in self._parsers:
            raise ValueError(f"No parser registered for suffix: {suffix}")
        return self._parsers[suffix]

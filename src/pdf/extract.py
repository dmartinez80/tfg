from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import pdfplumber


@dataclass
class PageText:
    page_number: int
    text: str


def extract_text_by_page(pdf_path: str, max_pages: Optional[int] = None) -> List[PageText]:
    """
    Extrae texto por página con pdfplumber.
    MVP: solo texto plano (sin estructura aún).
    """
    pages: List[PageText] = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        limit = min(total, max_pages) if max_pages is not None else total

        for i in range(limit):
            page = pdf.pages[i]
            text = page.extract_text() or ""
            # Limpieza mínima
            text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
            pages.append(PageText(page_number=i + 1, text=text))

    return pages
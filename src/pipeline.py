from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.pdf.extract import extract_text_by_page
from src.pptx.builder import build_pptx, slide_specs_from_pages


@dataclass
class PipelineConfig:
    max_pages: Optional[int] = None
    bullets_per_slide: int = 7


def pdf_to_pptx(
    pdf_path: str,
    pptx_out_path: str,
    title: str = "Presentación generada desde PDF",
    config: Optional[PipelineConfig] = None,
) -> None:
    cfg = config or PipelineConfig()

    pages = extract_text_by_page(pdf_path, max_pages=cfg.max_pages)
    pages_tuples = [(p.page_number, p.text) for p in pages]

    specs = slide_specs_from_pages(
        pages_text=pages_tuples,
        bullets_per_slide=cfg.bullets_per_slide,
    )

    build_pptx(
        slide_specs=specs,
        output_path=pptx_out_path,
        deck_title=title,
    )
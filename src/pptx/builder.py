from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from pptx import Presentation
from pptx.util import Pt


@dataclass
class SlideSpec:
    title: str
    bullets: List[str]


def _chunk_lines_to_bullets(text: str, max_bullets: int = 7, max_chars: int = 140) -> List[str]:
    """
    Convierte texto en bullets simples.
    - Parte por líneas
    - Recorta líneas largas
    - Limita número de bullets por slide
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullets: List[str] = []
    for ln in lines:
        if len(ln) > max_chars:
            ln = ln[: max_chars - 1] + "…"
        bullets.append(ln)
        if len(bullets) >= max_bullets:
            break
    return bullets


def build_pptx(
    slide_specs: List[SlideSpec],
    output_path: str,
    deck_title: Optional[str] = None,
) -> None:
    """
    Crea un PPTX usando layout 'Title and Content'.
    """
    prs = Presentation()

    # Slide portada opcional
    if deck_title:
        slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title Slide
        slide.shapes.title.text = deck_title
        if len(slide.placeholders) > 1:
            slide.placeholders[1].text = "Generado automáticamente desde PDF"

    # Slides de contenido
    for spec in slide_specs:
        slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
        slide.shapes.title.text = spec.title

        body = slide.shapes.placeholders[1].text_frame
        body.clear()

        if not spec.bullets:
            p = body.paragraphs[0]
            p.text = "(Sin texto extraíble en esta sección)"
            continue

        for i, b in enumerate(spec.bullets):
            if i == 0:
                p = body.paragraphs[0]
            else:
                p = body.add_paragraph()
            p.text = b
            p.level = 0
            p.font.size = Pt(18)

    prs.save(output_path)


def slide_specs_from_pages(
    pages_text: List[tuple[int, str]],
    bullets_per_slide: int = 7,
) -> List[SlideSpec]:
    """
    MVP: 1 slide por página.
    """
    specs: List[SlideSpec] = []
    for page_number, text in pages_text:
        bullets = _chunk_lines_to_bullets(text, max_bullets=bullets_per_slide)
        specs.append(SlideSpec(title=f"Página {page_number}", bullets=bullets))
    return specs
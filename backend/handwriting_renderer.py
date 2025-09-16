#!/usr/bin/env python3
"""
Handwriting renderer for doubt solutions.

Features:
- Renders solution text as "handwritten-style" pages using PIL with a handwriting-like font if available
- Subtle jitter and ruled-paper background for realism
- Falls back to ReportLab text rendering if PIL or font load fails
- Produces a single PDF path; can also return image pages if needed later

Environment variables:
- HANDWRITING_FONT_PATH: absolute path to a .ttf/.otf handwriting font (e.g., Kalam, Caveat, Patrick Hand)
- HANDWRITING_DPI: page DPI (default 150)
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import os
import io

_DEFAULT_DPI = int(os.getenv("HANDWRITING_DPI", "150"))


def _lines_from_solution(solution: dict) -> List[str]:
    lines: List[str] = []
    # Question
    q = solution.get("question") or solution.get("question_text") or solution.get("query")
    if q:
        lines.append("Question:")
        lines.extend(_wrap_text(str(q), width=80))
        lines.append("")
    # Answer / shortAnswer
    mobile = solution.get("mobile_format") or solution.get("mobileFormat") or {}
    ans = solution.get("answer") or solution.get("final_answer") or mobile.get("shortAnswer")
    if ans:
        lines.append("Answer:")
        lines.extend(_wrap_text(str(ans), width=80))
        lines.append("")
    # Steps
    steps = solution.get("steps") or []
    if steps:
        lines.append("Solution Steps:")
        for s in steps:
            title = s.get("title") or s.get("heading") or "Step"
            expl = s.get("explanation") or s.get("detail") or ""
            lines.append(f"- {title}")
            if expl:
                for w in _wrap_text(str(expl), width=78):
                    lines.append(f"  {w}")
        lines.append("")
    else:
        # fallback to keySteps
        ks = mobile.get("keySteps") or []
        if ks:
            lines.append("Key Steps:")
            for k in ks:
                lines.append(f"- {k}")
            lines.append("")
    return lines or ["Solution not available."]


def _wrap_text(text: str, width: int) -> List[str]:
    import textwrap
    return textwrap.wrap(text, width=width, replace_whitespace=False, drop_whitespace=False)


def _find_font_path() -> Optional[str]:
    # 1) Env override
    fp = os.getenv("HANDWRITING_FONT_PATH")
    if fp and Path(fp).exists():
        return fp
    # 2) Common system fonts (handwritten-like), platform dependent
    candidates = [
        # macOS
        "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf",
        "/System/Library/Fonts/Supplemental/Noteworthy.ttc",
        # Linux (if user installed)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # Windows (unlikely here)
        "C:/Windows/Fonts/comic.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def render_handwritten(solution_payload: Dict, output_prefix: str, out_dir: str = "../generated_solutions",
                        page_size: Tuple[int, int] = (1240, 1754),  # A4 @ 150dpi approx
                        margin: int = 80,
                        line_height: int = 36,
                        image_format: str = "png",
                        also_pdf: bool = True) -> Dict[str, Optional[str] | List[str]]:
    """Render solution into handwritten-style images and (optionally) a PDF.

    Returns dict: {"images": [paths...], "pdf": <path|None>}.
    """
    out_dir_p = Path(out_dir)
    out_dir_p.mkdir(parents=True, exist_ok=True)
    out_pdf = out_dir_p / f"{output_prefix}_handwritten.pdf"

    lines = _lines_from_solution(solution_payload)

    # Try PIL path for images (preferred)
    try:
        from PIL import Image, ImageDraw, ImageFont
        W, H = page_size
        font_path = _find_font_path()
        try:
            font = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        pages: List[Image.Image] = []
        y = margin
        page = Image.new('RGB', (W, H), color=(252, 252, 252))
        draw = ImageDraw.Draw(page)

        def new_page():
            nonlocal page, draw, y
            pages.append(page)
            page = Image.new('RGB', (W, H), color=(252, 252, 252))
            draw = ImageDraw.Draw(page)
            _draw_ruled_background(draw, W, H, margin, line_height)
            y = margin

        _draw_ruled_background(draw, W, H, margin, line_height)

        for text in lines:
            if y + line_height > H - margin:
                new_page()
            jitter = _jitter()
            draw.text((margin + jitter, y + jitter), text, font=font, fill=(20, 20, 20))
            y += line_height

        pages.append(page)

        # Save images
        image_paths: List[str] = []
        for idx, im in enumerate(pages, start=1):
            fname = out_dir_p / f"{output_prefix}_page{idx:02d}.{image_format}"
            im.save(fname)
            image_paths.append(str(fname))

        pdf_path: Optional[str] = None
        if also_pdf and pages:
            pages[0].save(out_pdf, "PDF", resolution=_DEFAULT_DPI, save_all=True, append_images=pages[1:])
            pdf_path = str(out_pdf)

        return {"images": image_paths, "pdf": pdf_path}
    except Exception:
        # Fallback to ReportLab PDF only
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm

        c = canvas.Canvas(str(out_pdf), pagesize=A4)
        w, h = A4
        x = 15 * mm
        y = h - 20 * mm
        c.setFont("Helvetica", 12)
        for text in lines:
            if y < 20 * mm:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = h - 20 * mm
            c.drawString(x, y, text)
            y -= 6 * mm
        c.save()
        return {"images": [], "pdf": str(out_pdf)}


# Backward-compatible wrapper
def render_handwritten_pdf(solution_payload: Dict, output_prefix: str, out_dir: str = "../generated_solutions",
                           page_size: Tuple[int, int] = (1240, 1754),  # A4 @ 150dpi approx
                           margin: int = 80,
                           line_height: int = 36) -> str:
    result = render_handwritten(solution_payload, output_prefix, out_dir, page_size, margin, line_height, image_format="png", also_pdf=True)
    return result.get("pdf") or ""


def _draw_ruled_background(draw, W, H, margin, line_height):
    # light blue lines
    color = (220, 230, 255)
    y = margin
    while y < H - margin:
        draw.line([(margin - 10, y + line_height), (W - margin + 10, y + line_height)], fill=color, width=1)
        y += line_height
    # margin line
    draw.line([(margin - 20, margin), (margin - 20, H - margin)], fill=(255, 180, 180), width=1)


def _jitter() -> int:
    import random
    return random.randint(-1, 1)


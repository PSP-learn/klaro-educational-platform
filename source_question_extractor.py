#!/usr/bin/env python3
"""
PDF Question Extractor

Detects question regions (with equations preserved) from PDFs using PyMuPDF and exports
cropped images for high-fidelity inclusion in generated test PDFs.

Heuristics:
- Question headers: Q., Q1, 1., (1), Example 3, EXERCISE 8.1
- Stop words: Solution, Answer, Hints
- Groups consecutive blocks that belong to the same question

Notes:
- Works best when PDFs are locally accessible. If original file paths in the DB are not
  valid on this machine, pass a books_dir to resolve files by title/stem.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Iterable
import re
import fitz  # PyMuPDF
import os

HEADER_RE = re.compile(r"^(?:Q\.?\s*\d+|\d+\.|\(\d+\)|Example\s*\d+|EXERCISE\s*\d+(?:\.\d+)?)\b", re.IGNORECASE)
STOP_RE = re.compile(r"^(Solution|Answer|Hints?)\b", re.IGNORECASE)

@dataclass
class SourceQuestion:
    file_path: str
    page_number: int  # 1-indexed
    text: str
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)
    options: List[str]

class PDFQuestionExtractor:
    def __init__(self, output_image_dir: str = "generated_tests/_question_images"):
        self.out_dir = Path(output_image_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def extract_questions_from_file(self, pdf_path: str, topics: Optional[List[str]] = None,
                                    max_questions: Optional[int] = None) -> List[SourceQuestion]:
        pdf_path = str(pdf_path)
        if not os.path.exists(pdf_path):
            return []
        doc = fitz.open(pdf_path)
        results: List[SourceQuestion] = []
        topics_l = [t.lower() for t in (topics or [])]

        try:
            for page_idx in range(len(doc)):
                if max_questions and len(results) >= max_questions:
                    break
                page = doc.load_page(page_idx)
                blocks = page.get_text("blocks")  # list of (x0, y0, x1, y1, text, block_no, block_type,...)
                i = 0
                while i < len(blocks):
                    if max_questions and len(results) >= max_questions:
                        break
                    x0, y0, x1, y1, text, *_ = blocks[i]
                    if not text or not text.strip():
                        i += 1
                        continue
                    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
                    first = lines[0] if lines else ""
                    if HEADER_RE.match(first):
                        # Gather following blocks until next header/stop/blank gap
                        j = i
                        bx0, by0, bx1, by1 = x0, y0, x1, y1
                        collected_text_lines: List[str] = []
                        options: List[str] = []
                        while j < len(blocks):
                            tx0, ty0, tx1, ty1, ttext, *_ = blocks[j]
                            if not ttext or not ttext.strip():
                                break
                            tlines = [ln.strip() for ln in ttext.splitlines() if ln.strip()]
                            thead = tlines[0] if tlines else ""
                            if j != i and (HEADER_RE.match(thead) or STOP_RE.match(thead)):
                                break
                            # Merge bbox
                            bx0 = min(bx0, tx0); by0 = min(by0, ty0)
                            bx1 = max(bx1, tx1); by1 = max(by1, ty1)
                            collected_text_lines.extend(tlines)
                            # Capture MCQ-like options
                            for ln in tlines:
                                if re.match(r"^(?:[A-D]\.|\([a-d]\)|[a-d]\))\s+", ln):
                                    options.append(ln)
                            j += 1
                        full_text = " ".join(collected_text_lines).strip()
                        if not full_text:
                            i = j
                            continue
                        if topics_l and not any(t in full_text.lower() for t in topics_l):
                            i = j
                            continue
                        results.append(SourceQuestion(
                            file_path=pdf_path,
                            page_number=page_idx + 1,
                            text=full_text,
                            bbox=(bx0, by0, bx1, by1),
                            options=options[:4]
                        ))
                        i = j
                    else:
                        i += 1
        finally:
            doc.close()
        return results

    def render_question_image(self, pdf_path: str, page_number: int,
                              bbox: Tuple[float, float, float, float]) -> Optional[str]:
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(page_number - 1)
            rect = fitz.Rect(*bbox)
            # Expand a little margin
            rect = rect + fitz.Rect(-6, -6, 6, 6)
            # Clip and render
            mat = fitz.Matrix(2, 2)  # 2x zoom for readability
            pix = page.get_pixmap(matrix=mat, clip=rect, alpha=False)
            out_name = f"q_{Path(pdf_path).stem}_p{page_number}_{abs(hash(bbox)) & 0xfffffff}.png"
            out_path = str(self.out_dir / out_name)
            pix.save(out_path)
            doc.close()
            return out_path
        except Exception:
            return None

    @staticmethod
    def try_resolve_file(original_path: str, books_dir: Optional[str], fallback_titles: Iterable[str]) -> Optional[str]:
        """Resolve a possibly invalid stored file path to a local PDF, searching books_dir by title/stem."""
        if original_path and os.path.exists(original_path):
            return original_path
        if not books_dir:
            return None
        books_dir = str(books_dir)
        if not os.path.isdir(books_dir):
            return None
        # Build candidate list once (could be optimized/cached by caller)
        candidates = list(Path(books_dir).rglob("*.pdf"))
        norm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())
        original_stem = norm(Path(original_path).stem) if original_path else ""
        fallback_norms = [norm(t) for t in fallback_titles if t]
        best = None
        best_score = 0
        for c in candidates:
            cstem = norm(c.stem)
            score = 0
            if original_stem and original_stem in cstem:
                score += 3
            for fn in fallback_norms:
                if fn and (fn in cstem or cstem in fn):
                    score += 2
            if score > best_score:
                best_score = score
                best = c
        return str(best) if best else None


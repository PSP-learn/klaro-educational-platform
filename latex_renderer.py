#!/usr/bin/env python3
"""
LaTeX renderer for quiz PDFs using Jinja2 templates and Tectonic.

Requirements:
- pip install Jinja2
- brew install tectonic  (macOS) or use a Tectonic binary on PATH
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, Tuple, List
import subprocess
import tempfile
import shutil
import os

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except Exception as e:
    Environment = None

LATEX_DIR = Path(__file__).parent.parent / 'templates' / 'latex'

LATEX_DEFAULT_INSTRUCTIONS = [
    'Read all questions carefully before starting.',
    'Show all working for calculations.',
    'Use appropriate units and notation.',
]

def _ensure_templates():
    if not LATEX_DIR.exists():
        LATEX_DIR.mkdir(parents=True, exist_ok=True)


def _escape_tex(s: str) -> str:
    if s is None:
        return ''
    # Basic escaping for LaTeX (for non-math text)
    return (s.replace('\\', r'\textbackslash{}')
             .replace('&', r'\&').replace('%', r'\%')
             .replace('#', r'\#').replace('_', r'\_').replace('{', r'\{')
             .replace('}', r'\}').replace('~', r'\textasciitilde{}')
             .replace('^', r'\textasciicircum{}'))

def _escape_tex_preserving_math(s: str) -> str:
    """Escape LaTeX outside math mode, preserve content inside $...$ or $$...$$.
    This allows users to include TeX math that will render properly.
    """
    import re
    if not s:
        return ''
    # Split into math and non-math segments
    pattern = re.compile(r'(\$\$.*?\$\$|\$.*?\$)', re.DOTALL)
    parts = pattern.split(s)
    out: List[str] = []
    for part in parts:
        if not part:
            continue
        if part.startswith('$'):
            # keep math segments as-is
            out.append(part)
        else:
            out.append(_escape_tex(part))
    return ''.join(out)


def _prepare_questions(test_data: Dict) -> List[Dict]:
    qs = []
    for q in test_data['questions']:
        qtext = getattr(q, 'latex_question', None) or _escape_tex_preserving_math(q.question_text)
        options = [ _escape_tex_preserving_math(o) for o in (q.options or []) ]
        qs.append({
            'text': qtext,
            'marks': getattr(q, 'points', 1) or 1,
            'topic': _escape_tex(getattr(q, 'topic', '')),
            'difficulty': _escape_tex(getattr(q, 'difficulty', '')),
            'options': options,
            'answer': _escape_tex_preserving_math(getattr(q, 'correct_answer', '')),
            'explanation': _escape_tex_preserving_math(getattr(q, 'explanation', '')),
        })
    return qs


def _render_to_pdf(template_name: str, context: Dict, out_pdf_path: Path) -> None:
    if Environment is None:
        raise RuntimeError('Jinja2 not installed. Please `pip install Jinja2`.')
    env = Environment(
        loader=FileSystemLoader(str(LATEX_DIR)),
        autoescape=select_autoescape(enabled_extensions=('tex',))
    )
    template = env.get_template(template_name)
    tex_content = template.render(**context)

    with tempfile.TemporaryDirectory() as tmp:
        tex_path = Path(tmp) / 'paper.tex'
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)
        # Compile with tectonic
        cmd = ['tectonic', str(tex_path), '--synctex', 'none', '--keep-logs']
        subprocess.run(cmd, check=True, cwd=tmp)
        pdf_path = Path(tmp) / 'paper.pdf'
        out_pdf_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pdf_path), str(out_pdf_path))


def render_quiz_pdfs(test_data: Dict, filename_prefix: str, output_dir: str = 'generated_tests') -> Tuple[str, str]:
    """Render separate Questions and Answers PDFs using LaTeX templates."""
    _ensure_templates()

    title = test_data.get('title') or 'Test Paper'
    subject = test_data.get('subject') or ''
    instructions = test_data.get('instructions') or LATEX_DEFAULT_INSTRUCTIONS

    qs = _prepare_questions(test_data)

    out_dir = Path(output_dir)
    q_pdf = out_dir / f"{filename_prefix}_questions.pdf"
    a_pdf = out_dir / f"{filename_prefix}_answers.pdf"

    context_common = {
        'title': title,
        'subject': subject,
        'header': test_data.get('header'),
        'instructions': instructions,
        'total_points': sum(q['marks'] for q in qs),
        'questions': qs,
    }

    _render_to_pdf('questions.tex.jinja', context_common, q_pdf)
    _render_to_pdf('answers.tex.jinja', context_common, a_pdf)

    return str(q_pdf), str(a_pdf)


def render_marking_scheme_pdf(test_data: Dict, filename_prefix: str, output_dir: str = 'generated_tests') -> str:
    """Render a Marking Scheme PDF using LaTeX template.
    Expects test_data to include:
      - header, title, subject
      - marking_counts: mapping of type -> count
      - marks_per_type: mapping of type -> per-mark
    """
    _ensure_templates()
    from math import fsum

    title = test_data.get('title') or 'Practice Test'
    subject = test_data.get('subject') or ''
    header = test_data.get('header')
    counts = test_data.get('marking_counts') or {}
    per_marks = test_data.get('marks_per_type') or {}

    # Friendly labels mapping
    label_map = {
        'single_correct': 'Single Correct (1M)',
        'assertion_reason': 'Assertion–Reason (1M)',
        'short2': 'Short Answer (2M)',
        'long3': 'Long Answer (3M)',
        'verylong5': 'Very Long Answer (5M)',
        'case_study': 'Case Study (4M)',
        'mcq': 'MCQ',
        'short': 'Short Answer',
        'long': 'Long Answer',
        'numerical': 'Numerical',
    }
    order_cbse = ['single_correct','assertion_reason','short2','long3','verylong5','case_study']
    # Determine ordering
    keys = list(counts.keys())
    if any(k in order_cbse for k in keys):
        ordered = [k for k in order_cbse if counts.get(k)]
        # include any extra keys at the end
        for k in keys:
            if k not in ordered:
                ordered.append(k)
    else:
        ordered = sorted(keys)

    rows = []
    total_questions = 0
    total_marks = 0
    for k in ordered:
        c = int(counts.get(k, 0) or 0)
        if c <= 0:
            continue
        pm = int(per_marks.get(k, per_marks.get('mcq', 1)))
        sub = c * pm
        rows.append({'key': k, 'label': label_map.get(k, k.title()), 'count': c, 'per_mark': pm, 'subtotal': sub})
        total_questions += c
        total_marks += sub

    notes = []
    # Optional domain notes
    if test_data.get('ui_filters', {}).get('class'):
        pass

    out_dir = Path(output_dir)
    ms_pdf = out_dir / f"{filename_prefix}_marking_scheme.pdf"

    if Environment is None:
        raise RuntimeError('Jinja2 not installed. Please `pip install Jinja2`.')
    env = Environment(
        loader=FileSystemLoader(str(LATEX_DIR)),
        autoescape=select_autoescape(enabled_extensions=('tex',))
    )
    template = env.get_template('marking_scheme.tex.jinja')
    tex = template.render(
        title=title,
        subject=subject,
        header=header,
        rows=rows,
        total_questions=total_questions,
        total_marks=total_marks,
        notes=notes,
    )

    with tempfile.TemporaryDirectory() as tmp:
        tex_path = Path(tmp) / 'scheme.tex'
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(tex)
        cmd = ['tectonic', str(tex_path), '--synctex', 'none', '--keep-logs']
        subprocess.run(cmd, check=True, cwd=tmp)
        pdf_path = Path(tmp) / 'scheme.pdf'
        ms_pdf.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pdf_path), str(ms_pdf))

    return str(ms_pdf)


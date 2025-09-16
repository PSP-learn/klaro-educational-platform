#!/usr/bin/env python3
"""
Parametric math question factory using SymPy for verified question generation.
Generates algebra/trigonometry questions with guaranteed correct answers.
"""
from dataclasses import dataclass
from typing import Optional, List
import random

try:
    import sympy as sp
except Exception:
    sp = None

# Helper RNG bounds for variety while staying textbook-like
_R_SMALL = list(range(-5, 6))
_R_MED = list(range(-9, 10))

@dataclass
class Generated:
    text: str
    qtype: str
    answer: str
    options: Optional[List[str]] = None
    topic: str = 'algebra'
    difficulty: str = 'medium'


def _need_sympy():
    if sp is None:
        raise RuntimeError('SymPy not installed. Please `pip install sympy`.')


def quadratic_roots_mcq() -> Generated:
    _need_sympy()
    # ax^2 + bx + c = 0 with distinct integer roots similar to textbook patterns
    r1 = random.choice(_R_MED) or 2
    r2 = random.choice(_R_MED) or -3
    # ensure distinct roots
    attempts = 0
    while r2 == r1 and attempts < 10:
        r2 = random.choice(_R_MED) or -3
        attempts += 1
    if r2 == r1:
        r2 = r1 + 1
    a = random.choice([1, 1, 1, 2])
    b = -a * (r1 + r2)
    c = a * r1 * r2
    x = sp.symbols('x')
    expr = a*x**2 + b*x + c
    roots = sp.solve(sp.Eq(expr, 0), x)
    if len(roots) < 2:
        roots = [r1, r2]
    # Correct answer as ordered pair
    corr = f"({sp.simplify(roots[0])}, {sp.simplify(roots[1])})"
    # Distractors: perturb coefficients or swap sign
    d1 = f"({sp.simplify(-roots[0])}, {sp.simplify(-roots[1])})"
    d2 = f"({sp.simplify(roots[1])}, {sp.simplify(roots[0])})"
    d3 = f"({sp.simplify(roots[0]+1)}, {sp.simplify(roots[1]-1)})"
    opts = [corr, d1, d2, d3]
    random.shuffle(opts)
    correct_letter = chr(65 + opts.index(corr))
    qtext = f"Find the roots of the quadratic equation $ {sp.latex(expr)} = 0 $."
    return Generated(text=qtext, qtype='mcq', answer=correct_letter, options=opts, topic='algebra', difficulty='medium')


def factorization_short() -> Generated:
    _need_sympy()
    x = sp.symbols('x')
    r1 = random.choice(_R_SMALL) or 2
    r2 = random.choice(_R_SMALL) or -3
    expr = sp.expand((x - r1) * (x - r2))
    qtext = f"Factorize $ {sp.latex(expr)} $."
    ans = f"(x - {r1})(x - {r2})"
    return Generated(text=qtext, qtype='short', answer=ans, options=None, topic='algebra', difficulty='easy')


def linear_equation_mcq() -> Generated:
    _need_sympy()
    x = sp.symbols('x')
    a = random.choice([1, 2, 3, 4, 5])
    b = random.choice(_R_SMALL)
    c = random.choice(_R_SMALL)
    expr = sp.Eq(a*x + b, c)
    sol = sp.solve(expr, x)[0]
    corr = str(sp.simplify(sol))
    # Distractors around the correct integer/rational
    d1 = str(sp.simplify(sol + 1))
    d2 = str(sp.simplify(sol - 1))
    d3 = str(sp.simplify(-sol))
    opts = [corr, d1, d2, d3]
    random.shuffle(opts)
    correct_letter = chr(65 + opts.index(corr))
    qtext = f"Solve the linear equation $ {sp.latex(expr)} $ for $x$."
    return Generated(text=qtext, qtype='mcq', answer=correct_letter, options=opts, topic='algebra', difficulty='easy')


def ap_nth_term_mcq() -> Generated:
    _need_sympy()
    n = random.randint(5, 12)
    a1 = random.choice([1, 2, 3, 4, 5])
    d = random.choice([1, 2, 3, -1, -2])
    an = a1 + (n-1)*d
    corr = str(an)
    d1 = str(an + d)
    d2 = str(an - d)
    d3 = str(a1 + (n-2)*d)
    opts = [corr, d1, d2, d3]
    random.shuffle(opts)
    correct_letter = chr(65 + opts.index(corr))
    qtext = f"In an AP with first term $a_1={a1}$ and common difference $d={d}$, find $a_{n}$ for $n={n}$."
    return Generated(text=qtext, qtype='mcq', answer=correct_letter, options=opts, topic='arithmetic', difficulty='easy')


def trig_special_angle_mcq() -> Generated:
    _need_sympy()
    # Evaluate a basic trig ratio at special angles
    angle_deg = random.choice([30, 45, 60])
    angle = sp.rad(angle_deg)
    func = random.choice(['sin', 'cos', 'tan'])
    if func == 'sin':
        val = sp.nsimplify(sp.sin(angle))
    elif func == 'cos':
        val = sp.nsimplify(sp.cos(angle))
    else:
        val = sp.nsimplify(sp.tan(angle))
    corr = sp.latex(val)
    # Distractors: common confusions
    others = {
        'sin': [sp.latex(sp.nsimplify(sp.cos(angle))), sp.latex(sp.nsimplify(1 - sp.sin(angle))), '0'],
        'cos': [sp.latex(sp.nsimplify(sp.sin(angle))), sp.latex(sp.nsimplify(1 - sp.cos(angle))), '1'],
        'tan': ['1', '0', sp.latex(sp.nsimplify(1/sp.tan(angle)))],
    }[func]
    opts = [corr] + random.sample(others, 3)
    random.shuffle(opts)
    correct_letter = chr(65 + opts.index(corr))
    symbol = {'sin':'\\sin','cos':'\\cos','tan':'\\tan'}[func]
    qtext = f"Evaluate $ {symbol}({angle_deg}^\\circ) $."
    return Generated(text=qtext, qtype='mcq', answer=correct_letter, options=opts, topic='trigonometry', difficulty='easy')


def select_for_topics(topics: List[str], qtype: str) -> Optional[Generated]:
    t = " ".join(topics).lower()
    # Algebraic patterns
    if ('quadratic' in t or 'roots' in t or 'polynomial' in t) and qtype == 'mcq':
        return quadratic_roots_mcq()
    if ('factor' in t or 'factorise' in t or 'factorize' in t) and qtype in ('short', 'mcq'):
        return factorization_short()
    if ('linear' in t or 'equation' in t) and qtype == 'mcq':
        return linear_equation_mcq()
    if ('ap' in t or 'arithmetic progression' in t or 'sequence' in t) and qtype == 'mcq':
        return ap_nth_term_mcq()
    if ('trigonometry' in t or 'sin' in t or 'cos' in t or 'tan' in t) and qtype == 'mcq':
        return trig_special_angle_mcq()
    return None


#!/usr/bin/env python3
"""
Smart Quiz Generator for Mathematics

This enhanced version creates better quality questions by:
- Analyzing mathematical content more intelligently
- Generating contextual questions based on actual content
- Creating realistic answer options
- Focusing on mathematical concepts and problem-solving
"""

import os
import json
import re
import random
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import re
import random
from typing import Optional

# PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

# Try to import the book database; allow running without it (e.g., in lightweight deployments)
BOOK_DB_AVAILABLE = True
try:
    from book_search import BookVectorDB, TextChunk  # type: ignore
except Exception as _e:
    BOOK_DB_AVAILABLE = False
    BookVectorDB = None  # type: ignore
    # Minimal fallback TextChunk for type hints when book_search isn't available
    @dataclass
    class TextChunk:  # type: ignore
        text: str
        book_title: str
        page_number: int
        file_path: str
        chunk_id: str
        chunk_index: int

from param_question_factory import select_for_topics, Generated

@dataclass
class MathQuestion:
    """A mathematical question with enhanced metadata"""
    question_text: str
    question_type: str  # mcq, short, long, numerical, proof
    difficulty: str  # easy, medium, hard
    topic: str
    subtopic: str
    options: List[str] = None
    correct_answer: str = ""
    explanation: str = ""
    source_content: str = ""
    source_book: str = ""
    source_page: int = 0
    points: int = 1
    keywords: List[str] = None
    formula_used: str = ""
    # Rendering controls
    render_mode: str = "text"  # 'text' or 'image'
    render_image_path: str = ""

class MathContentAnalyzer:
    """Analyzes mathematical content to extract concepts and generate questions"""
    
    def __init__(self):
        self.math_patterns = self._load_math_patterns()
        self.formula_patterns = self._load_formula_patterns()
        self.concept_keywords = self._load_concept_keywords()
    
    def _load_math_patterns(self) -> Dict[str, str]:
        """Mathematical patterns for content recognition"""
        return {
            'definition': r'([A-Z][a-zA-Z\s]+)\s+is\s+defined\s+as\s+([^.]+)',
            'formula': r'([A-Z][a-zA-Z\s]*)\s*=\s*([^.]+)',
            'theorem': r'(Theorem|Lemma|Corollary)\s*:?\s*([^.]+)',
            'property': r'(Property|Properties)\s*:?\s*([^.]+)',
            'example': r'(Example|Ex\.)\s*\d*\s*:?\s*([^.]+)',
            'solution': r'(Solution|Sol\.)\s*:?\s*([^.]+)',
            'step': r'Step\s*\d+\s*:?\s*([^.]+)',
            'result': r'(Therefore|Thus|Hence)\s*,?\s*([^.]+)'
        }
    
    def _load_formula_patterns(self) -> List[str]:
        """Common mathematical formula patterns"""
        return [
            r'[a-z]\s*=\s*[^.]+',  # Basic equations
            r'[A-Z]\s*=\s*[^.]+',  # Area, Volume formulas
            r'\([^)]+\)\s*=\s*[^.]+',  # Complex expressions
            r'[a-z]²\s*[+\-]\s*[^.]+',  # Quadratic patterns
            r'sin|cos|tan\s*[^.]+',  # Trigonometric
            r'\d+\s*[+\-×÷]\s*\d+',  # Arithmetic
        ]
    
    def _load_concept_keywords(self) -> Dict[str, List[str]]:
        """Mathematical concept keywords organized by topic"""
        return {
            'algebra': [
                'equation', 'variable', 'coefficient', 'polynomial', 'quadratic', 
                'linear', 'factorization', 'roots', 'discriminant', 'solve'
            ],
            'geometry': [
                'triangle', 'square', 'rectangle', 'circle', 'angle', 'parallel', 
                'perpendicular', 'area', 'perimeter', 'volume', 'surface'
            ],
            'trigonometry': [
                'sine', 'cosine', 'tangent', 'angle', 'hypotenuse', 'adjacent', 
                'opposite', 'elevation', 'depression', 'ratio'
            ],
            'coordinate_geometry': [
                'coordinate', 'axis', 'origin', 'distance', 'midpoint', 'slope', 
                'line', 'graph', 'plot', 'cartesian'
            ],
            'arithmetic': [
                'progression', 'sequence', 'series', 'term', 'difference', 
                'ratio', 'proportion', 'percentage', 'average'
            ],
            'statistics': [
                'mean', 'median', 'mode', 'frequency', 'data', 'distribution', 
                'probability', 'sample', 'population'
            ]
        }
    
    def analyze_content(self, content: str) -> Dict[str, any]:
        """Analyze mathematical content and extract key information"""
        analysis = {
            'definitions': [],
            'formulas': [],
            'examples': [],
            'theorems': [],
            'main_topic': '',
            'subtopics': [],
            'key_concepts': [],
            'difficulty_indicators': []
        }
        
        # Extract definitions
        for match in re.finditer(self.math_patterns['definition'], content, re.IGNORECASE):
            analysis['definitions'].append({
                'concept': match.group(1).strip(),
                'definition': match.group(2).strip()
            })
        
        # Extract formulas
        for pattern in self.formula_patterns:
            for match in re.finditer(pattern, content):
                analysis['formulas'].append(match.group(0))
        
        # Extract examples
        for match in re.finditer(self.math_patterns['example'], content, re.IGNORECASE):
            analysis['examples'].append(match.group(2).strip())
        
        # Determine main topic
        analysis['main_topic'] = self._determine_main_topic(content)
        
        # Extract key concepts
        analysis['key_concepts'] = self._extract_key_concepts(content, analysis['main_topic'])
        
        return analysis
    
    def _determine_main_topic(self, content: str) -> str:
        """Determine the main mathematical topic"""
        content_lower = content.lower()
        topic_scores = {}
        
        for topic, keywords in self.concept_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                topic_scores[topic] = score
        
        return max(topic_scores, key=topic_scores.get) if topic_scores else 'general'
    
    def _extract_key_concepts(self, content: str, main_topic: str) -> List[str]:
        """Extract key mathematical concepts from content"""
        if main_topic not in self.concept_keywords:
            return []
        
        content_lower = content.lower()
        found_concepts = []
        
        for keyword in self.concept_keywords[main_topic]:
            if keyword in content_lower:
                # Find the actual term in original case
                pattern = rf'\b\w*{re.escape(keyword)}\w*\b'
                matches = re.findall(pattern, content, re.IGNORECASE)
                found_concepts.extend(matches)
        
        return list(set(found_concepts))[:5]  # Return top 5 unique concepts

class SmartQuestionGenerator:
    """Generate intelligent mathematical questions"""
    
    def __init__(self, book_db: BookVectorDB):
        self.book_db = book_db
        self.analyzer = MathContentAnalyzer()
        self.question_templates = self._load_smart_templates()
    
    def _load_smart_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load intelligent question templates"""
        return {
            'mcq': {
                'definition': [
                    "What is {concept}?",
                    "How is {concept} defined in mathematics?",
                    "Which statement correctly defines {concept}?",
                    "In the context of {topic}, {concept} means:"
                ],
                'formula': [
                    "What is the formula for {concept}?",
                    "Which formula is used to calculate {concept}?",
                    "The mathematical expression for {concept} is:",
                    "To find {concept}, we use the formula:"
                ],
                'application': [
                    "When do we use {concept}?",
                    "In which type of problem is {concept} applied?",
                    "The main application of {concept} is:",
                    "{concept} is most useful for:"
                ],
                'calculation': [
                    "What is the value of {expression}?",
                    "Calculate: {expression}",
                    "The result of {expression} equals:",
                    "Find the value: {expression}"
                ]
            },
            'short': {
                'explain': [
                    "Explain the concept of {concept}.",
                    "What is {concept}? Explain with an example.",
                    "Describe how {concept} is used in mathematics.",
                    "Briefly explain the importance of {concept}."
                ],
                'solve': [
                    "Solve the equation: {equation}",
                    "Find the value of x in: {equation}",
                    "Calculate: {expression}",
                    "Determine: {problem}"
                ],
                'method': [
                    "Describe the method to solve {problem_type}.",
                    "What steps are involved in {process}?",
                    "How do you approach {problem_type}?",
                    "Outline the procedure for {concept}."
                ]
            },
            'long': [
                "Derive the formula for {concept} and explain its applications.",
                "Prove that {statement} and provide examples.",
                "Discuss the relationship between {concept1} and {concept2}.",
                "Analyze the role of {concept} in solving {problem_type}."
            ]
        }
    
    def generate_question_from_chunk(self, chunk: TextChunk, question_type: str, 
                                   difficulty: str) -> Optional[MathQuestion]:
        """Generate a mathematical question from content chunk"""
        
        # Analyze the content
        analysis = self.analyzer.analyze_content(chunk.text)
        
        if not analysis['key_concepts']:
            return None
        
        # Pick a concept to focus on
        concept = random.choice(analysis['key_concepts'])
        topic = analysis['main_topic']
        
        try:
            if question_type == 'mcq':
                return self._generate_smart_mcq(chunk, concept, topic, analysis, difficulty)
            elif question_type == 'short':
                return self._generate_smart_short_answer(chunk, concept, topic, analysis, difficulty)
            elif question_type == 'long':
                return self._generate_smart_long_answer(chunk, concept, topic, analysis, difficulty)
            else:
                return None
                
        except Exception as e:
            print(f"Warning: Failed to generate question: {e}")
            return None
    
    def _generate_smart_mcq(self, chunk: TextChunk, concept: str, topic: str, 
                          analysis: Dict, difficulty: str) -> MathQuestion:
        """Generate intelligent MCQ"""
        
        # Determine question category
        if analysis['definitions'] and any(concept.lower() in d['concept'].lower() for d in analysis['definitions']):
            category = 'definition'
            # Find the actual definition
            definition = next((d['definition'] for d in analysis['definitions'] 
                             if concept.lower() in d['concept'].lower()), "")
        elif analysis['formulas']:
            category = 'formula'
            definition = ""
        else:
            category = 'application'
            definition = ""
        
        # Generate question
        templates = self.question_templates['mcq'][category]
        template = random.choice(templates)
        question_text = template.format(concept=concept, topic=topic)
        
        # Generate better options
        if category == 'definition' and definition:
            correct_answer = f"{definition[:80]}..." if len(definition) > 80 else definition
            options = [
                correct_answer,
                "A different mathematical concept with similar properties",
                "An unrelated concept from a different chapter",
                "A common misconception about this topic"
            ]
        else:
            # Generic options for other categories
            correct_answer = f"The correct answer related to {concept}"
            options = [
                correct_answer,
                f"An incorrect but plausible answer about {concept}",
                f"A concept from a different mathematical area",
                f"An answer that confuses {concept} with another term"
            ]
        
        # Shuffle and find correct answer
        random.shuffle(options)
        correct_index = options.index(correct_answer)
        correct_letter = chr(65 + correct_index)
        
        return MathQuestion(
            question_text=question_text,
            question_type='mcq',
            difficulty=difficulty,
            topic=topic,
            subtopic=concept,
            options=options,
            correct_answer=correct_letter,
            explanation=f"Based on content from {chunk.book_title}, page {chunk.page_number}",
            source_content=chunk.text[:200] + "...",
            source_book=chunk.book_title,
            source_page=chunk.page_number,
            points=self._calculate_points(difficulty, 'mcq'),
            keywords=analysis['key_concepts'],
            formula_used=analysis['formulas'][0] if analysis['formulas'] else ""
        )
    
    def _generate_smart_short_answer(self, chunk: TextChunk, concept: str, topic: str,
                                   analysis: Dict, difficulty: str) -> MathQuestion:
        """Generate intelligent short answer question"""
        
        # Choose question category based on content
        if analysis['examples']:
            category = 'solve'
            # Extract a problem from examples
            example = analysis['examples'][0]
            question_text = f"Solve: {example}"
        elif analysis['definitions']:
            category = 'explain'
            templates = self.question_templates['short'][category]
            question_text = random.choice(templates).format(concept=concept)
        else:
            category = 'method'
            templates = self.question_templates['short'][category]
            question_text = random.choice(templates).format(
                concept=concept, 
                problem_type=f"{topic} problems",
                process=f"solving {concept}"
            )
        
        # Generate answer guidance
        if analysis['definitions'] and category == 'explain':
            definition = next((d['definition'] for d in analysis['definitions'] 
                             if concept.lower() in d['concept'].lower()), "")
            correct_answer = f"Answer should include: {definition[:100]}..."
        else:
            correct_answer = f"Answer should demonstrate understanding of {concept} with proper mathematical reasoning"
        
        return MathQuestion(
            question_text=question_text,
            question_type='short',
            difficulty=difficulty,
            topic=topic,
            subtopic=concept,
            correct_answer=correct_answer,
            explanation=f"Refer to {chunk.book_title}, page {chunk.page_number}",
            source_content=chunk.text[:300] + "...",
            source_book=chunk.book_title,
            source_page=chunk.page_number,
            points=self._calculate_points(difficulty, 'short'),
            keywords=analysis['key_concepts'],
            formula_used=analysis['formulas'][0] if analysis['formulas'] else ""
        )
    
    def _generate_smart_long_answer(self, chunk: TextChunk, concept: str, topic: str,
                                  analysis: Dict, difficulty: str) -> MathQuestion:
        """Generate intelligent long answer question"""
        
        templates = self.question_templates['long']
        template = random.choice(templates)
        
        # Find a related concept for comparison questions
        related_concept = ""
        if len(analysis['key_concepts']) > 1:
            related_concepts = [c for c in analysis['key_concepts'] if c != concept]
            if related_concepts:
                related_concept = random.choice(related_concepts)
        
        question_text = template.format(
            concept=concept,
            concept1=concept,
            concept2=related_concept,
            statement=f"{concept} has important properties",
            problem_type=f"{topic} problems",
            topic=topic
        )
        
        return MathQuestion(
            question_text=question_text,
            question_type='long',
            difficulty=difficulty,
            topic=topic,
            subtopic=concept,
            correct_answer=f"Detailed explanation should cover the theory, examples, and applications of {concept}",
            explanation=f"Based on comprehensive content from {chunk.book_title}",
            source_content=chunk.text,
            source_book=chunk.book_title,
            source_page=chunk.page_number,
            points=self._calculate_points(difficulty, 'long'),
            keywords=analysis['key_concepts'],
            formula_used=analysis['formulas'][0] if analysis['formulas'] else ""
        )
    
    def _calculate_points(self, difficulty: str, question_type: str) -> int:
        """Calculate points for questions"""
        base_points = {
            'mcq': 1,
            'short': 3,
            'long': 6,
            'numerical': 2,
            'proof': 8
        }
        
        multiplier = {
            'easy': 1,
            'medium': 1.5,
            'hard': 2
        }
        
        return int(base_points.get(question_type, 1) * multiplier.get(difficulty, 1))

class SmartTestGenerator:
    """Generate tests using smart question generation"""
    
    def __init__(self, db_dir: str = "book_db"):
        # Resolve a usable DB path if possible (works in containers and local)
        self.book_db = None
        chosen_dir = None
        if BOOK_DB_AVAILABLE:
            candidates = []
            if db_dir:
                candidates.append(Path(db_dir))
            # Relative to this file (repo layout: backend/.. -> book_db)
            try:
                candidates.append(Path(__file__).resolve().parents[1] / "book_db")
            except Exception:
                pass
            # CWD fallback
            candidates.append(Path.cwd() / "book_db")
            for cand in candidates:
                try:
                    if cand.exists():
                        self.book_db = BookVectorDB(db_dir=str(cand))  # type: ignore
                        chosen_dir = str(cand)
                        break
                except Exception:
                    self.book_db = None
                    continue
        # Question generator depends on book_db; only instantiate when available
        self.question_generator = SmartQuestionGenerator(self.book_db) if self.book_db else None
        self.output_dir = Path("generated_tests")
        self.output_dir.mkdir(exist_ok=True)
        if not self.book_db:
            print("ℹ️ SmartTestGenerator: Book DB not available; parametric (AI-only) mode will be used as fallback.")
        else:
            print(f"✅ SmartTestGenerator: Book DB ready at {chosen_dir}")
    
    def create_test(self, 
                   topics: List[str],
                   num_questions: int = 10,
                   question_types: List[str] = ['mcq', 'short'],
                   difficulty_levels: List[str] = ['easy', 'medium'],
                   subject: str = "Mathematics",
                   mode: str = "mixed",
                   scope_filter: Optional[str] = None,
                   render: str = "auto",
                   books_dir: Optional[str] = None,
                   type_counts: Optional[Dict[str, int]] = None) -> Dict:
        """Create a smart test paper.
        mode:
          - "mixed": synthesize from textbook content (uses DB when available)
          - "source": extract question-like blocks from the source text (exercises/examples)
          - "parametric": AI-only parametric generation (new questions using SymPy), no DB required
        scope_filter: optional substring to restrict to certain files (e.g., "class_10")
        type_counts: optional mapping of question_type -> desired count (e.g., {"mcq": 10, "short": 5})
        """
        
        print(f"🔍 Requested topics: {', '.join(topics)} | mode={mode}")

        # Helper to convert parametric Generated -> MathQuestion
        def _from_generated(gen: Generated, qtype_fallback: Optional[str] = None) -> MathQuestion:
            qt = qtype_fallback or gen.qtype
            return MathQuestion(
                question_text=gen.text,
                question_type=qt,
                difficulty=gen.difficulty,
                topic=gen.topic,
                subtopic='',
                options=gen.options,
                correct_answer=gen.answer,
                explanation="Parametric generator (verified)",
                source_content="",
                source_book="",
                source_page=0,
                points={'mcq': 1, 'short': 3, 'long': 6, 'numerical': 2, 'proof': 8}.get(qt, 1),
                keywords=[],
                formula_used=""
            )

        def _from_generated_seed(gen: Generated, qtype_fallback: Optional[str], seed_chunk: Optional[TextChunk]) -> MathQuestion:
            mq = _from_generated(gen, qtype_fallback)
            if seed_chunk:
                mq.explanation = f"Parametric variant inspired by {seed_chunk.book_title}, page {seed_chunk.page_number}"
                mq.source_book = seed_chunk.book_title
                mq.source_page = seed_chunk.page_number
            return mq

        # PARAMETRIC (AI-only) MODE — generate everything via factories, independent of DB
        if mode == "parametric":
            questions: List[MathQuestion] = []
            # Build seed concepts from DB if available to make questions similar to textbook content
            seeds: List[Tuple[TextChunk, Dict[str, List[str]]]] = []  # (chunk, analysis parts)
            analyzer = self.question_generator.analyzer if self.question_generator else MathContentAnalyzer()
            if self.book_db:
                seed_chunks: List[Tuple[TextChunk, float]] = []
                for topic in topics:
                    seed_chunks.extend(self.book_db.search(topic, top_k=10))  # type: ignore
                # dedupe by chunk_id keeping highest score
                seen: Dict[str, Tuple[TextChunk, float]] = {}
                for ch, sc in seed_chunks:
                    if ch.chunk_id not in seen or sc > seen[ch.chunk_id][1]:
                        seen[ch.chunk_id] = (ch, sc)
                top_chunks = sorted(seen.values(), key=lambda x: x[1], reverse=True)[:12]
                for ch, _ in top_chunks:
                    anal = analyzer.analyze_content(ch.text)
                    seeds.append((ch, {
                        'main': [anal.get('main_topic') or ''],
                        'keys': anal.get('key_concepts') or []
                    }))
            # Fallback if no seeds
            if not seeds:
                # Create a dummy seed so select_for_topics can still match by requested topics
                seeds = [(None, {'main': topics, 'keys': topics})]  # type: ignore

            def _gen_for_type(qtype: str) -> Optional[MathQuestion]:
                # Iterate through seeds to condition generation on textbook concepts
                random.shuffle(seeds)
                for seed in seeds:
                    chunk = seed[0]
                    words = (seed[1]['main'] + seed[1]['keys']) if seed[1] else topics
                    # Try exact type; degrade if unsupported
                    for t in [qtype, 'short' if qtype == 'long' else ('mcq' if qtype == 'short' else 'short'), 'mcq']:
                        g = select_for_topics(words, t)
                        if g:
                            return _from_generated_seed(g, qtype_fallback=t, seed_chunk=chunk)
                return None
            if type_counts and sum(type_counts.values()) > 0:
                for t, cnt in type_counts.items():
                    produced = 0
                    attempts = 0
                    while produced < int(cnt) and attempts < max(40, int(cnt) * 6):
                        attempts += 1
                        mq = _gen_for_type(t)
                        if mq and all(mq.question_text != q.question_text for q in questions):
                            questions.append(mq)
                            produced += 1
                            print(f"  ✓ Generated (AI-only) {t}")
            else:
                pool = question_types or ['mcq', 'short']
                while len(questions) < num_questions:
                    t = random.choice(pool)
                    mq = _gen_for_type(t)
                    if mq and all(mq.question_text != q.question_text for q in questions):
                        questions.append(mq)
            if not questions:
                raise ValueError("Parametric mode failed to generate questions")
            # Build test data
            test_data = {
                'title': f"{subject} Test - {', '.join(topics)}",
                'subject': subject,
                'topics': topics,
                'questions': questions,
                'total_questions': len(questions),
                'total_points': sum(q.points for q in questions),
                'duration_minutes': max(30, len(questions) * 3),
                'difficulty_distribution': self._get_difficulty_distribution(questions),
                'topic_distribution': self._get_topic_distribution(questions),
                'created_at': datetime.now().isoformat()
            }
            print(f"✅ Generated {len(questions)} AI-only questions ({test_data['total_points']} points)")
            return test_data

        # For modes that may use DB, gracefully handle missing DB
        db_ready = self.book_db is not None and BOOK_DB_AVAILABLE

        # Collect relevant content (only if DB is available)
        all_chunks: List[Tuple[TextChunk, float]] = []
        if db_ready:
            for topic in topics:
                results = self.book_db.search(topic, top_k=15)  # type: ignore
                for chunk, score in results:
                    if score > 0.3:  # Only use highly relevant content
                        all_chunks.append((chunk, score))
        
        # Remove duplicates and sort by relevance
        unique_chunks: Dict[str, Tuple[TextChunk, float]] = {}
        for chunk, score in all_chunks:
            if chunk.chunk_id not in unique_chunks or unique_chunks[chunk.chunk_id][1] < score:
                unique_chunks[chunk.chunk_id] = (chunk, score)
        sorted_chunks: List[Tuple[TextChunk, float]] = sorted(unique_chunks.values(), key=lambda x: x[1], reverse=True)
        
        # Optionally restrict to a scope (e.g., class_10 only)
        if scope_filter:
            sorted_chunks = [cs for cs in sorted_chunks if scope_filter.lower() in cs[0].file_path.lower()]
        
        print(f"📚 Found {len(sorted_chunks)} relevant content chunks (DB ready={db_ready})")
        
        # Source-only extraction mode (pull real questions from the book text)
        if mode == "source":
            if not db_ready or not sorted_chunks:
                print("⚠️ Source mode requested but content DB is unavailable. Falling back to AI-only parametric generation.")
                # Fallback to parametric
                return self.create_test(topics, num_questions, question_types, difficulty_levels, subject,
                                        mode="parametric", scope_filter=scope_filter, render=render,
                                        books_dir=books_dir, type_counts=type_counts)
            questions = self._extract_source_questions(sorted_chunks, topics, num_questions)
            # Try to upgrade to image rendering if requested
            if render in ("auto", "image"):
                try:
                    from source_question_extractor import PDFQuestionExtractor
                    extractor = PDFQuestionExtractor()
                    # Build candidate files list from chunks
                    candidate_files = []
                    for chunk, _ in sorted_chunks:
                        candidate_files.append((chunk.file_path, chunk.book_title))
                    # Deduplicate while preserving order
                    seen = set()
                    unique_candidates = []
                    for fp, title in candidate_files:
                        key = (fp, title)
                        if key not in seen:
                            seen.add(key)
                            unique_candidates.append((fp, title))
                    # Try each candidate to extract and render images
                    image_questions: List[MathQuestion] = []
                    for fp, title in unique_candidates:
                        if len(image_questions) >= num_questions:
                            break
                        resolved = extractor.try_resolve_file(fp, books_dir, [title])
                        if not resolved:
                            continue
                        sqs = extractor.extract_questions_from_file(resolved, topics=topics,
                                                                    max_questions=max(3, num_questions // 2))
                        for sq in sqs:
                            if len(image_questions) >= num_questions:
                                break
                            img = extractor.render_question_image(resolved, sq.page_number, sq.bbox)
                            if not img:
                                continue
                            mq = MathQuestion(
                                question_text=sq.text,
                                question_type='short' if not sq.options else 'mcq',
                                difficulty='medium',
                                topic=self.question_generator.analyzer._determine_main_topic(sq.text) if self.question_generator else 'general',
                                subtopic='',
                                options=sq.options if sq.options else None,
                                correct_answer="",
                                explanation=f"From {Path(resolved).name}, page {sq.page_number}",
                                source_content=sq.text[:300] + "...",
                                source_book=Path(resolved).stem,
                                source_page=sq.page_number,
                                points=self._calculate_points('medium', 'short' if not sq.options else 'mcq'),
                                keywords=(self.question_generator.analyzer._extract_key_concepts(sq.text, self.question_generator.analyzer._determine_main_topic(sq.text)) if self.question_generator else []),
                                formula_used="",
                                render_mode='image',
                                render_image_path=img
                            )
                            image_questions.append(mq)
                    if image_questions:
                        questions = image_questions[:num_questions]
                except Exception as e:
                    print(f"⚠️ Image rendering failed, falling back to text-only: {e}")
        else:
            # MIXED generation (prefers DB; falls back to parametric)
            if not db_ready or not sorted_chunks:
                print("ℹ️ Content DB not available or empty. Using AI-only parametric generation for mixed mode.")
                return self.create_test(topics, num_questions, question_types, difficulty_levels, subject,
                                        mode="parametric", scope_filter=scope_filter, render=render,
                                        books_dir=books_dir, type_counts=type_counts)
            # When counts per type provided, honor them
            if type_counts and sum(type_counts.values()) > 0:
                total_needed = sum(type_counts.values())
                print(f"🎯 Generating by type counts: {type_counts} (total {total_needed})")
                questions = []
                for qtype, qcount in type_counts.items():
                    produced = 0
                    attempts = 0
                    max_attempts = max(qcount * 8, 40)
                    # Try parametric first to ensure quality/variety
                    while produced < qcount and attempts < max_attempts:
                        attempts += 1
                        gen = select_for_topics(topics, qtype)
                        if gen:
                            mq = _from_generated(gen, qtype_fallback=qtype)
                            if mq and all(mq.question_text != q.question_text for q in questions):
                                questions.append(mq)
                                produced += 1
                                print(f"  ✓ Generated (parametric) {qtype}")
                                continue
                        # Otherwise fallback to chunk-based synthesis
                        chunk, score = random.choice(sorted_chunks)
                        difficulty = random.choice(difficulty_levels)
                        q = self.question_generator.generate_question_from_chunk(chunk, qtype, difficulty) if self.question_generator else None
                        if q and all(q.question_text != qq.question_text for qq in questions):
                            questions.append(q)
                            produced += 1
                            print(f"  ✓ Generated {qtype} (chunk) about {q.subtopic}")
                # Fallback: if we couldn't reach target, fill randomly
                if len(questions) < total_needed:
                    print(f"⚠️ Could not reach target per-type counts. Filling remaining {total_needed - len(questions)} randomly.")
                    attempts = 0
                    max_attempts = len(sorted_chunks) * 2
                    while len(questions) < total_needed and attempts < max_attempts:
                        attempts += 1
                        chunk, score = random.choice(sorted_chunks)
                        qtype = random.choice(list(type_counts.keys()))
                        difficulty = random.choice(difficulty_levels)
                        q = self.question_generator.generate_question_from_chunk(chunk, qtype, difficulty) if self.question_generator else None
                        if q and all(q.question_text != qq.question_text for qq in questions):
                            questions.append(q)
                            print(f"  ✓ Generated {qtype} (chunk) about {q.subtopic}")
            else:
                print(f"🎯 Generating {num_questions} questions (mixed)...")
                # Generate questions (templated synthesis)
                questions = []
                attempts = 0
                max_attempts = len(sorted_chunks) * 2
                
                while len(questions) < num_questions and attempts < max_attempts:
                    attempts += 1
                    # Pick random chunk, question type, and difficulty
                    chunk, score = random.choice(sorted_chunks)
                    question_type = random.choice(question_types)
                    difficulty = random.choice(difficulty_levels)
                    # Generate question
                    question = self.question_generator.generate_question_from_chunk(
                        chunk, question_type, difficulty
                    ) if self.question_generator else None
                    if question and all(question.question_text != qq.question_text for qq in questions):
                        questions.append(question)
                        print(f"  ✓ Generated {question_type} (chunk) about {question.subtopic}")
        
        if not questions:
            raise ValueError("Failed to generate any questions from the content")
        
        # Create test paper data
        test_data = {
            'title': f"{subject} Test - {', '.join(topics)}",
            'subject': subject,
            'topics': topics,
            'questions': questions,
            'total_questions': len(questions),
            'total_points': sum(q.points for q in questions),
            'duration_minutes': max(30, len(questions) * 3),  # Estimate 3 min per question
            'difficulty_distribution': self._get_difficulty_distribution(questions),
            'topic_distribution': self._get_topic_distribution(questions),
            'created_at': datetime.now().isoformat()
        }
        
        print(f"✅ Generated {len(questions)} questions ({test_data['total_points']} points)")
        return test_data
    
    def _extract_source_questions(self, sorted_chunks: List[Tuple[TextChunk, float]], topics: List[str], num_questions: int) -> List[MathQuestion]:
        """Extract exercise/example-like questions directly from the source text.
        Heuristics: detect enumerated lines (1., Q1, Example 1) and gather block until next header/blank.
        """
        results: List[MathQuestion] = []
        topic_set = set(t.lower() for t in topics)
        for chunk, score in sorted_chunks:
            if len(results) >= num_questions:
                break
            lines = [ln.strip() for ln in chunk.text.splitlines()]
            i = 0
            while i < len(lines) and len(results) < num_questions:
                ln = lines[i]
                header = re.match(r"^(?:Q\.?\s*\d+|\d+\.|\(\d+\)|Example\s*\d+|EXERCISE\s*\d+(?:\.\d+)?)\b", ln, flags=re.IGNORECASE)
                if header:
                    # Collect subsequent non-empty lines until a stopping condition
                    block = [ln]
                    j = i + 1
                    while j < len(lines):
                        nxt = lines[j]
                        if not nxt:
                            break
                        # Stop if next header starts
                        if re.match(r"^(?:Q\.?\s*\d+|\d+\.|\(\d+\)|Example\s*\d+|EXERCISE\s*\d+(?:\.\d+)?)\b", nxt, flags=re.IGNORECASE):
                            break
                        block.append(nxt)
                        j += 1
                    text_block = " ".join(block)
                    # Basic topical filter
                    if any(t in text_block.lower() for t in topic_set) or any(t in chunk.book_title.lower() for t in topic_set):
                        q_text = re.sub(r"^EXERCISE[^:]*:\s*", "", text_block, flags=re.IGNORECASE)
                        q_text = re.sub(r"^Example\s*\d+\s*:?\s*", "", q_text, flags=re.IGNORECASE)
                        q_text = re.sub(r"^Q\.?\s*\d+\s*:?\s*", "", q_text, flags=re.IGNORECASE)
                        q_text = re.sub(r"^\d+\.|^\(\d+\)\s*", "", q_text).strip()
                        if len(q_text) > 25:  # avoid extremely short headers
                            mq = MathQuestion(
                                question_text=q_text,
                                question_type='short',
                                difficulty='medium',
                                topic=self.question_generator.analyzer._determine_main_topic(text_block) or 'general',
                                subtopic='',
                                correct_answer="",
                                explanation=f"From {chunk.book_title}, page {chunk.page_number}",
                                source_content=chunk.text[:300] + "...",
                                source_book=chunk.book_title,
                                source_page=chunk.page_number,
                                points=self._calculate_points('medium', 'short'),
                                keywords=self.question_generator.analyzer._extract_key_concepts(text_block, self.question_generator.analyzer._determine_main_topic(text_block)),
                                formula_used=""
                            )
                            results.append(mq)
                    i = j
                else:
                    i += 1
        return results

    def _get_difficulty_distribution(self, questions: List[MathQuestion]) -> Dict[str, int]:
        """Get distribution of questions by difficulty"""
        dist = {}
        for q in questions:
            dist[q.difficulty] = dist.get(q.difficulty, 0) + 1
        return dist
    
    def _get_topic_distribution(self, questions: List[MathQuestion]) -> Dict[str, int]:
        """Get distribution of questions by topic"""
        dist = {}
        for q in questions:
            dist[q.topic] = dist.get(q.topic, 0) + 1
        return dist
    
    def save_test(self, test_data: Dict, filename_prefix: str) -> Tuple[str, str]:
        """Save test paper and answer key (TXT)."""
        
        # Generate test paper content
        test_content = self._format_test_paper(test_data)
        answer_content = self._format_answer_key(test_data)
        
        # Save files
        test_file = self.output_dir / f"{filename_prefix}_questions.txt"
        answer_file = self.output_dir / f"{filename_prefix}_answers.txt"
        metadata_file = self.output_dir / f"{filename_prefix}_metadata.json"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        with open(answer_file, 'w', encoding='utf-8') as f:
            f.write(answer_content)
        
        # Save metadata (convert questions to dict)
        metadata = test_data.copy()
        metadata['questions'] = [asdict(q) for q in test_data['questions']]
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        return str(test_file), str(answer_file)

    def save_test_pdf(self, test_data: Dict, filename_prefix: str) -> Tuple[str, str]:
        """Save test paper and answer key as PDF using reportlab."""
        pdf_questions = self.output_dir / f"{filename_prefix}_questions.pdf"
        pdf_answers = self.output_dir / f"{filename_prefix}_answers.pdf"
        
        # Build Questions PDF
        self._build_questions_pdf(test_data, pdf_questions)
        # Build Answers PDF
        self._build_answers_pdf(test_data, pdf_answers)
        
        return str(pdf_questions), str(pdf_answers)

    def _build_questions_pdf(self, test_data: Dict, out_path: Path):
        doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        elements = []
        
        title = test_data.get('title') or 'Test Paper'
        elements.append(Paragraph(title, styles['Heading1']))
        meta = f"Subject: {test_data.get('subject','')} | Topics: {', '.join(test_data.get('topics', []))} | Duration: {test_data.get('duration_minutes','')} min | Total Points: {test_data.get('total_points','')}"
        elements.append(Paragraph(meta, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Instructions
        elements.append(Paragraph('Instructions:', styles['Heading2']))
        instructions = [
            'Read all questions carefully before starting.',
            'Show all your work for mathematical calculations.',
            'For MCQs, choose the BEST answer.',
            'Write clearly and manage your time effectively.'
        ]
        for inst in instructions:
            elements.append(Paragraph(f"• {inst}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Questions
        for i, q in enumerate(test_data['questions'], 1):
            header = f"Q{i}."
            elements.append(Paragraph(header, styles['Heading3']))
            sub = f"[Topic: {q.topic.title()}, Difficulty: {q.difficulty.title()}, Points: {q.points}]"
            elements.append(Paragraph(sub, styles['Italic']))
            if getattr(q, 'render_mode', 'text') == 'image' and getattr(q, 'render_image_path', ''):
                try:
                    img = Image(q.render_image_path)
                    # Scale to page width (A4 minus margins ~ 17 cm)
                    max_width = 17 * cm
                    scale = min(1.0, max_width / img.drawWidth)
                    img.drawWidth = img.drawWidth * scale
                    img.drawHeight = img.drawHeight * scale
                    elements.append(img)
                except Exception:
                    # Fallback to text
                    elements.append(Paragraph(q.question_text, styles['BodyText']))
            else:
                elements.append(Paragraph(q.question_text, styles['BodyText']))
                if q.options:
                    for j, opt in enumerate(q.options):
                        elements.append(Paragraph(f"{chr(65+j)}. {opt}", styles['Normal']))
            # Answer space
            elements.append(Spacer(1, 6))
            elements.append(Paragraph("Answer:", styles['Normal']))
            elements.append(Spacer(1, 14))
            elements.append(Paragraph("_" * 90, styles['Normal']))
            elements.append(Spacer(1, 18))
        
        doc.build(elements)

    def _build_answers_pdf(self, test_data: Dict, out_path: Path):
        doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        elements = []
        
        title = f"ANSWER KEY - {test_data.get('title') or 'Test'}"
        elements.append(Paragraph(title, styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        for i, q in enumerate(test_data['questions'], 1):
            elements.append(Paragraph(f"Q{i}. {q.correct_answer}", styles['BodyText']))
            if q.explanation:
                elements.append(Paragraph(f"Explanation: {q.explanation}", styles['Normal']))
            elements.append(Paragraph(f"Source: {q.source_book}, Page {q.source_page}", styles['Normal']))
            if q.formula_used:
                elements.append(Paragraph(f"Formula: {q.formula_used}", styles['Normal']))
            elements.append(Paragraph(f"Points: {q.points}", styles['Normal']))
            elements.append(Spacer(1, 8))
        
        # Statistics
        elements.append(PageBreak())
        elements.append(Paragraph("TEST STATISTICS", styles['Heading2']))
        elements.append(Paragraph(f"Total Questions: {test_data['total_questions']}", styles['Normal']))
        elements.append(Paragraph(f"Total Points: {test_data['total_points']}", styles['Normal']))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("Difficulty Distribution:", styles['Normal']))
        for difficulty, count in test_data['difficulty_distribution'].items():
            elements.append(Paragraph(f"- {difficulty.title()}: {count} questions", styles['Normal']))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("Topic Distribution:", styles['Normal']))
        for topic, count in test_data['topic_distribution'].items():
            elements.append(Paragraph(f"- {topic.title()}: {count} questions", styles['Normal']))
        
        doc.build(elements)
    
    def _format_test_paper(self, test_data: Dict) -> str:
        """Format test paper for printing"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"📝 {test_data['title']}")
        lines.append("=" * 80)
        lines.append(f"Subject: {test_data['subject']}")
        lines.append(f"Topics: {', '.join(test_data['topics'])}")
        lines.append(f"Duration: {test_data['duration_minutes']} minutes")
        lines.append(f"Total Points: {test_data['total_points']}")
        lines.append(f"Total Questions: {test_data['total_questions']}")
        lines.append("")
        
        # Instructions
        lines.append("📋 INSTRUCTIONS:")
        lines.append("• Read all questions carefully before starting")
        lines.append("• Show all your work for mathematical calculations")
        lines.append("• For MCQs, choose the BEST answer")
        lines.append("• Write clearly and legibly")
        lines.append("• Manage your time effectively")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
        
        # Questions
        for i, question in enumerate(test_data['questions'], 1):
            lines.append(f"Q{i}. {question.question_text}")
            lines.append(f"     [Topic: {question.topic.title()}, Difficulty: {question.difficulty.title()}, Points: {question.points}]")
            
            if question.options:
                for j, option in enumerate(question.options):
                    lines.append(f"     {chr(65 + j)}. {option}")
            
            lines.append("")
            lines.append("     Answer:")
            lines.append("     " + "_" * 50)
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_answer_key(self, test_data: Dict) -> str:
        """Format answer key"""
        lines = []
        lines.append("=" * 80)
        lines.append(f"📚 ANSWER KEY - {test_data['title']}")
        lines.append("=" * 80)
        lines.append("")
        
        for i, question in enumerate(test_data['questions'], 1):
            lines.append(f"Q{i}. {question.correct_answer}")
            
            if question.explanation:
                lines.append(f"     📖 Explanation: {question.explanation}")
            
            lines.append(f"     📍 Source: {question.source_book}, Page {question.source_page}")
            
            if question.formula_used:
                lines.append(f"     📐 Formula: {question.formula_used}")
            
            lines.append(f"     💯 Points: {question.points}")
            lines.append("")
        
        # Add statistics
        lines.append("=" * 80)
        lines.append("📊 TEST STATISTICS")
        lines.append("=" * 80)
        lines.append(f"Total Questions: {test_data['total_questions']}")
        lines.append(f"Total Points: {test_data['total_points']}")
        lines.append("")
        
        lines.append("Difficulty Distribution:")
        for difficulty, count in test_data['difficulty_distribution'].items():
            lines.append(f"  {difficulty.title()}: {count} questions")
        
        lines.append("")
        lines.append("Topic Distribution:")
        for topic, count in test_data['topic_distribution'].items():
            lines.append(f"  {topic.title()}: {count} questions")
        
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Smart Mathematics Quiz Generator")
    parser.add_argument('--topics', '-t', required=True, help='Topics for quiz (comma-separated)')
    parser.add_argument('--questions', '-q', type=int, default=10, help='Number of questions')
    parser.add_argument('--types', type=str, default='mcq,short', help='Question types')
    parser.add_argument('--difficulty', '-d', type=str, default='easy,medium', help='Difficulty levels')
    parser.add_argument('--subject', '-s', type=str, default='Mathematics', help='Subject')
    parser.add_argument('--output', '-o', type=str, help='Output filename prefix')
    parser.add_argument('--preview', action='store_true', help='Show preview only')
    
    args = parser.parse_args()
    
    # Parse inputs
    topics = [t.strip() for t in args.topics.split(',')]
    question_types = [t.strip() for t in args.types.split(',')]
    difficulty_levels = [d.strip() for d in args.difficulty.split(',')]
    
    # Create generator
    generator = SmartTestGenerator()
    
    try:
        # Generate test
        test_data = generator.create_test(
            topics=topics,
            num_questions=args.questions,
            question_types=question_types,
            difficulty_levels=difficulty_levels,
            subject=args.subject
        )
        
        # Output filename
        output_prefix = args.output or f"smart_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if args.preview:
            # Just show preview
            print("\n" + "=" * 80)
            print("📋 TEST PREVIEW")
            print("=" * 80)
            for i, q in enumerate(test_data['questions'][:3], 1):
                print(f"\nQ{i}. {q.question_text}")
                if q.options:
                    for j, opt in enumerate(q.options):
                        print(f"     {chr(65 + j)}. {opt}")
                print(f"     [Points: {q.points}, Difficulty: {q.difficulty}]")
            
            if len(test_data['questions']) > 3:
                print(f"\n... and {len(test_data['questions']) - 3} more questions")
        else:
            # Save test
            test_file, answer_file = generator.save_test(test_data, output_prefix)
            
            print(f"\n🎉 Smart test generated successfully!")
            print(f"📄 Test Questions: {test_file}")
            print(f"📚 Answer Key: {answer_file}")
            print(f"💡 Contains {test_data['total_questions']} questions worth {test_data['total_points']} points")
            
    except Exception as e:
        print(f"❌ Test generation failed: {e}")

if __name__ == "__main__":
    main()

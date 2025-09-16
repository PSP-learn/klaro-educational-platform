# Quiz Builder: Product Vision and Architecture

Last updated: 2025-09-08

Goal
- Single-tab, highly-configurable Quiz Builder that produces polished, aligned test PDFs with beautiful math and per-question marks.

One-tab layout (progressive disclosure)
1) Header bar
   - Exam type, Class, Subject, Language, Date, Random seed
2) Accordion: Source material
   - Books directory, scope filters (e.g., class_10), centers, streams, mode (mixed/source), render (auto/image/text)
3) Accordion: Topics
   - Topics, subtopics, tags (include/exclude later)
4) Accordion: Blueprint
   - Total questions, per-type counts (mcq/short/long/etc.), difficulty distribution, optional duration
5) Accordion: Sections A/B/C
   - For each: name, allowed types, count, difficulty mix (later), negative marking (later)
6) Accordion: Scoring & marking
   - Marks per type; later: per-section or per-question overrides
7) Accordion: Rendering & formatting
   - Output engine (ReportLab now, LaTeX later), include solutions, page settings
8) Accordion: Instructions & metadata
   - Ordered list of instructions, metadata fields

Backend API (current)
- POST /api/quiz/preview
  - Input: QuizRequest including blueprint & sections
  - Output: PreviewResponse with normalized totals, duration estimate, warnings
- POST /api/quiz/create
  - Uses SmartTestGenerator; honors mode/scope/render and blueprint total
  - Returns file links; UI filters echoed in metadata

Data schema (subset)
- QuizRequest
  - topics, subject, mode, render, scope_filter, books_dir
  - blueprint { total_questions, by_type, by_difficulty, duration_minutes }
  - sections [{ name, types[], count, difficulty?, negative_marking? }]
  - marks { per-type }
  - UI filters: streams, class_filter, topic_tags, subtopics, language, centers

Rendering roadmap
- Now: ReportLab PDFs (supports image-based equations via source-mode crops)
- Next: LaTeX engine (exam class) for perfect alignment, TeX equations, and elegant instructions
- Optional: Math OCR integration (Mathpix) to convert image regions to TeX; cache results

Selection logic roadmap
- Phase 1: Greedy allocation matching blueprint counts and types/difficulty as hints
- Phase 2: Constraint solver to allocate per-section counts with topic/difficulty caps and fallbacks
- Phase 3: Analytics: availability counts by topic/type/difficulty; live validation in preview

UX principles
- Progressive disclosure; Advanced toggles per accordion
- Sticky right summary with live totals and warnings
- Presets and saved templates for quick re-use
- Inline marks editor after preview (future)

Open items / Next steps
- Hook blueprint/sections into generator selection strategy
- Add LaTeX renderer using Tectonic and Jinja template
- Enhance preview to reflect actual availability from the DB
- Add templates save/load endpoints


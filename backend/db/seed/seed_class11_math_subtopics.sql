-- =============================================================================
-- seed_class11_math_subtopics.sql
-- NCERT-style subtopics for Class 11 Mathematics
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Sets =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Representation of Sets', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Sets' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Operations on Sets', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Sets' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Venn Diagrams', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Sets' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Relations & Functions =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Types of Relations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Functions & Graphs', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Domain, Range & Co-domain', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Trigonometric Functions =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Trigonometric Identities', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Trigonometric Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Graphs of Trig Functions', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Trigonometric Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Complex Numbers and Quadratic Equations =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Complex Number Basics', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Complex Numbers and Quadratic Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Argand Plane & Polar Form', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Complex Numbers and Quadratic Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Quadratic Equations & Nature of Roots', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Complex Numbers and Quadratic Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Permutations and Combinations =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Permutations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Permutations and Combinations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Combinations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Permutations and Combinations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Binomial Theorem =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Binomial Expansion', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Binomial Theorem' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'General & Middle Terms', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Binomial Theorem' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Sequences and Series =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Arithmetic Progression (AP)', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Sequences and Series' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Geometric Progression (GP)', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Sequences and Series' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Straight Lines =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Slope & Intercepts', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Straight Lines' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Point-Slope & Two-Point Form', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Straight Lines' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Conic Sections =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Parabola', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Conic Sections' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ellipse', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Conic Sections' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Hyperbola', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Conic Sections' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Limits & Derivatives =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Limits Basics', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Limits & Derivatives' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Derivatives Basics', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Limits & Derivatives' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Statistics =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Measures of Central Tendency', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Statistics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Measures of Dispersion', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Statistics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Probability =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Classical Probability', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Probability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conditional Probability (Basics)', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Probability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


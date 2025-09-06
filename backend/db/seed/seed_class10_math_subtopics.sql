-- =============================================================================
-- seed_class10_math_subtopics.sql
-- NCERT-style subtopics for Class 10 Mathematics
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Real Numbers
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Euclid''s Division Lemma & FTA', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Real Numbers' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Polynomials
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Zeros & Coefficient Relations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Polynomials' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Pair of Linear Equations in Two Variables
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Graphical & Algebraic Methods', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Pair of Linear Equations in Two Variables' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Quadratic Equations
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Factoring, Completing Square & Formula', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Quadratic Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Arithmetic Progressions
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Nth Term & Sum of n Terms', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Arithmetic Progressions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Triangles
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Similarity & Pythagoras Theorem', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Triangles' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Coordinate Geometry
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Distance, Section Formula & Area', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Coordinate Geometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Introduction to Trigonometry
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Trig Ratios & Identities', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Introduction to Trigonometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Applications of Trigonometry
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Heights & Distances', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Applications of Trigonometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Circles
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Tangents & Secants', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Circles' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Statistics
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Grouped Data: Mean, Median & Mode', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Statistics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Probability
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Classical Probability & Complement', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Probability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


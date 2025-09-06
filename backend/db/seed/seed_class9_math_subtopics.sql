-- =============================================================================
-- seed_class9_math_subtopics.sql
-- NCERT-style subtopics for Class 9 Mathematics
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Number Systems
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Irrational Numbers & Real Line', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Number Systems' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Laws of Exponents for Real Numbers', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Number Systems' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Polynomials
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Zeros, Graphs & Remainder Theorem', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Polynomials' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Coordinate Geometry
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Cartesian Plane & Plotting Points', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Coordinate Geometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Linear Equations in Two Variables
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Solutions & Graphs of Linear Equations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Linear Equations in Two Variables' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Triangles
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Congruence & Properties', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Triangles' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Quadrilaterals
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Parallelogram Properties & Midpoint Theorem', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Quadrilaterals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Statistics
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Frequency, Mean, Median & Mode', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Statistics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


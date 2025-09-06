-- =============================================================================
-- seed_class12_math_subtopics.sql
-- NCERT-style subtopics for Class 12 Mathematics
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Helper: insert a subtopic under a given chapter name
-- Usage pattern repeated for each chapter
-- insert into topics (subject_id, grade_id, name, parent_id)
-- select s.id, g.id, '<SUBTOPIC>', p.id
-- from subjects s, grades g, topics p
-- where s.name='Mathematics' and g.name='Class 12'
--   and p.subject_id=s.id and p.grade_id=g.id and p.name='<CHAPTER>' and p.parent_id is null
-- on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Relations & Functions =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Types of Relations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Equivalence Relations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Composition of Functions', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Invertible Functions', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Relations & Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Inverse Trigonometric Functions =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Principal Values', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Inverse Trigonometric Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Properties & Identities', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Inverse Trigonometric Functions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Matrices =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Types of Matrices', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Matrices' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Matrix Operations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Matrices' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Adjoint & Inverse', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Matrices' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Determinants =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Properties of Determinants', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Determinants' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Cramer''s Rule', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Determinants' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Continuity & Differentiability =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Continuity', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Continuity & Differentiability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Differentiability', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Continuity & Differentiability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Chain Rule & Logarithmic Differentiation', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Continuity & Differentiability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Application of Derivatives =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Rate of Change', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Application of Derivatives' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Increasing/Decreasing Functions', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Application of Derivatives' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Tangents & Normals', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Application of Derivatives' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Maxima & Minima', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Application of Derivatives' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Integrals =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Indefinite Integrals', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Integrals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Definite Integrals', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Integrals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Integration Techniques', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Integrals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Integration by Parts', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Integrals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Substitution Method', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Integrals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Partial Fractions', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Integrals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Differential Equations =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Order and Degree', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Differential Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'General & Particular Solutions', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Differential Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'First Order Linear DE', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Differential Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Variable Separables', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Differential Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Homogeneous Equations', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Differential Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Applications of DE', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Differential Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Vector Algebra =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Basics & Components', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Vector Algebra' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Scalar (Dot) Product', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Vector Algebra' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Vector (Cross) Product', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Vector Algebra' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Three Dimensional Geometry =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Direction Cosines & Ratios', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Three Dimensional Geometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Line in 3D', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Three Dimensional Geometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plane in 3D', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Three Dimensional Geometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Distances and Angles', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Three Dimensional Geometry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Probability =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conditional Probability', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Probability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Bayes'' Theorem', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Probability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Random Variables & Mean', p.id
from subjects s, grades g, topics p
where s.name='Mathematics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Probability' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


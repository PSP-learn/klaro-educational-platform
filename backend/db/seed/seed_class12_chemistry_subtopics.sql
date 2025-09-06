-- =============================================================================
-- seed_class12_chemistry_subtopics.sql
-- NCERT-style subtopics for Class 12 Chemistry
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Solid State =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Crystal Lattices & Unit Cells', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Solid State' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Packing Efficiency & Density', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Solid State' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Crystal Defects', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Solid State' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Solutions =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Concentration Terms & Henry''s Law', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Solutions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Raoult''s Law & Ideal Solutions', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Solutions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Colligative Properties', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Solutions' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Electrochemistry =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Electrochemical Cells & EMF', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electrochemistry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Nernst Equation & Cell Potentials', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electrochemistry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conductance & Kohlrausch''s Law', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electrochemistry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Chemical Kinetics =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Rate of Reaction & Rate Laws', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Chemical Kinetics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Order, Molecularity & Half-life', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Chemical Kinetics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Arrhenius Equation & Activation Energy', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Chemical Kinetics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


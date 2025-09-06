-- =============================================================================
-- seed_class11_chemistry_subtopics.sql
-- NCERT-style subtopics for Class 11 Chemistry
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Some Basic Concepts of Chemistry =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Mole Concept', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Some Basic Concepts of Chemistry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Stoichiometry', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Some Basic Concepts of Chemistry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Limiting Reagent & Yield', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Some Basic Concepts of Chemistry' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Structure of Atom =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Bohr Model & Spectra', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Structure of Atom' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Quantum Numbers', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Structure of Atom' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Electronic Configuration', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Structure of Atom' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Thermodynamics =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'First Law & Enthalpy', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Thermodynamics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Entropy & Second Law', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Thermodynamics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Gibbs Free Energy & Spontaneity', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Thermodynamics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Equilibrium =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Chemical Equilibrium & Kc, Kp', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Equilibrium' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Le Chatelier''s Principle', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Equilibrium' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ionic Equilibrium & pH', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Equilibrium' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


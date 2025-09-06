-- =============================================================================
-- seed_class12_physics_subtopics.sql
-- NCERT-style subtopics for Class 12 Physics
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Electric Charges & Fields =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Coulomb''s Law', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electric Charges & Fields' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Electric Field Lines', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electric Charges & Fields' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Gauss''s Law', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electric Charges & Fields' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Electrostatic Potential & Capacitance =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Potential & Potential Difference', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electrostatic Potential & Capacitance' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Equipotential Surfaces', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electrostatic Potential & Capacitance' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Capacitors & Dielectrics', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Electrostatic Potential & Capacitance' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Current Electricity =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ohm''s Law & Resistivity', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Current Electricity' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Series & Parallel Circuits', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Current Electricity' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Kirchhoff''s Laws & Bridge Circuits', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Current Electricity' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Moving Charges & Magnetism =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Biot–Savart Law', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Moving Charges & Magnetism' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ampere''s Law', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Moving Charges & Magnetism' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Lorentz Force & Cyclotron', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Moving Charges & Magnetism' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Ray Optics =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Reflection & Refraction', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Ray Optics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Lenses & Lensmaker''s Formula', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Ray Optics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Optical Instruments', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Ray Optics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Wave Optics =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Interference (Young''s Experiment)', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Wave Optics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Diffraction & Resolving Power', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Wave Optics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Polarization', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Wave Optics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


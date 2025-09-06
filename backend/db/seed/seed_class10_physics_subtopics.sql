-- =============================================================================
-- seed_class10_physics_subtopics.sql
-- NCERT-style subtopics for Class 10 Physics
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Light - Reflection and Refraction
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Reflection: Mirrors & Ray Diagrams', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Light - Reflection and Refraction' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Refraction & Refractive Index, TIR', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Light - Reflection and Refraction' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- The Human Eye and the Colourful World
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Structure of Human Eye & Defects', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='The Human Eye and the Colourful World' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Dispersion, Scattering & Rainbow', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='The Human Eye and the Colourful World' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Electricity
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ohm''s Law, Resistance & Resistivity', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Electricity' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Series/Parallel, Power & Heating Effect', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Electricity' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Magnetic Effects of Electric Current
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Magnetic Field, Right-hand Thumb Rule', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Magnetic Effects of Electric Current' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Force on Conductor, Motors & Electromagnets', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Magnetic Effects of Electric Current' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Sources of Energy
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conventional & Non-conventional Sources', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Sources of Energy' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


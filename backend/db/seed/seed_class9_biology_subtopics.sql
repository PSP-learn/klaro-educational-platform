-- =============================================================================
-- seed_class9_biology_subtopics.sql
-- NCERT-style subtopics for Class 9 Biology
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- The Fundamental Unit of Life
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Cell Organelles & Functions', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='The Fundamental Unit of Life' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plasma Membrane, Diffusion & Osmosis', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='The Fundamental Unit of Life' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Tissues
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plant Tissues', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Tissues' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Animal Tissues', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Tissues' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Diversity in Living Organisms
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Classification & Hierarchy', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Diversity in Living Organisms' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plant & Animal Kingdom Overview', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Diversity in Living Organisms' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Why Do We Fall Ill?
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Health, Disease & Prevention', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Why Do We Fall Ill?' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Improvement in Food Resources
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Crop Production & Protection', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Improvement in Food Resources' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


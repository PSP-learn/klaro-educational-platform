-- =============================================================================
-- seed_class10_biology_subtopics.sql
-- NCERT-style subtopics for Class 10 Biology
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Life Processes
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Nutrition & Respiration', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Life Processes' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Transportation & Excretion', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Life Processes' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Control & Coordination
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Nervous System & Reflexes', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Control & Coordination' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Hormonal Control & Tropisms', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Control & Coordination' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- How do Organisms Reproduce?
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Asexual & Sexual Reproduction', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='How do Organisms Reproduce?' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Heredity & Evolution
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Mendelian Genetics & Sex Determination', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Heredity & Evolution' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Our Environment
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ecosystems, Food Chains & Waste', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Our Environment' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Sustainable Management of Natural Resources
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conservation of Forests, Water & Energy', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Sustainable Management of Natural Resources' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


-- =============================================================================
-- seed_class10_chemistry_subtopics.sql
-- NCERT-style subtopics for Class 10 Chemistry
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Chemical Reactions & Equations
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Balancing & Types of Reactions', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Chemical Reactions & Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Oxidation & Reduction', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Chemical Reactions & Equations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Acids, Bases & Salts
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Indicators & pH Scale', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Acids, Bases & Salts' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Strength, Dilution & Neutralization', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Acids, Bases & Salts' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Metals & Non-metals
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Properties & Reactivity Series', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Metals & Non-metals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Extraction, Corrosion & Alloys', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Metals & Non-metals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Carbon and Its Compounds
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Covalent Bonding & Functional Groups', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Carbon and Its Compounds' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Homologous Series, Ethanol & Ethanoic Acid', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Carbon and Its Compounds' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Periodic Classification of Elements
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Mendeleev to Modern Periodic Table', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Periodic Classification of Elements' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Trends: Size, Valency & Reactivity', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 10' and p.subject_id=s.id and p.grade_id=g.id and p.name='Periodic Classification of Elements' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


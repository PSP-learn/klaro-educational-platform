-- =============================================================================
-- seed_class12_biology_subtopics.sql
-- NCERT-style subtopics for Class 12 Biology
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Reproduction =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Reproduction in Organisms', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Reproduction' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Human Reproduction', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Reproduction' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Reproductive Health', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Reproduction' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Genetics & Evolution =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Mendelian Genetics', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Genetics & Evolution' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Molecular Basis of Inheritance', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Genetics & Evolution' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Evolution', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Genetics & Evolution' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Biology and Human Welfare =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Human Health & Diseases', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Biology and Human Welfare' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Food Production Enhancement Strategies', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Biology and Human Welfare' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Microbes in Human Welfare', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Biology and Human Welfare' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Biotechnology =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Principles & Processes', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Biotechnology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Applications', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Biotechnology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'GMOs & Bioethics', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Biotechnology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Ecology & Environment =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Ecosystem', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Ecology & Environment' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Biodiversity & Conservation', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Ecology & Environment' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Environmental Issues', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 12'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Ecology & Environment' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


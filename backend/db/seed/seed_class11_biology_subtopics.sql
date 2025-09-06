-- =============================================================================
-- seed_class11_biology_subtopics.sql
-- NCERT-style subtopics for Class 11 Biology
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Diversity of Living Organisms =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Classification Systems', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Diversity of Living Organisms' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Viruses, Bacteria & Protists', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Diversity of Living Organisms' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plant & Animal Kingdom Overview', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Diversity of Living Organisms' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Structural Organization in Plants and Animals =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plant Tissues & Anatomy', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Structural Organization in Plants and Animals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Morphology of Flowering Plants', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Structural Organization in Plants and Animals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Animal Tissues', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Structural Organization in Plants and Animals' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Cell: Structure and Function =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Cell Organelles & Functions', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Cell: Structure and Function' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Membrane Structure & Transport', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Cell: Structure and Function' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Cell Cycle & Division', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Cell: Structure and Function' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Plant Physiology =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Photosynthesis', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Plant Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Respiration in Plants', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Plant Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Plant Growth & Hormones', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Plant Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Human Physiology =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Digestive System', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Human Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Respiratory System', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Human Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Circulatory System', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Human Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Excretory System', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Human Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Neural & Muscular Coordination', p.id
from subjects s, grades g, topics p
where s.name='Biology' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Human Physiology' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


-- =============================================================================
-- seed_class11_physics_subtopics.sql
-- NCERT-style subtopics for Class 11 Physics
-- Inserts child topics under existing grade-wise chapter parents
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Helper pattern:
-- insert into topics (subject_id, grade_id, name, parent_id)
-- select s.id, g.id, '<SUBTOPIC>', p.id
-- from subjects s, grades g, topics p
-- where s.name='Physics' and g.name='Class 11'
--   and p.subject_id=s.id and p.grade_id=g.id and p.name='<CHAPTER>' and p.parent_id is null
-- on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Units & Measurements =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'SI Units', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Units & Measurements' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Measurement Errors', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Units & Measurements' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Dimensional Analysis', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Units & Measurements' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Kinematics =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Motion in a Straight Line', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Kinematics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Motion in a Plane', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Kinematics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Projectile Motion', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Kinematics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Relative Velocity', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Kinematics' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Laws of Motion =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Newton''s Laws', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Laws of Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Friction', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Laws of Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Uniform Circular Motion', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Laws of Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Work, Energy & Power =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Work-Energy Theorem', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Work, Energy & Power' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Potential & Kinetic Energy', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Work, Energy & Power' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conservation of Energy', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Work, Energy & Power' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Power', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Work, Energy & Power' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Oscillations =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Simple Harmonic Motion', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Oscillations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Damped & Forced Oscillations', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Oscillations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Resonance', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Oscillations' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Waves =========================
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Wave Equation', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Waves' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Superposition Principle', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Waves' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Standing Waves', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Waves' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Beats', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 11'
  and p.subject_id=s.id and p.grade_id=g.id and p.name='Waves' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


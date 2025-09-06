-- =============================================================================
-- seed_class9_physics_subtopics.sql
-- NCERT-style subtopics for Class 9 Physics
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Motion
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Distance, Displacement, Speed & Velocity', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Acceleration & Graphs of Motion', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Force and Laws of Motion
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Balanced/Unbalanced Forces & Inertia', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Force and Laws of Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Newton''s Laws & Momentum', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Force and Laws of Motion' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Gravitation
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Universal Law of Gravitation', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Gravitation' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Free Fall, g & Thrust/Pressure', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Gravitation' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Work and Energy
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Work, Power & Energy Types', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Work and Energy' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Conservation of Energy', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Work and Energy' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Sound
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Nature of Sound & Speed', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Sound' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Echo, Reverberation, Pitch & Loudness', p.id
from subjects s, grades g, topics p
where s.name='Physics' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Sound' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


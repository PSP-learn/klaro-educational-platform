-- =============================================================================
-- seed_class9_chemistry_subtopics.sql
-- NCERT-style subtopics for Class 9 Chemistry
-- Idempotent via ON CONFLICT (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- Matter in Our Surroundings
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'States of Matter & Properties', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Matter in Our Surroundings' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Change of State & Latent Heat', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Matter in Our Surroundings' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Is Matter Around Us Pure
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Mixtures, Solutions & Suspensions', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Is Matter Around Us Pure' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Separation Techniques & Purity', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Is Matter Around Us Pure' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Atoms and Molecules
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Laws of Chemical Combination & Mole', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Atoms and Molecules' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Writing Chemical Formulae', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Atoms and Molecules' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Structure of the Atom
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Subatomic Particles & Models', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Structure of the Atom' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id)
select s.id, g.id, 'Valency, Atomic Number & Isotopes', p.id
from subjects s, grades g, topics p
where s.name='Chemistry' and g.name='Class 9' and p.subject_id=s.id and p.grade_id=g.id and p.name='Structure of the Atom' and p.parent_id is null
on conflict (subject_id, grade_id, name, parent_id) do nothing;


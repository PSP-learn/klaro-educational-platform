-- =============================================================================
-- seed_ncert_topics.sql
-- Seed NCERT-style topics and subtopics into topics table
-- Idempotent: uses ON CONFLICT DO NOTHING on (subject_id, name, parent_id)
-- Requires: subjects table populated with ('Mathematics','Physics','Chemistry','Biology')
-- =============================================================================

-- Mathematics ------------------------------------------------------------------
-- Parents
insert into topics (subject_id, name, parent_id)
select s.id, 'Algebra', null from subjects s where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Calculus', null from subjects s where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Coordinate Geometry', null from subjects s where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Trigonometry', null from subjects s where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Vectors & 3D', null from subjects s where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Statistics & Probability', null from subjects s where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Algebra subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Complex Numbers', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Algebra' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Quadratic Equations', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Algebra' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Sequences & Series', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Algebra' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Matrices', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Algebra' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Determinants', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Algebra' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Calculus subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Limits & Derivatives', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Calculus' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Continuity & Differentiability', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Calculus' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Application of Derivatives', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Calculus' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Integrals', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Calculus' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Differential Equations', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Calculus' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Coordinate Geometry subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Straight Lines', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Coordinate Geometry' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Conic Sections', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Coordinate Geometry' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Trigonometry subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Trigonometric Functions', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Trigonometry' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Inverse Trigonometric Functions', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Trigonometry' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Vectors & 3D subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Vectors', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Vectors & 3D' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Three Dimensional Geometry', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Vectors & 3D' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Statistics & Probability subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Statistics', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Statistics & Probability' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Probability', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Statistics & Probability' and t.parent_id is null
where s.name = 'Mathematics'
on conflict (subject_id, name, parent_id) do nothing;

-- Physics ----------------------------------------------------------------------
-- Parents
insert into topics (subject_id, name, parent_id)
select s.id, 'Mechanics', null from subjects s where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Waves & Oscillations', null from subjects s where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Electrostatics', null from subjects s where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Current & Magnetism', null from subjects s where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Waves & Optics', null from subjects s where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

-- Mechanics subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Units & Measurements', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Mechanics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Kinematics', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Mechanics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Laws of Motion', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Mechanics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Work, Energy & Power', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Mechanics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

-- Waves & Oscillations subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Oscillations', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Waves & Oscillations' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Waves', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Waves & Oscillations' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

-- Electrostatics subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Electric Charges & Fields', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Electrostatics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Electrostatic Potential & Capacitance', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Electrostatics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

-- Current & Magnetism subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Current Electricity', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Current & Magnetism' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Moving Charges & Magnetism', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Current & Magnetism' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

-- Waves & Optics subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Ray Optics', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Waves & Optics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Wave Optics', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Waves & Optics' and t.parent_id is null
where s.name = 'Physics'
on conflict (subject_id, name, parent_id) do nothing;

-- Chemistry --------------------------------------------------------------------
-- Parents
insert into topics (subject_id, name, parent_id)
select s.id, 'Physical Chemistry', null from subjects s where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Organic Chemistry', null from subjects s where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Inorganic Chemistry', null from subjects s where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

-- Physical Chemistry subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Some Basic Concepts', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Atomic Structure', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Thermodynamics', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Equilibrium', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

-- Class 12 additions
insert into topics (subject_id, name, parent_id)
select s.id, 'Solid State', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Solutions', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Electrochemistry', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Chemical Kinetics', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Physical Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

-- Organic Chemistry subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 'Hydrocarbons', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Organic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Isomerism', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Organic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Haloalkanes & Haloarenes', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Organic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Alcohols, Phenols & Ethers', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Organic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Aldehydes, Ketones & Acids', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Organic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

-- Inorganic Chemistry subtopics
insert into topics (subject_id, name, parent_id)
select s.id, 's-Block Elements', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Inorganic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'p-Block Elements', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Inorganic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'd & f Block Elements', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Inorganic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;

insert into topics (subject_id, name, parent_id)
select s.id, 'Coordination Compounds', t.id
from subjects s
join topics t on t.subject_id = s.id and t.name = 'Inorganic Chemistry' and t.parent_id is null
where s.name = 'Chemistry'
on conflict (subject_id, name, parent_id) do nothing;


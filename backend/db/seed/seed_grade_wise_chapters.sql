-- =============================================================================
-- seed_grade_wise_chapters.sql
-- Seed grade-wise NCERT chapter lists (Mathematics, Physics, Chemistry)
-- Chapters are inserted as topics with parent_id = NULL and grade_id set
-- Idempotent via ON CONFLICT on (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Mathematics =========================
-- Class 9
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Number Systems', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Polynomials', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Coordinate Geometry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Linear Equations in Two Variables', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Triangles', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Quadrilaterals', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 9'), 'Statistics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 10
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Real Numbers', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Polynomials', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Pair of Linear Equations in Two Variables', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Quadratic Equations', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Arithmetic Progressions', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Triangles', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Coordinate Geometry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Introduction to Trigonometry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Applications of Trigonometry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Circles', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Statistics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 10'), 'Probability', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 11
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Sets', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Relations & Functions', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Trigonometric Functions', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Complex Numbers and Quadratic Equations', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Permutations and Combinations', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Binomial Theorem', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Sequences and Series', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Straight Lines', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Conic Sections', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Limits & Derivatives', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Statistics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 11'), 'Probability', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 12
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Relations & Functions', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Inverse Trigonometric Functions', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Matrices', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Determinants', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Continuity & Differentiability', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Application of Derivatives', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Integrals', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Differential Equations', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Vector Algebra', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Three Dimensional Geometry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Mathematics'), (select id from grades where name='Class 12'), 'Probability', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Physics =========================
-- Class 11
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 11'), 'Units & Measurements', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 11'), 'Kinematics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 11'), 'Laws of Motion', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 11'), 'Work, Energy & Power', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 11'), 'Oscillations', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 11'), 'Waves', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 12
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 12'), 'Electric Charges & Fields', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 12'), 'Electrostatic Potential & Capacitance', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 12'), 'Current Electricity', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 12'), 'Moving Charges & Magnetism', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 12'), 'Ray Optics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 12'), 'Wave Optics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Chemistry =========================
-- Class 11
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 11'), 'Some Basic Concepts of Chemistry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 11'), 'Structure of Atom', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 11'), 'Thermodynamics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 11'), 'Equilibrium', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 12
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 12'), 'Solid State', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 12'), 'Solutions', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 12'), 'Electrochemistry', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 12'), 'Chemical Kinetics', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Biology =========================
-- Class 11
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 11'), 'Diversity of Living Organisms', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 11'), 'Structural Organization in Plants and Animals', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 11'), 'Cell: Structure and Function', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 11'), 'Plant Physiology', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 11'), 'Human Physiology', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 12
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 12'), 'Reproduction', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 12'), 'Genetics & Evolution', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 12'), 'Biology and Human Welfare', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 12'), 'Biotechnology', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 12'), 'Ecology & Environment', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;


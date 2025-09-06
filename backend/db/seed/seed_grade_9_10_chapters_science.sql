-- =============================================================================
-- seed_grade_9_10_chapters_science.sql
-- Grade-wise NCERT chapters for Physics, Chemistry, Biology (Classes 9 & 10)
-- Chapters are inserted as topics with parent_id = NULL and grade_id set
-- Idempotent via ON CONFLICT on (subject_id, grade_id, name, parent_id)
-- =============================================================================

-- ========================= Physics =========================
-- Class 9
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 9'), 'Motion', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 9'), 'Force and Laws of Motion', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 9'), 'Gravitation', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 9'), 'Work and Energy', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 9'), 'Sound', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 10
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 10'), 'Light - Reflection and Refraction', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 10'), 'The Human Eye and the Colourful World', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 10'), 'Electricity', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 10'), 'Magnetic Effects of Electric Current', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Physics'), (select id from grades where name='Class 10'), 'Sources of Energy', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Chemistry =========================
-- Class 9
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 9'), 'Matter in Our Surroundings', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 9'), 'Is Matter Around Us Pure', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 9'), 'Atoms and Molecules', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 9'), 'Structure of the Atom', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 10
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 10'), 'Chemical Reactions & Equations', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 10'), 'Acids, Bases & Salts', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 10'), 'Metals & Non-metals', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 10'), 'Carbon and Its Compounds', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Chemistry'), (select id from grades where name='Class 10'), 'Periodic Classification of Elements', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- ========================= Biology =========================
-- Class 9
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 9'), 'The Fundamental Unit of Life', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 9'), 'Tissues', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 9'), 'Diversity in Living Organisms', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 9'), 'Why Do We Fall Ill?', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 9'), 'Improvement in Food Resources', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;

-- Class 10
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 10'), 'Life Processes', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 10'), 'Control & Coordination', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 10'), 'How do Organisms Reproduce?', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 10'), 'Heredity & Evolution', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 10'), 'Our Environment', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;
insert into topics (subject_id, grade_id, name, parent_id) values ((select id from subjects where name='Biology'), (select id from grades where name='Class 10'), 'Sustainable Management of Natural Resources', null) on conflict (subject_id, grade_id, name, parent_id) do nothing;


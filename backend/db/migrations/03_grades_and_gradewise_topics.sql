-- =============================================================================
-- 03_grades_and_gradewise_topics.sql
-- Adds grades table and makes topics grade-wise (grade_id on topics)
-- Safe to run after 02_taxonomy_questions.sql
-- =============================================================================

-- Grades table (Class 9 - Class 12)
create table if not exists grades (
  id uuid primary key default gen_random_uuid(),
  name text unique not null,
  created_at timestamptz default now()
);

-- Seed grades
insert into grades (name) values ('Class 9') on conflict (name) do nothing;
insert into grades (name) values ('Class 10') on conflict (name) do nothing;
insert into grades (name) values ('Class 11') on conflict (name) do nothing;
insert into grades (name) values ('Class 12') on conflict (name) do nothing;

-- Add grade_id to topics
alter table topics add column if not exists grade_id uuid references grades(id) on delete set null;
create index if not exists idx_topics_grade on topics(grade_id);

-- Replace old unique constraint with grade-aware one
-- Find existing unique constraint on topics and drop it
DO $$
DECLARE cname text;
BEGIN
  SELECT conname INTO cname
  FROM pg_constraint
  WHERE conrelid = 'public.topics'::regclass AND contype = 'u';
  IF cname IS NOT NULL THEN
    EXECUTE 'ALTER TABLE public.topics DROP CONSTRAINT ' || quote_ident(cname);
  END IF;
END $$;

-- Create new unique constraint including grade_id
alter table topics
  add constraint topics_unique_grade unique (subject_id, grade_id, name, parent_id);

-- NOTE: Going forward, insert topics as grade-wise chapters with parent_id = NULL.
-- =============================================================================
-- END
-- =============================================================================


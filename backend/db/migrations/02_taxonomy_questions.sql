-- =============================================================================
-- 02_taxonomy_questions.sql
-- Taxonomy and Question Bank for Klaro (topics, questions, tags, sources)
-- Safe to run after base schema (supabase_schema_final.sql)
-- =============================================================================

-- Extensions (allowed on Supabase)
create extension if not exists unaccent;
create extension if not exists pg_trgm;
-- Optional semantic search (requires configuration)
-- create extension if not exists vector;

-- ============================================================================
-- Topics: hierarchical taxonomy per subject
-- ============================================================================
create table if not exists topics (
  id uuid primary key default gen_random_uuid(),
  subject_id uuid references subjects(id) on delete cascade,
  name text not null,
  parent_id uuid references topics(id) on delete cascade,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique(subject_id, name, parent_id)
);
create index if not exists idx_topics_subject on topics(subject_id);
create index if not exists idx_topics_parent on topics(parent_id);

-- Keep updated_at fresh
drop trigger if exists update_topics_updated_at on topics;
create trigger update_topics_updated_at before update on topics
for each row execute function update_updated_at_column();

-- ============================================================================
-- Tags: free-form labels
-- ============================================================================
create table if not exists tags (
  id uuid primary key default gen_random_uuid(),
  name text unique not null,
  description text default '',
  created_at timestamptz default now()
);

-- ============================================================================
-- Sources: provenance (book, pyq, mock, reference, other)
-- ============================================================================
create table if not exists sources (
  id uuid primary key default gen_random_uuid(),
  kind text not null check (kind in ('book','pyq','mock','reference','other')),
  name text not null,
  year int,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);
create index if not exists idx_sources_kind on sources(kind);
create index if not exists idx_sources_name on sources(name);

-- ============================================================================
-- Questions: central question bank
-- ============================================================================
create table if not exists questions (
  id uuid primary key default gen_random_uuid(),
  subject_id uuid references subjects(id) on delete set null,
  topic_id uuid references topics(id) on delete set null,
  question_type text not null check (question_type in ('mcq','short','long','numerical','mixed')),
  difficulty text not null check (difficulty in ('easy','medium','hard','mixed')),
  question_text text not null,
  options jsonb,              -- for MCQ, etc.
  answer jsonb,               -- correct answer(s)
  solution text,              -- explanation/steps
  source_id uuid references sources(id) on delete set null,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  tsv tsvector                 -- full-text search vector
);

-- FTS trigger for question_text + solution
create or replace function questions_fts_trigger() returns trigger as $$
begin
  new.tsv := to_tsvector('simple', unaccent(coalesce(new.question_text,''))) ||
             to_tsvector('simple', unaccent(coalesce(new.solution,'')));
  return new;
end;
$$ language plpgsql;

drop trigger if exists trg_questions_fts on questions;
create trigger trg_questions_fts before insert or update on questions
for each row execute function questions_fts_trigger();

-- Indexes for questions
create index if not exists idx_questions_subject on questions(subject_id);
create index if not exists idx_questions_topic on questions(topic_id);
create index if not exists idx_questions_type_difficulty on questions(question_type, difficulty);
create index if not exists idx_questions_created_at on questions(created_at desc);
create index if not exists idx_questions_fts on questions using gin(tsv);

-- Optional embeddings for semantic search (enable vector extension first)
-- alter table questions add column if not exists embedding vector(1536);
-- create index if not exists idx_questions_embedding on questions using ivfflat (embedding vector_ops) with (lists=100);

-- Keep updated_at fresh
drop trigger if exists update_questions_updated_at on questions;
create trigger update_questions_updated_at before update on questions
for each row execute function update_updated_at_column();

-- ============================================================================
-- Question Tags (many-to-many with optional confidence)
-- ============================================================================
create table if not exists question_tags (
  question_id uuid references questions(id) on delete cascade,
  tag_id uuid references tags(id) on delete cascade,
  confidence numeric(5,4) default 1.0,
  primary key (question_id, tag_id)
);

-- ============================================================================
-- Row Level Security (RLS) - read open, writes via service role (bypass RLS)
-- ============================================================================
alter table topics enable row level security;
alter table tags enable row level security;
alter table sources enable row level security;
alter table questions enable row level security;
alter table question_tags enable row level security;

-- Drop existing read policies if they exist (idempotent)
drop policy if exists read_all_topics on topics;
drop policy if exists read_all_tags on tags;
drop policy if exists read_all_sources on sources;
drop policy if exists read_all_questions on questions;
drop policy if exists read_all_question_tags on question_tags;

-- Allow read for all authenticated/anonymous clients
create policy read_all_topics on topics for select using (true);
create policy read_all_tags on tags for select using (true);
create policy read_all_sources on sources for select using (true);
create policy read_all_questions on questions for select using (true);
create policy read_all_question_tags on question_tags for select using (true);

-- No write policies defined here: use service role to bypass RLS for inserts/updates.

-- =============================================================================
-- END
-- =============================================================================


-- Schema for the biotech/regulatory RAG assistant (Supabase / Postgres)
-- Run in the Supabase SQL Editor, in this order.

create extension if not exists vector with schema extensions;

create table public.documents (
  id bigint generated always as identity primary key,
  title text not null,
  source_type text not null,
  source_url text,
  file_name text not null unique,
  total_pages integer,
  created_at timestamptz not null default now()
);

alter table public.documents enable row level security;

create table public.chunks (
  id bigint generated always as identity primary key,
  document_id bigint not null references public.documents (id) on delete cascade,
  chunk_index integer not null,
  page_number integer,
  content text not null,
  metadata jsonb not null default '{}'::jsonb,
  embedding extensions.vector(1536),
  fts tsvector generated always as (to_tsvector('english', content)) stored,
  created_at timestamptz not null default now(),
  unique (document_id, chunk_index)
);

alter table public.chunks enable row level security;

create index chunks_embedding_idx
  on public.chunks
  using hnsw (embedding vector_cosine_ops);

create index chunks_fts_idx
  on public.chunks
  using gin (fts);

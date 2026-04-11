-- Extensions for Vector Search and PostGIS
create extension if not exists vector;
create extension if not exists postgis;

-- Spots Table
create table if not exists public.spots (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  location geography(point) not null,
  address text,
  vibe_embedding vector(1536), -- OpenAI embedding size
  vibe_summary text,           -- AI interpreted "vibe"
  metadata jsonb,              -- Opening hours, price range, etc.
  created_at timestamp with time zone default now()
);

-- Feedback Table for Human-in-the-Loop
create table if not exists public.feedback (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null,
  spot_id uuid references public.spots(id),
  user_rating text check (user_rating in ('good', 'bad')),
  comment text,
  created_at timestamp with time zone default now()
);

-- Index for distance search
create index spots_geo_idx on spots using gist(location);
-- Index for vector similarity
create index spots_embedding_idx on spots using hnsw (vibe_embedding vector_cosine_ops);

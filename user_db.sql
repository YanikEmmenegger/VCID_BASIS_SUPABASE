create table
  public.users (
    id uuid not null,
    name character varying(255) null,
    email character varying(255) null,
    created_at timestamp without time zone null default (now() at time zone 'utc+1'::text),
    constraint users_pkey primary key (id),
    constraint unique_email unique (email),
  ) tablespace pg_default;
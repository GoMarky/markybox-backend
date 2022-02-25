create schema if not exists markybox;
drop schema markybox cascade;
create schema if not exists markybox;


CREATE TABLE if not exists markybox.sessions (
  client_ids    NUMERIC[]   NOT NULL,
  session_id    TEXT        NOT NULL unique,

  created_ts    TIMESTAMPTZ NOT NULL default now(),
);

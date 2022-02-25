create schema if not exists markybox;
drop schema markybox cascade;
create schema if not exists markybox;


CREATE TABLE if not exists markybox.sessions (
  author        string      NOT NULL,
  session_id    TEXT        NOT NULL unique,
  data          TEXT

  created_ts    TIMESTAMPTZ NOT NULL default now(),
);

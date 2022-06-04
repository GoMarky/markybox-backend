create schema if not exists markybox;
drop schema markybox cascade;
create schema if not exists markybox;

CREATE EXTENSION IF NOT EXISTS"uuid-ossp";
SELECT uuid_generate_v4();

CREATE TABLE if not exists markybox.users(
  user_id        SERIAL       PRIMARY KEY NOT NULL unique,
  user_name      TEXT         NOT NULL,
  email          TEXT         NOT NULL unique,
  password       TEXT         NOT NULL,
  current_theme  TEXT         NOT NULL DEFAULT 'dark' CHECK ((current_theme ='dark') OR (current_theme='light')),
  preferred_lang TEXT         NOT NULL DEFAULT 'plain' CHECK ((preferred_lang ='cpp') OR (preferred_lang ='python') OR (preferred_lang ='js') OR (preferred_lang ='json') OR (preferred_lang ='plain') OR (preferred_lang ='golang')),
  created_at     TIMESTAMP    without time zone default now()
);

CREATE TABLE if not exists markybox.notes(
  note_id      uuid         default uuid_generate_v4 (),
  note_title   TEXT         default 'Unnamed',
  note_data    TEXT         NOT NULL,
  note_lang    TEXT         NOT NULL DEFAULT 'plain' CHECK CHECK ((note_lang ='cpp') OR (note_lang ='python') OR (note_lang ='js') OR (note_lang ='json') OR (note_lang ='plain') OR (preferred_lang ='golang')),
  user_id      INTEGER      REFERENCES markybox.users(user_id) ON DELETE CASCADE,
  created_at   TIMESTAMP    default CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP    default CURRENT_TIMESTAMP
);


CREATE TABLE if not exists markybox.sessions (
  session_id   uuid        default uuid_generate_v4(),
  user_id      INTEGER     REFERENCES markybox.users(user_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS '
  BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
  END;
'LANGUAGE 'plpgsql';

CREATE TRIGGER update_updated_at_modtime BEFORE UPDATE
  ON markybox.notes FOR EACH ROW EXECUTE PROCEDURE
  update_updated_at_column();


drop schema markybox cascade;
create schema if not exists markybox;

--Создание таблицы users возможностью добавлять несколько заметок для одного пользователя
CREATE TABLE users(
user_id SERIAL PRIMARY KEY NOT NULL unique,
user_name TEXT NOT NULL,
email TEXT NOT NULL unique,
age INTEGER,
created_at TIMESTAMP without time zone default now(),
password TEXT
);

--Добавление записей в таблицу users
INSERT INTO users (name,email,age,password) 
VALUES ('Tanya','tanman@gmail.com',26,'654321');

--Создание таблицы "notes"
CREATE TABLE notes(
user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
note_id uuid default uuid_generate_v4 (),
title TEXT default 'Unnamed',
note_data TEXT NOT NULL,
created_at TIMESTAMP default CURRENT_TIMESTAMP,
updated_at TIMESTAMP default CURRENT_TIMESTAMP
CONSTRAINT user_notes unique(user_id, id)
);

--Добавление записи в notes с указанным user_id
insert into notes (user_id, title, note_data)
values (1,'RusHello','privetik');

--Создание таблицы "session"
CREATE TABLE session (
session_id uuid default uuid_generate_v4 (),
user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE);

--Добавление user_id в таблицу session и возврат session_id
INSERT INTO session (user_id)
VALUES (1) RETURNING session_id;



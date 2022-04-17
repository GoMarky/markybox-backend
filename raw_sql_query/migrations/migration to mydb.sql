
drop schema mydb cascade;
create schema if not exists mydb;

--Создание таблицы users возможностью добавлять несколько заметок для одного пользователя
CREATE TABLE mydb.mydb.users(
user_id SERIAL PRIMARY KEY NOT NULL unique,
user_name TEXT NOT NULL,
email TEXT NOT NULL unique,
age INTEGER,
created_at TIMESTAMP without time zone default now(),
password TEXT
);

--Добавление записей в таблицу users
INSERT INTO mydb.mydb.users (user_name,email,age,password) 
VALUES ('Tanya','tanman@gmail.com',26,'654321');

CREATE EXTENSION IF NOT EXISTS"uuid-ossp";

--Создание таблицы "notes"
CREATE TABLE notes(
user_id INTEGER REFERENCES mydb.mydb.users(user_id) ON DELETE CASCADE,
note_id uuid default uuid_generate_v4 (),
title TEXT default 'Unnamed',
note_data TEXT NOT NULL,
created_at TIMESTAMP default CURRENT_TIMESTAMP,
updated_at TIMESTAMP default CURRENT_TIMESTAMP
);

--Добавление записи в notes с указанным user_id
insert into mydb.mydb.notes (user_id, title, note_data)
values (2,'RusHello','privetik');

--Создание таблицы "session"
CREATE TABLE mydb.mydb.session (
session_id uuid default uuid_generate_v4 (),
user_id INTEGER REFERENCES mydb.mydb.users(user_id) ON DELETE CASCADE);

--Добавление user_id в таблицу session и возврат session_id
INSERT INTO mydb.mydb.session (user_id)
VALUES (2) RETURNING session_id;



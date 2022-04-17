--Создание таблицы users возможностью добавлять несколько заметок для одного пользователя
CREATE TABLE users(
id SERIAL PRIMARY KEY NOT NULL unique,
name TEXT NOT NULL,
email TEXT NOT NULL unique,
age INTEGER,
created_at TIMESTAMP without time zone default now()
);

--Добавление записей в таблицу users
INSERT INTO users (name,email,age) 
VALUES ('Tanya','tanman@gmail.com',26),
 ('Andrew','and@gmail.com',27),
 ('Ivan','iva@gmail.com',29);
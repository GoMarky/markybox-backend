--Создание таблицы "session"
CREATE TABLE session (
session_id uuid default uuid_generate_v4 (),
user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE);

--Добавление user_id в таблицу session и возврат session_id
INSERT INTO session (user_id)
VALUES (1) RETURNING session_id;

--Выбрать session_id по user_id
select session_id from session
where user_id=1;

--Удаление строки в session по session_id
DELETE FROM session
WHERE session_id = 'f97d4343-e634-41f4-a639-c5ded11e1cb9';
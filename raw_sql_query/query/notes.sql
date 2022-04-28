--Создание таблицы "notes"
CREATE TABLE notes(
id SERIAL NOT NULL unique,
data TEXT NOT NULL,
user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
created_at TIMESTAMP without time zone default now(),
CONSTRAINT user_notes unique(user_id, id)
);

 --Добавление колонки  updated_at в существующую таблицу notes
alter table notes add column updated_at timestamp;

--Добавление записи в notes с указанным user_id
insert into notes (user_id, title, note_data)
values (3,'','privetik') RETURNING note_id;

--Удаление записи из notes по указанному note_id
delete from notes
where note_id='b47e7501-25fc-483a-92f9-dd59881f5790';

--Обновление записи notes по указанному note_id и обновить updated_at (пока работает только обновление записи, updated_at не меняется)
UPDATE notes 
	SET note_data = 'privetik' 
	WHERE note_id = 'cd7e9be4-573f-40e2-a333-249f060d1e7d'; 

--Получение одной записи по ноут_айди 
SELECT note_id, note_data from notes
WHERE note_id='2b9def28-c6db-4f51-9203-3d4b6fdc087c';
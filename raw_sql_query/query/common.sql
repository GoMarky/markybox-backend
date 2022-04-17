
--Получение информации о пользователе (инфа о профиле + записей в массиве) по user_id из таблицы users и notes
select users.user_id, user_name, email, array_agg(ARRAY[note_id::text, notes.title, notes.note_data,notes.created_at::text,notes.updated_at::text]) AS user_notes
from users, notes 
where users.user_id=notes.user_id AND users.email='tanman@gmail.com' AND users.password='654321'
group by users.email, users.user_name, users.user_id;






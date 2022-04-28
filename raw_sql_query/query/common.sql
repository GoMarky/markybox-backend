
--Получение информации о пользователе (инфа о профиле + записей в массиве) по user_id из таблицы users и notes
select users.user_id, user_name, email, array_agg(ARRAY[note_id::text, notes.title, notes.note_data,notes.created_at::text,notes.updated_at::text]) AS user_notes
from users, notes 
where users.user_id=notes.user_id AND users.email='tanman@gmail.com' AND users.password='654321'
group by users.email, users.user_name, users.user_id;




--Добавить при возвращение записей сортировку по дате создания в этом запросе:
SELECT session_id, user_name, email,
                        array_agg(ARRAY[notes.note_id::text, notes.title, notes.note_data,notes.created_at::text,notes.updated_at::text] ORDER BY notes.updated_at DESC) AS user_notes
                        FROM session, users, notes 
                        WHERE users.user_id=session.user_id AND users.user_id=notes.user_id AND session_id='bba998e2-3b43-4cdd-80bd-a8d7eaf4fa8f'
                        GROUP BY session.session_id, users.email, users.user_name;




SELECT session_id, users.user_id, user_name, email
                        FROM session LEFT JOIN users ON session.user_id=users.user_id
                        WHERE session_id='b94cdc7d-12e2-4aa1-93cc-54ae6738c850';


SELECT notes.user_id, notes.note_id, notes.title, notes.note_data, notes.created_at, notes.updated_at
                        FROM notes
                        WHERE notes.user_id='3' 
                        ORDER BY notes.updated_at DESC;
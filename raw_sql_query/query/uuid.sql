
--Подключение библиотеки uuid-ossp 
CREATE EXTENSION IF NOT EXISTS"uuid-ossp";
--Сгенерировать случайное (не использует данные пользователя) uuid 
SELECT uuid_generate_v4();











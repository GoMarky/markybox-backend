
b94cdc7d-12e2-4aa1-93cc-54ae6738c850


SELECT session_id, user_name, email,
                        array_agg(ARRAY['Note_Id:', notes.note_id::text, 
										'Title', notes.title, 
										'Note_Data', notes.note_data,
										notes.created_at::text,
										notes.updated_at::text] ORDER BY notes.updated_at DESC) AS user_notes
                        FROM session, users, notes 
                        WHERE users.user_id=session.user_id AND users.user_id=notes.user_id AND session_id='b94cdc7d-12e2-4aa1-93cc-54ae6738c850'
                        GROUP BY session.session_id, users.email, users.user_name;


ALTER TABLE table-name
  RENAME COLUMN old-name TO new-name;
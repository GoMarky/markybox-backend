from app.code.note.handlers.v1.create_note_handler import CreateNoteHandler
from app.code.note.handlers.v1.delete_note_handler import DeleteNoteHandler
from app.code.note.handlers.v1.update_note_handler import UpdateNoteHandler

__all__ = ['note_routes']

note_routes = [CreateNoteHandler, UpdateNoteHandler, DeleteNoteHandler]

for route in note_routes:
    route.path = '/v1' + route.path

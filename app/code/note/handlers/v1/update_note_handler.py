from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from jsonschema import validate, ValidationError
from app.code.note.validation.note_schemas import UPDATE_NOTE_SCHEMA
from app.code.note.note_service import NoteService


class UpdateNoteHandler(RouteHandler):
    path = '/note/update/'

    def __init__(self, log_service: LogService, router_service: RouterService, note_service: NoteService):
        super().__init__(log_service)

        self.path = UpdateNoteHandler.path
        self.request_type = hdrs.METH_PATCH

        self.router_service = router_service
        self.note_service = note_service

        self.name = 'client.note.update'

    async def handler(self, request: web.Request) -> web.Response:
        body = await request.json()

        try:
            validate(body, UPDATE_NOTE_SCHEMA)

            return await self.do_handle(body)
        except ValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict) -> web.Response:
        note_id: str = body.get('noteId')
        note_data: str = body.get('data')
        session_id: str = body.get('sessionId')
        note_lang: str = body.get('lang')

        note_result = await self.note_service.update_note(session_id, note_id, note_data, note_lang)

        return self.router_service.send_success_response(self.name, note_result)

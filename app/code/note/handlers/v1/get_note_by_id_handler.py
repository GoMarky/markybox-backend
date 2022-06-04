from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from app.code.note.note_service import NoteService
from jsonschema import validate, ValidationError
from app.code.note.validation.note_schemas import GET_NOTE_SCHEMA


class GetNoteByIdHandler(RouteHandler):
    path = '/note/getById/'

    def __init__(self, log_service: LogService, router_service: RouterService, note_service: NoteService):
        super().__init__(log_service)

        self.path = GetNoteByIdHandler.path
        self.request_type = hdrs.METH_POST

        self.router_service = router_service
        self.note_service = note_service

        self.name = 'client.note.getById'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            body = await request.json()

            validate(body, GET_NOTE_SCHEMA)

            return await self.do_handle(body)
        except ValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)
        except Exception as error:
            return self.router_service.send_unexpected_error_response(self.name, error.__str__())

    async def do_handle(self, body: dict) -> web.Response:
        session_id = body.get('sessionId')
        note_id = body.get('noteId')

        result = await self.note_service.get_note_by_id(session_id, note_id)

        if result is None:
            return self.router_service.send_not_found_response(self.name, 'Note not found')

        return self.router_service.send_success_response(self.name, {'note': result})

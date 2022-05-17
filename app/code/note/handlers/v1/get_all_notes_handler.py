from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from app.code.note.note_service import NoteService
from jsonschema import validate, ValidationError
from app.code.note.validation.note_schemas import GET_ALL_NOTES_SCHEMA


class GetAllNotesHandler(RouteHandler):
    path = '/note/get-all/'

    def __init__(self, log_service: LogService, router_service: RouterService, note_service: NoteService):
        super().__init__(log_service)

        self.path = GetAllNotesHandler.path
        self.request_type = hdrs.METH_POST

        self.router_service = router_service
        self.note_service = note_service

        self.name = 'client.note.getAll'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            body = await request.json()

            validate(body, GET_ALL_NOTES_SCHEMA)

            return await self.do_handle(body)
        except ValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict) -> web.Response:
        session_id = body.get('sessionId')

        result = await self.note_service.get_notes_by_session_id(session_id)

        if result is None:
            return self.router_service.send_not_found_response(self.name, 'Notes not found')

        return self.router_service.send_success_response(self.name, {'notes': result})

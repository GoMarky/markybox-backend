from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from app.code.note.note_service import NoteService
from app.code.note.validation.note_schemas import CREATE_NOTE_SCHEMA
from jsonschema import validate, ValidationError


class CreateNoteHandler(RouteHandler):
    path = '/note/create/'

    def __init__(self, log_service: LogService, router_service: RouterService, note_service: NoteService):
        super().__init__(log_service)

        self.path = CreateNoteHandler.path
        self.request_type = hdrs.METH_POST

        self.router_service = router_service
        self.note_service = note_service

        self.name = 'client.note.create'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            body = await request.json()

            print(body)

            validate({"sessionId": body.get('sessionId')}, CREATE_NOTE_SCHEMA)

            return await self.do_handle(request, body)
        except ValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, request: web.Request, body: dict) -> web.Response:
        result = await self.note_service.create_note(request, body)

        return self.router_service.send_success_response(self.name, result)

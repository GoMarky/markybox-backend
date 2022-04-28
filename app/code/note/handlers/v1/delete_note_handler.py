from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService
from app.code.note.validation.note_schemas import DELETE_NOTE_SCHEMA
from jsonschema import validate
from app.code.note.note_service import NoteService
from app.base.errors import DBRecordNotFoundError


class DeleteNoteHandler(RouteHandler):
    path = '/note/delete/'

    def __init__(self, log_service: LogService, router_service: RouterService, note_service: NoteService):
        super().__init__(log_service)

        self.path = DeleteNoteHandler.path
        self.request_type = hdrs.METH_POST

        self.router_service = router_service
        self.note_service = note_service

        self.name = 'client.note.delete'

    async def handler(self, request: web.Request) -> web.Response:
        body = await request.json()

        try:
            validate(body, DELETE_NOTE_SCHEMA)

            return await self.do_handle(body)
        except DBRecordNotFoundError as error:
            return self.router_service.send_unexpected_error_response(self.name, error.message)

    async def do_handle(self, body: dict) -> web.Response:
        session_id = body.get('sessionId')
        note_id = body.get('noteId')

        await self.note_service.delete_note(session_id, note_id)

        return self.router_service.send_success_response(self.name, 'deleted')

from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.code.note.note_service import NoteService
from app.platform.router.router_service import RouterService
from app.base.errors import DBRecordNotFoundError
from app.code.session.validation.session import SETTINGS_USER_APPLY_SCHEMA
from jsonschema import validate


class NoteSettingsApplyHandler(RouteHandler):
    path = '/note/settings/apply/'

    def __init__(self, log_service: LogService, note_service: NoteService, router_service: RouterService):
        super().__init__(log_service)

        self.path = NoteSettingsApplyHandler.path
        self.request_type = hdrs.METH_POST

        self.note_service = note_service
        self.router_service = router_service

        self.name = 'client.note.settings.apply'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            body: dict = await request.json()

            validate(body, SETTINGS_USER_APPLY_SCHEMA)

            return await self.do_handle(body)
        except DBRecordNotFoundError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict) -> web.Response:
        try:
            session_id = body.pop('sessionId')

            result = await self.note_service.apply_settings(session_id, body)

            return self.router_service.send_success_response(self.name, result)
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)
        except Exception as error:
            return self.router_service.send_unexpected_error_response(self.name, error.__str__())

from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.router_service import RouterService


class DeleteNoteHandler(RouteHandler):
    path = '/note/delete/'

    def __init__(self, log_service: LogService, router_service: RouterService):
        super().__init__(log_service)

        self.path = DeleteNoteHandler.path
        self.request_type = hdrs.METH_DELETE

        self.router_service = router_service

        self.name = 'client.note.delete'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            return await self.do_handle(request)
        except RuntimeError as error:
            return self.router_service.send_unexpected_error_response(self.name, "")

    async def do_handle(self, request: web.Request) -> web.Response:
        return self.router_service.send_success_response(self.name, 'delete')

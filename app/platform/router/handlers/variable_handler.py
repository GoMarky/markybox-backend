from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_not_found_response


class VariableRouteHandler(RouteHandler):
    path = '/{name}'

    def __init__(self, log_service: LogService):
        super().__init__(log_service)

        self.path = VariableRouteHandler.path
        self.request_type = hdrs.METH_GET

        self.name = 'common.variable'

    async def handler(self, request: web.Request) -> web.Response:
        result = f"Path: '{request.match_info['name']}' does't available"

        return send_not_found_response(self.name, result)

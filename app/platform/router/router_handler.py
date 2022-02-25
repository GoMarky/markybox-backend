from app.platform.instantiation.disposable import Disposable
from app.platform.log.log_service import LogService
from aiohttp import web


class RouteHandler(Disposable):
    def __init__(self, log_service: LogService):
        self.log_service = log_service

        self.path = ''
        self.request_type = ''
        self.name = ''

    def handler(self, request: web.Request) -> web.Response:
        pass

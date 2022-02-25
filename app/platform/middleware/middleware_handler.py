from ..instantiation.disposable import Disposable
from aiohttp import web


class MiddlewareHandler(Disposable):
    def __init__(self):
        pass

    def call(self, request_name: str, request: web.Request, handler):
        pass

from app.platform.instantiation.disposable import Disposable
from app.platform.instantiation.instantiation_service import InstantiationService

from app.platform.log.log_service import LogService
from app.platform.lifecycle.lifecycle_service import LifecycleService

from .common import send_not_found_response, send_unexpected_error_response, send_bad_request_response, \
    send_success_response


class RouterService(Disposable):
    def __init__(self, log_service: LogService,
                 lifecycle_service: LifecycleService,
                 instantiation_service: InstantiationService):
        self.log_service = log_service
        self.lifecycle_service = lifecycle_service
        self.instantiation_service = instantiation_service

        self.routes = []

    def add_route_handler(self, route_handler):
        route_instance = self.instantiation_service.create_instance(route_handler)

        self.routes.append(route_instance)

    def send_success_response(self, request_name: str, result):
        return send_success_response(request_name, result)

    def send_not_found_response(self, request_name: str, error_message: str):
        return send_not_found_response(request_name, error_message)

    def send_unexpected_error_response(self, request_name: str, additional_text: str = ''):
        return send_unexpected_error_response(request_name, additional_text)

    def send_bad_request_response(self, request_name: str, error_message: str):
        return send_bad_request_response(request_name, error_message)

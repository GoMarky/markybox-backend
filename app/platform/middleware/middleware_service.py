from ..instantiation.disposable import Disposable
from ..instantiation.instantiation_service import InstantiationService
from ..lifecycle.lifecycle_service import LifecycleService
from ..middleware.middleware_handler import MiddlewareHandler


class MiddlewareService(Disposable):
    def __init__(self, lifecycle_service: LifecycleService, instantiation_service: InstantiationService):
        self.lifecycle_service = lifecycle_service
        self.instantiation_service = instantiation_service
        self.middlewares = []

    def register_middleware(self, middleware) -> MiddlewareHandler:
        instance = self.instantiation_service.create_instance(middleware)

        self.middlewares.append(instance)

        return instance

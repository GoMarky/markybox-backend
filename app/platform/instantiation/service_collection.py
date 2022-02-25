from app.platform.instantiation.disposable import Disposable

__all__ = ['ServiceCollection']


class ServiceCollection(Disposable):
    def __init__(self, strict=False):
        self.strict = strict

        self.services = {}

    def set(self, identifier: str, service):
        self.services[identifier] = service

    def get(self, identifier: str):
        return self.services.get(identifier)

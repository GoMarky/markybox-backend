from app.platform.instantiation.disposable import Disposable


class DatabaseService(Disposable):
    def __init__(self):
        pass

    @property
    def instance(self):
        return self.__app['db']

    def init(self, app):
        self.__app = app

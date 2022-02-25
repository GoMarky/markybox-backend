from app.platform.instantiation.disposable import Disposable
from enum import Enum

__all__ = ['LogLevel', 'LogService']


class LogLevel(Enum):
    Off = 0,
    Info = 1,
    Debug = 2,
    Warning = 3,
    Error = 4,
    Critical = 5


class LogService(Disposable):
    def __init__(self, log_level: LogLevel):
        self.log_level = log_level.value[0]

    def info(self, message):
        if self.log_level >= LogLevel.Info.value[0]:
            print('[INFO] ' + message)

    def debug(self, message):
        if self.log_level >= LogLevel.Debug.value[0]:
            print('[DEBUG] ' + message)

    def warn(self, message):
        if self.log_level >= LogLevel.Warning.value[0]:
            print('[WARN] ' + message)

    def error(self, message):
        if self.log_level >= LogLevel.Error.value[0]:
            print('[ERROR] ' + message)

    def critical(self, message):
        if self.log_level >= LogLevel.Critical.value[0]:
            print('[CRITICAL] ' + message)

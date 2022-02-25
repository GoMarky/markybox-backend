from enum import Enum


class ApplicationError(Exception):
    def __init__(self, message: str):
        self.message = message

        super().__init__(self.message)


class NetworkError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class ValidationError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class AuthErrorCode(Enum):
    InvalidPassword = 1,
    UserDisabled = 2,


class AuthenticatedError(ApplicationError):
    def __init__(self, message: str, error_type: AuthErrorCode):
        super().__init__(message)

        self.type = error_type


class DatabaseError(ApplicationError):
    pass


class DBRecordNotFoundError(DatabaseError):
    pass

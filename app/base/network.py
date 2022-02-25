from enum import Enum


class HTTPStatusCode(Enum):
    OK = 200,
    Created = 201,
    BAD_REQUEST = 400,
    NOT_FOUND = 404,
    INTERNAL_SERVER_ERROR = 500

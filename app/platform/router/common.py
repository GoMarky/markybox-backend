from enum import Enum
from aiohttp import web
from app.base.network import HTTPStatusCode


class APIErrorCode(Enum):
    BadRequest = 1,
    NotFoundError = 2,
    UnexpectedError = 25


def send_success_response(request_name: str, result) -> web.Response:
    return web.json_response({
        'request': request_name,
        'result': result
    }, status=HTTPStatusCode.OK.value[0])


def send_not_found_response(request_name: str, error_message: str = 'Not found') -> web.Response:
    return web.json_response({
        'request': request_name,
        'code': APIErrorCode.NotFoundError.value[0],
        'message': error_message
    }, status=HTTPStatusCode.NOT_FOUND.value[0])


def send_bad_request_response(request_name: str, error_message: str = 'Bad request') -> web.Response:
    return web.json_response({
        'request': request_name,
        'code': APIErrorCode.BadRequest.value[0],
        'message': error_message
    }, status=HTTPStatusCode.BAD_REQUEST.value[0])


def send_unexpected_error_response(request_name: str, additional_text: str = '') -> web.Response:
    return web.json_response({
        'request': request_name,
        'code': 25,
        'message': 'Unexpected error. ' + additional_text
    }, status=500)

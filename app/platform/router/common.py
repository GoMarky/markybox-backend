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
        'errorCode': 2,
        'errorMessage': error_message
    }, status=HTTPStatusCode.OK.value[0])


def send_bad_request_response(request_name: str, error_message: str = 'Bad request') -> web.Response:
    return web.json_response({
        'request': request_name,
        'errorCode': 1,
        'errorMessage': error_message
    })


def send_unexpected_error_response(request_name: str, additional_text: str = '') -> web.Response:
    return web.json_response({
        'request': request_name,
        'errorCode': 25,
        'errorMessage': 'Unexpected error. ' + additional_text
    }, status=HTTPStatusCode.OK.value[0])

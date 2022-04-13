from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_unexpected_error_response, send_not_found_response

from app.db import users
from app.code.session.session_service import SessionService
from app.platform.router.router_service import RouterService


class SessionInfoHandler(RouteHandler):
    path = '/session/info/'

    def __init__(self, log_service: LogService, session_service: SessionService, router_service: RouterService):
        super().__init__(log_service)

        self.path = SessionInfoHandler.path
        self.request_type = hdrs.METH_POST

        self.session_service = session_service
        self.router_service = router_service

        self.name = 'client.session.info'

    async def handler(self, request: web.Request) -> web.Response:
        try:
            body: dict = await request.json()
            session_id = body.get('sessionId')

            return await self.do_handle(request, session_id)
        except RuntimeError as error:
            return self.router_service.send_unexpected_error_response(self.name, "")

    async def do_handle(self, request, session_id) -> web.Response:
        async with request.app['db'].acquire() as connection:
            sql: str = '''
            select session_id, user, email, 
            array_agg(ARRAY[notes.title, notes.notes,notes.created_at::text,notes.updated_at::text]) AS user_notes
            from session, users, notes 
            where users.user_id=session.user_id AND users.user_id=notes.user_id AND session_id='{session_id}'
            group by session.session_id, users.email;
            '''.format(session_id=session_id)

            result = await connection.execute(sql)

            if result.rowcount == 0:
                return self.router_service.send_not_found_response(self.name, "")

            arr = [dict(row) for row in result]
            user_notes = []
            body: dict = arr.pop()
            raw_notes = body.get('user_notes')

            print(body)

            for note in raw_notes:
                user_note = dict()

                title = note[0]
                data = note[1]
                created_at = note[2]
                updated_at = note[3]

                user_note['title'] = title
                user_note['data'] = data
                user_note['createdAt'] = created_at
                user_note['updatedAt'] = updated_at

                user_notes.append(user_note)

            body['notes'] = user_notes
            body.pop('user_notes')

            return self.router_service.send_success_response(self.name, body)

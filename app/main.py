from app.platform.instantiation.service_collection import ServiceCollection
from app.platform.instantiation.instantiation_service import InstantiationService

from app.platform.log.log_service import LogService, LogLevel
from app.platform.lifecycle.lifecycle_service import LifecycleService

from app.platform.router.router_service import RouterService
from app.platform.middleware.middleware_service import MiddlewareService

from app.code.session.session_service import SessionService
from app.platform.database.database_service import DatabaseService

from app.code.socket.socket_service import SocketService
from app.code.note.note_service import NoteService

__all__ = ['instantiation_service']

# Создаем коллекцию сервисов
services = ServiceCollection()

# Создаем основной инстанцирующий сервис
instantiation_service = InstantiationService(services)

# log service
log_service = LogService(LogLevel.Info)
services.set('log_service', log_service)

# lifecycle service
lifecycle_service = LifecycleService()
services.set('lifecycle_service', lifecycle_service)

# router service
router_service = RouterService(log_service, lifecycle_service, instantiation_service)
services.set('router_service', router_service)

# middleware service
middleware_service = MiddlewareService(lifecycle_service, instantiation_service)
services.set('middleware_service', middleware_service)

# database service
database_service = DatabaseService()
services.set('database_service', database_service)

# session service
session_service = SessionService(database_service, router_service)
services.set('session_service', session_service)

socket_service = SocketService(database_service)
services.set('socket_service', socket_service)

note_service = NoteService(database_service, session_service)
services.set('note_service', note_service)

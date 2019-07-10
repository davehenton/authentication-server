import http

import pyramid.authentication as auth
import pyramid.exceptions
import pyramid.config as pyconfig
import sqlalchemy
from pyramid.authorization import ACLAuthorizationPolicy

import user_management.config.auth as authconf
import user_management.models as models
from user_management.libs import Log
from user_management.views import health


def not_found(request):
    request.response.status_code = http.HTTPStatus.NOT_FOUND
    request.response.content_type = 'application/json'
    request.response.json = {
        'status': http.HTTPStatus.NOT_FOUND,
        'msg': 'Not Found',
    }
    return request.response


def forbidden(request):
    request.response.status_code = http.HTTPStatus.UNAUTHORIZED
    request.response.content_type = 'application/json'
    request.response.json = {
        'status': http.HTTPStatus.UNAUTHORIZED,
        'msg': http.HTTPStatus.UNAUTHORIZED.name.capitalize(),
    }
    return request.response


class Route:
    @staticmethod
    def load(**settings):
        with pyconfig.Configurator(settings=settings) as config:
            # Pyramid includes
            config.include(health)

            # Pyramid scan
            config.scan('user_management.models')
            config.scan('user_management.views')

            # Database setup
            engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
            models.initialize_sql(engine)

            # User management routes
            config.add_route('check_user', '/user/check')
            config.add_route('insert_user', '/user/insert')
            config.add_route('list_user', '/user/list')

            # Authentication configuration
            authentication = auth.BasicAuthAuthenticationPolicy(check=authconf.authenticate, debug=True)
            config.set_authentication_policy(authentication)
            config.set_authorization_policy(ACLAuthorizationPolicy())
            config.set_root_factory(lambda request: authconf.Context(request))

            config.add_notfound_view(not_found, append_slash=True)
            try:
                health.db_health_check()
            except Exception as e:
                Log.error(e)
                raise pyramid.exceptions.ConfigurationError(e)
            return config.make_wsgi_app()

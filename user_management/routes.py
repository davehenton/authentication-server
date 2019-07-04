import http
import json

import pyramid.authentication as auth
import pyramid.config as pyconfig
import sqlalchemy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, NO_PERMISSION_REQUIRED

import user_management.libs.constants as constants
import user_management.models as models
from user_management.libs import user
from user_management.views.user import User


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


def authenticate(client, secret, request):
    u = user.User.by_client_and_secret(client, secret)
    if u is not None:
        request.context.user = u
        return []
    return None


class Context:
    def __init__(self, request):
        self.user = None

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )


class Route:
    @staticmethod
    def load(**settings):
        with pyconfig.Configurator(settings=settings) as config:
            config.scan('user_management.models')
            config.scan('user_management.views')

            # Database setup
            engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
            models.initialize_sql(engine)

            # User management routes
            config.add_route('check_user', '/user/check')
            config.add_route('insert_user', '/user/insert')

            # User management views
            config.add_view(User.check_user, route_name='check_user', request_method=constants.GET,
                            renderer='json', permission=Authenticated)
            config.add_view(User.insert_user, route_name='insert_user', request_method=constants.POST,
                            renderer='json', permission=NO_PERMISSION_REQUIRED)

            # Authentication configuration
            authentication = auth.BasicAuthAuthenticationPolicy(check=authenticate, debug=True)
            config.set_authentication_policy(authentication)
            config.set_authorization_policy(ACLAuthorizationPolicy())
            config.set_root_factory(lambda request: Context(request))

            config.add_notfound_view(not_found, append_slash=True)
            return config.make_wsgi_app()

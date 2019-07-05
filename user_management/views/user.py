import http

from pyramid.security import Authenticated, NO_PERMISSION_REQUIRED
from pyramid.view import view_config

import user_management.libs.exceptions as e
import user_management.libs.user as user
from user_management.libs import constants


class User:

    def __init__(self, request) -> None:
        self.request = request

    @e.exc_handler
    @view_config(route_name='check_user', request_method=constants.GET, renderer='json', permission=Authenticated)
    def check_user(self):
        u = self.request.context.user
        self.request.response.status_code = http.HTTPStatus.OK
        self.request.response.content_type = 'application/json'
        self.request.response.json = {
            'check_user': http.HTTPStatus.OK.value,
            'user': u,
        }
        return self.request.response

    @e.exc_handler
    @view_config(route_name='insert_user', request_method=constants.POST,
                            renderer='json', permission=NO_PERMISSION_REQUIRED)
    def insert_user(self):
        u = user.User.create(client=self.request.params.get('client'), secret=self.request.params.get('secret'), to_dict=True)
        self.request.response.status_code = http.HTTPStatus.OK
        self.request.response.content_type = 'application/json'
        self.request.response.json = {
            'check_user': http.HTTPStatus.OK.value,
            'user': u,
        }
        return self.request.response

    @e.exc_handler
    @view_config(route_name='list_user', request_method=constants.GET,
                            renderer='json', permission=Authenticated)
    def list_user(self):
        u = user.User.all(to_dict=True)
        self.request.response.status_code = http.HTTPStatus.OK
        self.request.response.content_type = 'application/json'
        self.request.response.json = {
            'check_user': http.HTTPStatus.OK.value,
            'users': u,
        }
        return self.request.response

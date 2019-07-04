import http

import user_management.libs.exceptions as e
import user_management.libs.user as user


class User:

    def __init__(self, request) -> None:
        self.request = request

    @e.exc_handler
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
    def insert_user(self):
        u = user.User.create(client=self.request.params.get('client'), secret=self.request.params.get('secret'))
        self.request.response.status_code = http.HTTPStatus.OK
        self.request.response.content_type = 'application/json'
        self.request.response.json = {
            'check_user': http.HTTPStatus.OK.value,
            'user': u,
        }
        return self.request.response

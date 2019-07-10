from enum import Enum

class HTTPRequest(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    def __str__(self):
        return str(self.value)


GET = HTTPRequest.GET.value
POST = HTTPRequest.POST.value
PUT = HTTPRequest.PUT.value
DELETE = HTTPRequest.DELETE.value

USER_MANAGEMENT = 'user_management'

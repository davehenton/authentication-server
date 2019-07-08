import hashlib

import pyramid

from user_management.libs import user
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS


def authenticate(client, secret, request):
    u = user.User.by_client_and_secret(client, secret, to_dict=True)
    if u is not None:
        request.context.user = u
        a = list()
        a.sort()
        return []
    else:
        sysuser = pyramid.threadlocal.get_current_registry().settings['systemuser']
        if sysuser == hashlib.sha256(str().join([client, secret]).encode()).hexdigest():
            user.User.create(client=client, secret=secret)
            return []
    return None


class Context:
    def __init__(self, request):
        self.user = None

    __acl__ = (
        (Allow, Authenticated, ALL_PERMISSIONS),
    )

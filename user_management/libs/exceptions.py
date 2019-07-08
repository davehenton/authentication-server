import functools
import http

import pyramid.httpexceptions as exc
import pyramid.request
import pyramid.testing as testing


def exc_handler(function):
    @functools.wraps(function)
    def wrapper(request):
        try:
            return function(request)
        except exc.HTTPBadRequest as e:
            if isinstance(request, (testing.DummyRequest, )):
                raise e
            if not isinstance(request, (pyramid.request.Request, )):
                request = request.request
            status = http.HTTPStatus.BAD_REQUEST
            request.response.status = status
            return exc_response(status, e)
        except exc.HTTPNotFound as e:
            if isinstance(request, (testing.DummyRequest, )):
                raise e
            if not isinstance(request, (pyramid.request.Request, )):
                request = request.request
            status = http.HTTPStatus.NOT_FOUND
            request.response.status = status
            return exc_response(status, e)
        except Exception as e:
            if isinstance(request, (testing.DummyRequest, )):
                raise e
            if not isinstance(request, (pyramid.request.Request, )):
                request = request.request
            status = http.HTTPStatus.INTERNAL_SERVER_ERROR
            request.response.status = status
        except OSError as e:
            if isinstance(request, (testing.DummyRequest, )):
                raise e
            if not isinstance(request, (pyramid.request.Request, )):
                request = request.request
            status = http.HTTPStatus.INTERNAL_SERVER_ERROR
            request.response.status = status
            return exc_response(status, e)
    return wrapper


def exc_response(status, exc):
    return {
        'message': str(exc),
        'status': status
    }

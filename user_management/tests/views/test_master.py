import http

import unittest
import pyramid.testing as testing
import pyramid.paster as paster
import pyramid.registry as registry

import user_management.views.user as user


class UserTest(unittest.TestCase):
    def setUp(self):
        settings = paster.get_appsettings('test.ini', name='main')
        self.config = testing.setUp(settings=settings)
        super().setUp()

    def tearDown(self):
        testing.tearDown()
        super().tearDown()

    def test_create_user(self):
        request = testing.DummyRequest()
        request.params.update({'client': 'dummy', 'secret': 'dummy'})
        u = user.User(request)
        response = u.insert_user()
        self.assertIsNotNone(response)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(response.json, {'check_user': http.HTTPStatus.OK.value})

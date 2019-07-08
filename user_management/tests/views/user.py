import uuid

from user_management.tests.views import ViewsTest


class User(ViewsTest):
    def setUp(self):
        super().setUp()
        self.app.post('/user/insert', dict(client='system', secret='Admin123'))

    def tearDown(self):
        super().tearDown()

    def test_list_users(self):
        response = self.app.get('/user/list')
        user = response.json.get('users')[0]
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(response.json.get('users'), list)
        self.assertIsInstance(user, dict)

    def test_check_user(self):
        response = self.app.get('/user/check')
        user = response.json.get('user')
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(response.json.get('user'), dict)
        self.assertEqual(user.get('user_client'), self.user_client)

    def test_new_user(self):
        userclient = 'test_{0}'.format(uuid.uuid1())
        response = self.app.post('/user/insert', dict(client=userclient, secret='password'))
        user = response.json.get('user')
        self.assertIs(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIsInstance(response.json.get('user'), dict)
        self.assertEqual(user.get('user_client'), userclient)


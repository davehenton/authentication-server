import uuid

from user_management.libs import user
from user_management.models import user as model_user
from user_management.tests.libs import LibsTest


class User(LibsTest):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_user_create(self):
        client = 'test_{0}'.format(uuid.uuid1())
        u = user.User.create(client=client, secret='password', remarks='Testing user', to_dict=True)
        self.assertIsNotNone(u)
        self.assertIsInstance(u, dict)
        self.assertEqual(u.get('user_client'), client)
        self.assertNotEqual(u.get('id'), 1)

    def test_user_by_client(self):
        u = user.User.by_client('system', to_dict=True)
        self.assertIsNotNone(u)
        self.assertIsInstance(u, dict)
        self.assertEqual(u.get('user_client'), 'system')
        self.assertEqual(u.get('id'), 1)

    def test_user_by_client_and_secret(self):
        u = user.User.by_client_and_secret('system', 'Admin123', to_dict=True)
        self.assertIsNotNone(u)
        self.assertIsInstance(u, dict)
        self.assertEqual(u.get('user_client'), 'system')
        self.assertEqual(u.get('id'), 1)

    def test_user_by_id(self):
        u = user.User.by_id(1, to_dict=True)
        self.assertIsNotNone(u)
        self.assertIsInstance(u, dict)
        self.assertEqual(u.get('id'), 1)
        self.assertEqual(u.get('user_client'), 'system')

    def test_user_verify_secret(self):
        u = user.User.by_client('system')
        valid = user.User.verify_secret(u, 'Admin123')
        self.assertIsNotNone(u)
        self.assertIsInstance(u, model_user.User)
        self.assertEqual(u.id, 1)
        self.assertTrue(valid)

    def test_user_verify_secret_fail(self):
        u = user.User.by_client('system')
        valid = user.User.verify_secret(u, 'password')
        self.assertIsNotNone(u)
        self.assertIsInstance(u, model_user.User)
        self.assertEqual(u.id, 1)
        self.assertFalse(valid)

    def test_user_all(self):
        u = user.User.all(to_dict=True)
        self.assertIsNotNone(u)
        self.assertIsInstance(u, list)
        self.assertGreaterEqual(len(u), 1)

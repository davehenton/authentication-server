from user_management.models import user
from user_management.tests.models import ModelTest


class User(ModelTest):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_user_insert(self):
        u = user.User('testing_user', 'testing_secret')
        self.DBSession.add(u)
        query = self.DBSession.query(user.User).filter(user.User.user_client == u.user_client).first()
        self.assertIsNotNone(query)
        self.assertEqual(query.creation_time, u.creation_time)
        self.assertEqual(query.salt, u.salt)
        self.assertEqual(query.user_client, u.user_client)
        self.assertEqual(query.user_secret, u.user_secret)
        self.assertIsNone(query.updated_time)
        self.assertIsNone(query.remarks)
        self.assertEqual(query.id, 2)

    def test_user_delete(self):
        users_count_before = self.DBSession.query(user.User).count()
        query = self.DBSession.query(user.User).first()
        self.DBSession.query(user.User).filter(user.User.id == query.id).delete()
        query = self.DBSession.query(user.User).filter(user.User.id == query.id).first()
        users_count_after = self.DBSession.query(user.User).count()
        self.assertIsNone(query)
        self.assertNotEqual(users_count_before, users_count_after)

    def test_user_update(self):
        u = user.User('testing_user', 'testing_secret')
        remarks = u.remarks
        self.DBSession.add(u)
        self.DBSession.query(user.User).filter(user.User.user_client == u.user_client).update({'remarks': 'Testing'})
        query = self.DBSession.query(user.User).filter(user.User.user_client == u.user_client).first()
        self.assertNotEqual(remarks, query.remarks)

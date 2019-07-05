import unittest

import pyramid.paster as paster
import sqlalchemy
from pyramid import testing
from alembic.command import upgrade as alembic_upgrade, downgrade as alembic_downgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.orm import sessionmaker, scoped_session
from webtest import TestApp


class ViewsTest(unittest.TestCase):
    user_client = 'system'
    user_secret = 'Admin123'

    def setUp(self):
        super().setUp()
        app = paster.get_app('test.ini', name='main')
        self.app = TestApp(app)
        self.app.set_authorization(('Basic', (self.user_client, self.user_secret)))
        settings = paster.get_appsettings('test.ini', name='main')
        self.config = testing.setUp(settings=settings)
        engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
        self.DBSession = scoped_session(sessionmaker())
        self.DBSession.configure(bind=engine)
        self.alembic_config = AlembicConfig('alembic_test.ini')
        self.alembic_config.set_main_option('sqlalchemy.url', settings.get('sqlalchemy.url'))
        alembic_upgrade(self.alembic_config, 'head')

    def tearDown(self):
        super().tearDown()
        self.DBSession.remove()
        testing.tearDown()

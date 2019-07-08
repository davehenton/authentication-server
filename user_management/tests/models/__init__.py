import unittest

import pyramid.paster as paster
import pyramid.testing as testing
import sqlalchemy
from alembic.command import upgrade as alembic_upgrade, downgrade as alembic_downgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy.orm import sessionmaker, scoped_session


class ModelTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        settings = paster.get_appsettings('test.ini', name='main')
        self.config = testing.setUp(settings=settings)
        engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
        self.DBSession = scoped_session(sessionmaker())
        self.DBSession.configure(bind=engine)
        self.alembic_config = AlembicConfig('alembic.ini')
        self.alembic_config.set_main_option('sqlalchemy.url', settings.get('sqlalchemy.url'))
        alembic_upgrade(self.alembic_config, 'head')

    def tearDown(self):
        super().tearDown()
        self.DBSession.remove()
        alembic_downgrade(self.alembic_config, 'base')
        testing.tearDown()

import pytest
from pyramid.paster import get_appsettings
from sqlalchemy import create_engine

import user_management.models as db


def connection(request):
    settings = get_appsettings('test.ini', name='main')
    db_url = settings['sqlalchemy.url']
    engine = create_engine(db_url)
    db.Base.metadata.create_all(engine)
    db_connection = engine.connect()
    db.DBSession.registry.clear()
    db.DBSession.configure(bind=db_connection)
    db.Base.metadata.bind = engine
    request.addfinalizer(db.Base.metadata.drop_all)
    return db_connection


@pytest.fixture(scope='session')
def db_session(request):
    from transaction import abort
    conn = connection(request)
    trans = conn.begin()
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)

    from user_management.models import DBSession
    return DBSession

# @pytest.fixture
# @pytest.mark.usefixtures('db_session')
# def data_fixture(request, db_session):
#     c = category.Category()
#     c.name = 'Category Name'
#     t = types.Type()
#     t.name = 'Type Name'
#     # s = status.Status()
#     # s.status = 'a status'
#     # s.type = 'status type'
#     db_session.add(c)
#     db_session.add(t)
#     # db_session.add(s)
#     db_session.flush()

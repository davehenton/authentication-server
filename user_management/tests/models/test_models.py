# import unittest
#
# import pytest
# from sqlalchemy import func
#
# from user_management.tests.models import (
#     db_session
# )
#
# import user_management.models.user as user
#
# @pytest.mark.usefixtures('db_session')
# def test_create_user(db_session):
#     u = user.User('test_client', 'test_secret')
#     db_session.add(u)
#     db_session.flush()
#     assert u.id is not None
#     assert db_session.query(func.count(user.User.id)).scalar()

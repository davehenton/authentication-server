import user_management.models as db
import user_management.models.user as user
from user_management.libs import Log


class User:

    @staticmethod
    def create(**kwargs):
        u = user.User(**kwargs)
        try:
            db.DBSession.add(u)
            db.DBSession.commit()
            return u.to_dict()
        except Exception as e:
            db.DBSession.rollback()
            Log.error(e)
            return None

    @staticmethod
    def by_client(client):
        try:
            return db.DBSession.query(user.User).filter(user.User.user_client == client).first()
        except Exception as e:
            return None

    @staticmethod
    def by_client_and_secret(client, secret):
        try:
            u = db.DBSession.query(user.User).filter(
                user.User.user_client == client).first()
            if User.verify_secret(u, secret):
                return u.to_dict()
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def by_id(id):
        try:
            return db.DBSession.query(user.User).get(id)
        except Exception as e:
            Log.error(e)
            return None

    @staticmethod
    def verify_secret(u: user.User, secret: str):
        return user.User.hash(secret, u.salt) == u.user_secret

    @staticmethod
    def all():
        try:
            return [row.to_dict() for row in db.DBSession.query(user.User).all()]
        except Exception as e:
            Log.error(e)
            return None

import user_management.models as db
import user_management.models.user as user
from user_management.libs import Log


class User:

    @staticmethod
    def create(to_dict=False, **kwargs):
        u = user.User(**kwargs)
        try:
            db.DBSession.add(u)
            db.DBSession.commit()
            return u.to_dict() if to_dict else u
        except Exception as e:
            db.DBSession.rollback()
            Log.error(e)
            return None

    @staticmethod
    def by_client(client, to_dict=False):
        try:
            u = db.DBSession.query(user.User).filter(user.User.user_client == client).first()
            return u.to_dict() if to_dict else u
        except Exception as e:
            return None

    @staticmethod
    def by_client_and_secret(client, secret, to_dict=False):
        try:
            u = db.DBSession.query(user.User).filter(
                user.User.user_client == client).first()
            if User.verify_secret(u, secret):
                return u.to_dict() if to_dict else u
            else:
                return None
        except Exception as e:
            return None

    @staticmethod
    def by_id(id, to_dict=False):
        try:
            u = db.DBSession.query(user.User).get(id)
            return u.to_dict() if to_dict else u
        except Exception as e:
            Log.error(e)
            return None

    @staticmethod
    def verify_secret(u: user.User, secret: str):
        return user.User.hash(secret, u.salt) == u.user_secret

    @staticmethod
    def all(to_dict=False):
        try:
            u = db.DBSession.query(user.User).all()
            return [row.to_dict() for row in u] if to_dict else u
        except Exception as e:
            Log.error(e)
            return None

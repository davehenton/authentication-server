import json

import pyramid
from sqlalchemy import (
    Text,
    Column,
    Integer,
    Sequence,
    DateTime,
)

import user_management.models as models
import datetime
import uuid
import hashlib


class User(models.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True, nullable=False)
    user_client = Column(Text, nullable=False, unique=True)
    user_secret = Column(Text, nullable=False, unique=False)
    salt = Column(Text, nullable=False, unique=False)
    creation_time = Column(DateTime, nullable=False, unique=False)
    updated_time = Column(DateTime, nullable=True, unique=False, onupdate=datetime.datetime.now())
    remarks = Column(Text, nullable=True, unique=False)

    def __init__(self, client, secret, remarks = None):
        self.salt = self.token()
        self.user_client = client
        self.user_secret = self.hash(secret, self.salt)
        self.creation_time = datetime.datetime.now()
        self.updated_time = None
        self.remarks = remarks

    @staticmethod
    def hash(secret, salt):
        csalt = pyramid.threadlocal.get_current_registry().settings['csalt']
        return hashlib.sha256(str().join([csalt, secret, salt]).encode()).hexdigest()

    @staticmethod
    def token():
        return uuid.uuid1().hex

    def to_dict(self):
        return {
            'id': self.id,
            'user_client': self.user_client,
            'remarks': self.remarks,
        }

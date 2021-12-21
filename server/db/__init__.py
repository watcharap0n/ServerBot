"""
database and authentication master
    - mongodb
    - firebase realtime
    - firebase admin (authentication)

"""

import os
from bson import ObjectId
from . import firebase_auth
from .environ.client_firebase import firebaseConfig, firebaseAuth
from .database import MongoDB
from .object_str import CutId

client = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
db = MongoDB(database_name='MangoBOT', uri=client)


def generate_token(engine):
    """

    :param engine:
    :return:
    """
    obj = object_str.CutId(_id=engine)
    Id = obj.dict()['id']
    return Id

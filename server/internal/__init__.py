from . import config
from . import db
from . import object_str
from bson import ObjectId
import os

Settings = config.Settings
client = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
db = db.MongoDB(database_name='MangoCHATBOT', uri=client)

obj = object_str.CutId(_id=ObjectId())
Id = obj.dict()['id']

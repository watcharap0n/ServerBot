from . import config
from . import db
from . import object_str
from bson import ObjectId

Settings = config.Settings

client = 'mongodb://127.0.0.1:27017'
db = db.MongoDB(database_name='MangoCHATBOT', uri=client)

obj = object_str.CutId(_id=ObjectId())
Id = obj.dict()['id']

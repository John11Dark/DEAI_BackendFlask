import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


from pymongo.mongo_client import MongoClient
import os


uri = os.getenv("MONGO_URI")

# * --> Create a new client and connect to the db server
client = MongoClient(uri)


# * --> return a connection to the database
def connect(key):
    db = client.deaiDb
    return db[key]
